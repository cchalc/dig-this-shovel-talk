# ShovelSense Data Architecture

## Overview

This document describes the data architecture for the ShovelSense Automated Smart Truck Diversion synthetic data pipeline.

## Data Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA MODEL DIAGRAM                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐          ┌──────────────────┐                         │
│  │   dim_shovels    │          │    dim_trucks    │                         │
│  ├──────────────────┤          ├──────────────────┤                         │
│  │ PK shovel_id     │          │ PK truck_id      │                         │
│  │    shovel_type   │          │    truck_model   │                         │
│  │    bucket_cap    │          │    payload_cap   │                         │
│  │    sensor_heads  │          │    fms_system    │                         │
│  └────────┬─────────┘          └────────┬─────────┘                         │
│           │                             │                                    │
│           │         ┌───────────────────┼───────────────────┐               │
│           │         │                   │                   │               │
│           ▼         ▼                   ▼                   │               │
│  ┌──────────────────────────────────────────────────────┐   │               │
│  │              fact_bucket_measurements                 │   │               │
│  ├──────────────────────────────────────────────────────┤   │               │
│  │ PK measurement_id                                     │   │               │
│  │ FK shovel_id ───────────────────────────────────────►│   │               │
│  │ FK truck_id ────────────────────────────────────────►│   │               │
│  │ FK block_id ────────────────────────────────────────►│   │               │
│  │    timestamp                                          │   │               │
│  │    cu_grade_pct, fe_grade_pct, zn_grade_ppm          │   │               │
│  │    xrf_confidence, sensor_status                      │   │               │
│  └──────────────────────────────────────────────────────┘   │               │
│                                                              │               │
│           │                                                  │               │
│           │ (aggregated)                                     │               │
│           ▼                                                  │               │
│  ┌──────────────────────────────────────────────────────┐   │               │
│  │                 fact_truck_loads                      │   │               │
│  ├──────────────────────────────────────────────────────┤   │               │
│  │ PK load_id                                            │   │               │
│  │ FK truck_id ─────────────────────────────────────────┼───┘               │
│  │ FK shovel_id                                          │                   │
│  │ FK block_id                                           │                   │
│  │    timestamp, n_buckets                               │                   │
│  │    avg_cu_grade_pct, avg_fe_grade_pct                │                   │
│  │    planned_classification, shovelsense_classification │                   │
│  │    diversion_type, destination                        │                   │
│  │    payload_tonnes, cycle_time_minutes                 │                   │
│  └──────────────────────────────────────────────────────┘                   │
│                                                                              │
│           │                                                                  │
│           │ (aggregated)                                                     │
│           ▼                                                                  │
│  ┌──────────────────────────────────────────────────────┐                   │
│  │              fact_daily_diversions                    │                   │
│  ├──────────────────────────────────────────────────────┤                   │
│  │    load_date                                          │                   │
│  │ FK shovel_id                                          │                   │
│  │    total_trucks, diverted_trucks                      │                   │
│  │    ore_from_waste, waste_from_ore                     │                   │
│  │    diversion_rate, avg_cu_grade                       │                   │
│  │    total_tonnes                                        │                   │
│  └──────────────────────────────────────────────────────┘                   │
│                                                                              │
│  ┌──────────────────┐                                                       │
│  │  dim_block_model │◄─────────────────────────────────────────────────────┐│
│  ├──────────────────┤                                    (referenced by)   ││
│  │ PK block_id      │                                    measurements &    ││
│  │    bench         │                                    truck_loads       ││
│  │    easting       │                                                      ││
│  │    northing      │                                                      ││
│  │    elevation     │                                                      ││
│  │    planned_cu    │                                                      ││
│  │    geo_domain    │                                                      ││
│  │    is_dyke       │                                                      ││
│  │    blast_move    │                                                      ││
│  └──────────────────┘                                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Medallion Architecture

### Bronze Layer (Raw Ingestion)
Raw data ingested from parquet files with minimal transformation.

| Table | Source | Description |
|-------|--------|-------------|
| `bronze_block_model` | block_model.parquet | Geological block model |
| `bronze_shovels` | shovels.parquet | Shovel fleet master data |
| `bronze_trucks` | trucks.parquet | Truck fleet master data |
| `bronze_bucket_measurements` | bucket_measurements.parquet | XRF sensor readings |
| `bronze_truck_loads` | truck_loads.parquet | Aggregated truck loads |
| `bronze_shift_summaries` | shift_summaries.parquet | Shift-level statistics |

### Silver Layer (Cleaned & Validated)
Data quality checks, type casting, and enrichment.

| Table | Source | Transformations |
|-------|--------|-----------------|
| `silver_block_model` | bronze_block_model | Add is_ore flag, grade_bin |
| `silver_shovels` | bronze_shovels | Cast dates, validate IDs |
| `silver_trucks` | bronze_trucks | Validate IDs |
| `silver_bucket_measurements` | bronze_bucket_measurements | Parse timestamps, add quality flags |
| `silver_truck_loads` | bronze_truck_loads | Parse timestamps, add shift/diversion flags |
| `silver_shift_summaries` | bronze_shift_summaries | Cast dates |

