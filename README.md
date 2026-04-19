# Automated Smart Truck Diversion

Critical analysis and synthetic data generation for evaluating ShovelSense-style XRF-based ore sorting and truck diversion systems.

## Overview

This project provides:

1. **Critical Analysis** - Academic review of the ShovelSense white paper against 9 peer-reviewed papers
2. **Synthetic Data Generation** - Realistic mining operations data simulating XRF measurements and truck diversions
3. **Databricks Pipeline** - Bronze/Silver/Gold data pipeline using Spark Declarative Pipelines
4. **PDF Documents** - Technical documentation for RAG testing

## Quick Start

```fish
# Install dependencies
uv pip install -r requirements.txt

# View available commands
just

# Run full pipeline
just all
```

## Project Structure

```
automated-smart-truck-diversion/
├── docs/
│   ├── Automated-Smart-Truck-Diversions_White-Paper-Aug-2022.pdf  # Original paper
│   ├── paper-analysis.md                    # Paper breakdown
│   ├── analysis/                            # Critical assessments
│   │   ├── 00-critical-assessment-summary.md
│   │   ├── 01-openmines-analysis.md
│   │   └── ...
│   └── references/                          # Downloaded academic papers
├── scripts/
│   ├── generate_mining_data.py              # Synthetic data generation
│   └── generate_pdfs.py                     # PDF document generation
├── bundles/
│   ├── databricks.yml                       # Asset Bundle configuration
│   └── src/
│       ├── bronze_silver_pipeline.py        # DLT pipeline
│       └── data_quality_check.py            # Validation notebook
├── justfile                                 # Task orchestration
├── pyproject.toml                           # Python project config
└── requirements.txt                         # Dependencies
```

## Just Commands

| Command | Description |
|---------|-------------|
| `just setup` | Validate Databricks connection |
| `just create-infra` | Create catalog, schema, and volumes |
| `just generate-data` | Generate synthetic mining data |
| `just generate-pdfs` | Generate PDF documents |
| `just deploy` | Deploy Databricks Asset Bundle |
| `just run-pipeline` | Run the DLT pipeline |
| `just all` | Run full pipeline |
| `just config` | Show current configuration |
| `just list-data` | List data in the volume |

## Configuration

Default configuration:
- **Databricks Host**: https://fevm-cjc-aws-workspace.cloud.databricks.com
- **Profile**: fevm-cjc
- **Catalog**: cjc_aws_workspace_catalog
- **Schema**: shovelsense

Override with environment variables:
```fish
set -x CATALOG my_catalog
set -x SCHEMA my_schema
```

## Generated Data

### Structured Data (Parquet)

| Table | Description | ~Rows |
|-------|-------------|-------|
| `block_model` | Geological block model | 500 |
| `shovels` | Shovel fleet master | 3 |
| `trucks` | Truck fleet master | 15 |
| `bucket_measurements` | XRF sensor readings | ~100K |
| `truck_loads` | Aggregated truck loads | ~19K |
| `shift_summaries` | Shift-level stats | ~480 |

### PDF Documents

| Category | Count | Description |
|----------|-------|-------------|
| `technical_docs` | 8 | XRF calibration, FMS integration |
| `geological_reports` | 6 | Block models, grade control |
| `validation_studies` | 5 | Accuracy analysis, reconciliation |
| `operations_procedures` | 5 | Dispatching, safety, training |
| `research_papers` | 6 | Academic literature on ore sorting |

## Critical Findings

The analysis identified significant concerns with ShovelSense claims:

1. **Validation Gap**: No baseline comparison, no confusion matrix, single self-reported case study
2. **Algorithmic Simplicity**: Appears to be threshold rules, not sophisticated ML
3. **Data Integrity**: $2M+ claims lack immutable audit trail
4. **Transparency**: "Proprietary algorithms" with no specifications

See `docs/analysis/00-critical-assessment-summary.md` for full details.

## Data Pipeline

The Databricks pipeline processes data through three layers:

```
Bronze (raw) → Silver (cleaned) → Gold (aggregated)
```

### Bronze Tables
- Direct ingestion from parquet files
- No transformations

### Silver Tables
- Type casting and validation
- Derived fields (shift, grade bins)
- Data quality expectations

### Gold Tables
- `gold_daily_diversions`: Daily stats by shovel
- `gold_classification_accuracy`: Confusion matrix metrics
- `gold_grade_distribution`: Grade stats by geological domain

## License

This project is for research and educational purposes.