### Gold Layer (Business-Ready)
Dimension and fact tables following Kimball star schema.

| Table | Type | Description |
|-------|------|-------------|
| `dim_shovels` | Dimension | Shovel attributes |
| `dim_trucks` | Dimension | Truck attributes |
| `dim_block_model` | Dimension | Geological reference |
| `dim_date` | Dimension | Date dimension for time analysis |
| `fact_bucket_measurements` | Fact | XRF measurement facts |
| `fact_truck_loads` | Fact | Truck load facts with diversions |
| `fact_daily_diversions` | Fact | Daily diversion aggregates |
| `fact_classification_accuracy` | Fact | Classification metrics (confusion matrix) |

## Entity Relationships

### Primary Keys
- `dim_shovels.shovel_id` (VARCHAR)
- `dim_trucks.truck_id` (VARCHAR)
- `dim_block_model.block_id` (VARCHAR)
- `dim_date.date_key` (INT, YYYYMMDD format)
- `fact_bucket_measurements.measurement_id` (VARCHAR)
- `fact_truck_loads.load_id` (VARCHAR)

### Foreign Key Relationships

```
fact_bucket_measurements
  ├── shovel_id → dim_shovels.shovel_id
  ├── truck_id → dim_trucks.truck_id
  ├── block_id → dim_block_model.block_id
  └── measurement_date_key → dim_date.date_key

fact_truck_loads
  ├── shovel_id → dim_shovels.shovel_id
  ├── truck_id → dim_trucks.truck_id
  ├── block_id → dim_block_model.block_id
  └── load_date_key → dim_date.date_key

fact_daily_diversions
  ├── shovel_id → dim_shovels.shovel_id
  └── date_key → dim_date.date_key
```

## Data Quality Rules

### Bronze Layer
- No transformations, append metadata columns
- Add `_ingested_at` timestamp
- Add `_source_file` path

### Silver Layer
| Table | Rule | Action |
|-------|------|--------|
| All | NULL primary keys | Drop row |
| bucket_measurements | xrf_confidence < 0.5 | Drop row |
| bucket_measurements | cu_grade_pct < 0 | Drop row |
| truck_loads | avg_cu_grade_pct < 0 | Drop row |

### Gold Layer
- Aggregate integrity checks
- Referential integrity validation
- Business rule validation (diversion rates within expected ranges)

## Key Metrics

### Operational Metrics
| Metric | Calculation | Expected Range |
|--------|-------------|----------------|
| Diversion Rate | diverted_trucks / total_trucks | 8-15% |
| Ore from Waste Rate | ore_from_waste / total_trucks | 5-8% |
| Waste from Ore Rate | waste_from_ore / total_trucks | 3-6% |
| XRF Confidence | avg(xrf_confidence) | > 0.85 |
| Sensor Availability | both_sensors_active / total | > 95% |

### Classification Metrics
| Metric | Formula |
|--------|---------|
| Accuracy | (TP + TN) / Total |
| Precision (Ore) | TP / (TP + FP) |
| Recall (Ore) | TP / (TP + FN) |
| F1 Score | 2 × (Precision × Recall) / (Precision + Recall) |

## Pipeline Configuration

```yaml
Catalog: cjc_aws_workspace_catalog
Schema: shovelsense
Volume: raw_data
Pipeline: shovelsense_pipeline

Compute: Serverless
Mode: Triggered (batch)
```

## Data Lineage

```
Volume (parquet files)
    │
    ▼
Bronze Tables (raw ingestion)
    │
    ▼
Silver Tables (cleaned, validated)
    │
    ├──────────────────┬──────────────────┐
    ▼                  ▼                  ▼
Dimension Tables   Fact Tables      Aggregate Facts
(dim_*)            (fact_*)         (fact_daily_*)
```

## Volume and Refresh Estimates

| Layer | Tables | Est. Rows | Refresh Frequency |
|-------|--------|-----------|-------------------|
| Bronze | 6 | ~105K | On new data arrival |
| Silver | 6 | ~105K | Incremental |
| Gold | 8 | ~20K | Daily |

## Access Patterns

### Common Queries

1. **Daily Diversion Summary**
```sql
SELECT * FROM gold_daily_diversions
WHERE load_date >= CURRENT_DATE - 7
ORDER BY load_date DESC, shovel_id
```

2. **Classification Accuracy by Day**
```sql
SELECT * FROM gold_classification_accuracy
ORDER BY load_date DESC
```

3. **Grade Distribution by Domain**
```sql
SELECT * FROM gold_grade_distribution
ORDER BY geological_domain, grade_bin
```

4. **Truck Load Details with Dimensions**
```sql
SELECT
  f.*,
  s.shovel_type,
  t.truck_model,
  b.geological_domain
FROM fact_truck_loads f
JOIN dim_shovels s ON f.shovel_id = s.shovel_id
JOIN dim_trucks t ON f.truck_id = t.truck_id
JOIN dim_block_model b ON f.block_id = b.block_id
WHERE f.is_diverted = true
```
