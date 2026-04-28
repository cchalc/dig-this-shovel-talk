"""
Apply table and column descriptions to Delta tables in Databricks.

This script adds documentation from the pipeline-documentation.md as metadata
directly on the Delta tables, making them discoverable in Unity Catalog.

Usage:
    python scripts/apply_table_metadata.py

Requires:
    - databricks-sdk
    - Valid Databricks authentication
"""

import os
import sys
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import StatementState

# Configuration
CATALOG = os.environ.get("CATALOG", "cjc_aws_workspace_catalog")
SCHEMA = os.environ.get("SCHEMA", "shovelsense")
WAREHOUSE_ID = os.environ.get("WAREHOUSE_ID", "751fe324525584e5")
PROFILE = os.environ.get("DATABRICKS_CONFIG_PROFILE", "fevm-cjc")

# =============================================================================
# TABLE METADATA
# =============================================================================

TABLE_COMMENTS = {
    # Bronze Layer
    "bronze_block_model": "Raw geological block model data ingested from parquet. Contains spatial coordinates, planned grades from blast hole sampling, mineralogy (chalcopyrite/bornite percentages), and surface-volume correlation estimates.",
    "bronze_shovels": "Raw shovel fleet master data. Includes XRF sensor specifications (detector type, penetration depth, detection limits) per Round 1 XRF physics analysis.",
    "bronze_trucks": "Raw haul truck fleet master data with payload capacity and FMS integration details.",
    "bronze_bucket_measurements": "Raw XRF sensor readings per bucket. Contains grade measurements, confidence scores, matrix effect factors, and heterogeneity error estimates from Round 1 analysis.",
    "bronze_truck_loads": "Raw truck load data with planned (blast hole) vs actual (XRF) classification comparison. Enables confusion matrix analysis per Critical Assessment.",
    "bronze_shift_summaries": "Raw shift-level operational summaries including diversion rates and F1 factor estimates.",

    # Silver Layer
    "silver_block_model": "Cleaned geological block model with mineralogy classification and surface-volume correlation quality indicators. Implements Round 1 zonation: Bornite core → Chalcopyrite zone → Pyrite halo.",
    "silver_shovels": "Cleaned shovel fleet data with parsed dates and days-in-service calculation.",
    "silver_trucks": "Cleaned truck fleet data with validated identifiers.",
    "silver_bucket_measurements": "Cleaned XRF measurements with matrix effect severity classification, measurement quality scores, and grade categorization. Addresses Round 1 heterogeneity error findings.",
    "silver_truck_loads": "Cleaned truck loads with economic valuation (Round 3), diversion flags, and XRF reliability indicators. Includes estimated copper value per load using $8,820/tonne copper price and 85% metallurgical recovery.",
    "silver_shift_summaries": "Cleaned shift summaries with parsed dates and date keys for dimension joins.",

    # Gold Dimensions
    "dim_shovels": "Shovel dimension table. Conformed dimension for star schema with equipment attributes and XRF sensor presence flags.",
    "dim_trucks": "Truck dimension table. Conformed dimension with vehicle attributes and FMS system identification.",
    "dim_block_model": "Block model dimension with mineralogy and XRF suitability indicators. Contains the 'critical unknown' from Round 1: surface-volume correlation that predicts XRF accuracy.",
    "dim_date": "Standard date dimension for time-series analysis. Covers the full date range of truck load data.",

    # Gold Facts
    "fact_bucket_measurements": "Fact table for XRF bucket measurements. Grain: one row per measurement. Includes matrix effect analysis from Round 1 XRF physics.",
    "fact_truck_loads": "Fact table for truck loads with diversion classification and economic impact. Grain: one row per load. Contains estimated_cu_value_usd from Round 3 economic model.",

    # Gold Aggregates
    "fact_daily_diversions": "Daily diversion statistics by shovel. Measures the '11% diversion rate' claim from ShovelSense white paper. Includes ore recovery and dilution prevention rates.",
    "fact_classification_accuracy": "Daily confusion matrix metrics. Addresses Critical Assessment gap: 'No confusion matrix for grade classification.' Includes precision, recall, and F1 score.",
    "fact_grade_distribution": "Grade distribution statistics by geological domain. Based on Queen's University sampling error research.",
    "fact_sensor_performance": "XRF sensor reliability metrics by shovel and date. Tracks calibration drift and dual-sensor redundancy per Round 3 Direction D failure modes.",
    "fact_domain_classification_accuracy": "Classification accuracy stratified by geological domain. Tests Round 2 hypothesis: 'XRF accuracy may vary spatially' based on chalcopyrite/bornite distribution.",
    "fact_sv_correlation_analysis": "Surface-volume correlation analysis. Tests the Round 1 'critical unknown': Does higher S-V correlation lead to better classification accuracy?",
    "summary_overall_performance": "Single-row summary with key performance indicators aligned to dialectical analysis metrics. Includes overall diversion rate, F1 score, and total copper value.",
}

# =============================================================================
# COLUMN METADATA
# =============================================================================

COLUMN_COMMENTS = {
    # dim_block_model - the most documented dimension
    "dim_block_model": {
        "block_id": "Primary key. Unique identifier for geological block.",
        "bench": "Mining bench level (elevation tier).",
        "easting": "X coordinate in mine grid (meters).",
        "northing": "Y coordinate in mine grid (meters).",
        "elevation": "Z coordinate / elevation (meters).",
        "planned_cu_grade": "Copper grade (%) from blast hole sampling. Used as 'ground truth' for classification.",
        "planned_fe_grade": "Iron grade (%) from blast hole sampling.",
        "planned_classification": "ORE or WASTE based on 0.32% Cu cutoff grade.",
        "geological_domain": "Zonation: BORNITE_CORE, CHALCOPYRITE_ZONE, PYRITE_HALO, SUPERGENE, LEACHED_CAP, WASTE_ZONE. From Round 1 deposit model.",
        "is_dyke": "Whether block intersects a barren dyke.",
        "blast_movement_m": "Estimated blast-induced movement (meters). Source of grade control error per AusIMM 2008.",
        "is_ore": "True if planned_cu_grade >= 0.32% cutoff.",
        "grade_bin": "Grade category: HIGH (>=1%), MEDIUM (>=0.5%), LOW (>=0.32%), WASTE (<0.32%).",
        "block_volume_m3": "Block volume in cubic meters (15m x 15m x 15m = 3,375 m³).",
        "chalcopyrite_pct": "Chalcopyrite (CuFeS₂) percentage. ~80% average per Round 1. Has 30.5% Fe causing matrix effects.",
        "bornite_pct": "Bornite (Cu₅FeS₄) percentage. ~20% average per Round 1. Higher Cu content, lower matrix effect.",
        "mineralogy_class": "BORNITE_DOMINANT (>50% bornite), CHALCOPYRITE_DOMINANT (>70% chalcopyrite), or MIXED.",
        "surface_volume_correlation": "Estimated correlation between surface XRF readings and volumetric grade. THE CRITICAL UNKNOWN from Round 1.",
        "sv_correlation_quality": "HIGH (>=0.70), MODERATE (0.50-0.70), or LOW (<0.50). Predicts XRF reliability.",
        "nugget_effect_variance": "Short-scale grade variability. High values indicate erratic grades within blocks.",
        "vein_density_class": "LOW, MEDIUM, or HIGH vein density. Affects heterogeneity error.",
    },

    # fact_truck_loads - the central fact table
    "fact_truck_loads": {
        "load_id": "Primary key. Unique identifier for truck load.",
        "load_date_key": "Foreign key to dim_date (YYYYMMDD format).",
        "shovel_id": "Foreign key to dim_shovels.",
        "truck_id": "Foreign key to dim_trucks.",
        "block_id": "Foreign key to dim_block_model. Source block for this load.",
        "timestamp": "Load timestamp (when truck departed shovel).",
        "load_date": "Date portion of timestamp.",
        "load_hour": "Hour portion of timestamp (0-23).",
        "shift": "DAY (6am-6pm) or NIGHT (6pm-6am).",
        "day_of_week": "1=Sunday through 7=Saturday.",
        "is_weekend": "True if Saturday or Sunday.",
        "n_buckets": "Number of bucket passes to fill truck (typically 4-6).",
        "avg_cu_grade_pct": "Average XRF-measured copper grade across all buckets.",
        "avg_fe_grade_pct": "Average XRF-measured iron grade across all buckets.",
        "payload_tonnes": "Actual payload weight in tonnes.",
        "cycle_time_minutes": "Total cycle time (load + haul + dump + return).",
        "estimated_cu_tonnes": "Contained copper tonnes = payload × grade / 100.",
        "avg_xrf_confidence": "Average XRF confidence score across buckets (0-1).",
        "surface_volume_correlation": "S-V correlation for source block. Predicts XRF accuracy.",
        "sv_correlation_quality": "HIGH, MODERATE, or LOW based on S-V correlation thresholds.",
        "xrf_reliability": "Composite reliability: HIGH (conf>=0.90 AND sv>=0.60), MODERATE, or LOW.",
        "geological_domain": "Source block geological domain for stratified analysis.",
        "estimated_cu_value_usd": "Economic value = payload × grade × 0.85 recovery × $8,820/t Cu. From Round 3.",
        "planned_classification": "ORE or WASTE from blast hole model (ground truth).",
        "shovelsense_classification": "ORE or WASTE from XRF measurement (sensor decision).",
        "diversion_type": "ALIGNED (agreement), ORE_FROM_WASTE (false positive), WASTE_FROM_ORE (false negative).",
        "destination": "MILL or WASTE_DUMP based on ShovelSense classification.",
        "grade_bin": "Grade category based on avg_cu_grade_pct.",
        "is_diverted": "True if planned != shovelsense classification.",
        "is_ore_recovery": "True if diversion_type = ORE_FROM_WASTE (value capture).",
        "is_dilution_prevention": "True if diversion_type = WASTE_FROM_ORE (dilution avoided).",
    },

    # fact_bucket_measurements
    "fact_bucket_measurements": {
        "measurement_id": "Primary key. Unique identifier for XRF measurement.",
        "measurement_date_key": "Foreign key to dim_date.",
        "shovel_id": "Foreign key to dim_shovels.",
        "truck_id": "Foreign key to dim_trucks.",
        "block_id": "Foreign key to dim_block_model.",
        "timestamp": "Measurement timestamp.",
        "measurement_date": "Date portion of timestamp.",
        "measurement_hour": "Hour portion of timestamp.",
        "bucket_number": "Sequential bucket number within truck load (1-6).",
        "cu_grade_pct": "XRF-measured copper grade (%).",
        "fe_grade_pct": "XRF-measured iron grade (%).",
        "zn_grade_ppm": "XRF-measured zinc grade (ppm).",
        "as_grade_ppm": "XRF-measured arsenic grade (ppm). Penalty element.",
        "laser_fill_level_pct": "Bucket fill level from laser sensor (%).",
        "xrf_confidence": "XRF measurement confidence score (0-1). Higher = more reliable.",
        "matrix_effect_factor": "Fe-Cu absorption correction factor. <1.0 indicates significant matrix effect from chalcopyrite iron.",
        "matrix_effect_severity": "HIGH (<0.95), MODERATE (0.95-0.98), or LOW (>0.98) matrix effect.",
        "measurement_quality_score": "Composite: 0.5×confidence + 0.3×matrix_factor + 0.2×dual_sensor.",
        "sensor_head_1_active": "True if primary XRF sensor was active.",
        "sensor_head_2_active": "True if secondary XRF sensor was active.",
        "both_sensors_active": "True if dual-sensor redundancy was available.",
        "is_high_confidence": "True if xrf_confidence >= 0.90.",
        "grade_category": "HIGH_GRADE, MEDIUM_GRADE, LOW_GRADE, or WASTE based on cu_grade_pct.",
    },

    # fact_classification_accuracy
    "fact_classification_accuracy": {
        "load_date": "Date for this accuracy record.",
        "load_date_key": "Foreign key to dim_date.",
        "total_loads": "Total truck loads on this date.",
        "true_positive": "Planned=ORE, XRF=ORE. Correct ore identification.",
        "true_negative": "Planned=WASTE, XRF=WASTE. Correct waste identification.",
        "false_positive": "Planned=WASTE, XRF=ORE. Ore from Waste (value capture).",
        "false_negative": "Planned=ORE, XRF=WASTE. Waste from Ore (dilution prevention or lost ore).",
        "accuracy": "(TP + TN) / Total. Overall classification accuracy.",
        "precision_ore": "TP / (TP + FP). Of loads sent to mill, what % were actually ore?",
        "recall_ore": "TP / (TP + FN). Of actual ore loads, what % were correctly identified?",
        "f1_score": "2 × Precision × Recall / (Precision + Recall). Harmonic mean. Key metric from Round 2.",
    },

    # fact_daily_diversions
    "fact_daily_diversions": {
        "load_date": "Date for this diversion record.",
        "load_date_key": "Foreign key to dim_date.",
        "shovel_id": "Foreign key to dim_shovels.",
        "total_trucks": "Total truck loads from this shovel on this date.",
        "diverted_trucks": "Loads where planned != shovelsense classification.",
        "ore_from_waste_count": "Loads diverted from waste dump to mill (value capture).",
        "waste_from_ore_count": "Loads diverted from mill to waste dump (dilution prevention).",
        "avg_cu_grade": "Average copper grade for loads from this shovel.",
        "total_tonnes": "Total payload tonnes from this shovel.",
        "total_cu_tonnes": "Total contained copper tonnes.",
        "avg_cycle_time": "Average truck cycle time in minutes.",
        "diversion_rate": "diverted_trucks / total_trucks. Target ~11% per white paper.",
        "ore_recovery_rate": "ore_from_waste_count / total_trucks. Target ~6.4% per white paper.",
        "dilution_prevention_rate": "waste_from_ore_count / total_trucks. Target ~4.7% per white paper.",
    },

    # fact_domain_classification_accuracy
    "fact_domain_classification_accuracy": {
        "geological_domain": "Geological zone being analyzed.",
        "total_loads": "Total truck loads from this domain.",
        "true_positive": "Correct ore identifications in this domain.",
        "true_negative": "Correct waste identifications in this domain.",
        "false_positive": "Ore from Waste diversions in this domain.",
        "false_negative": "Waste from Ore diversions in this domain.",
        "avg_surface_volume_corr": "Average S-V correlation in this domain. Higher = better XRF accuracy expected.",
        "avg_xrf_confidence": "Average XRF confidence in this domain.",
        "total_cu_value_usd": "Total copper value processed from this domain.",
        "accuracy": "Classification accuracy within this domain.",
        "precision_ore": "Ore precision within this domain.",
        "recall_ore": "Ore recall within this domain.",
        "f1_score": "F1 score within this domain. Key metric for zone-specific XRF value.",
        "diversion_rate": "Diversion rate within this domain.",
    },

    # fact_sv_correlation_analysis
    "fact_sv_correlation_analysis": {
        "sv_corr_bin": "Surface-volume correlation bin: 0.70-1.00 (high), 0.55-0.70, 0.40-0.55, 0.00-0.40 (low).",
        "total_loads": "Total truck loads in this S-V correlation bin.",
        "correct_classifications": "Loads where planned = shovelsense classification.",
        "ore_from_waste": "Ore from Waste diversions in this bin.",
        "waste_from_ore": "Waste from Ore diversions in this bin.",
        "avg_xrf_confidence": "Average XRF confidence in this bin.",
        "avg_sv_correlation": "Average S-V correlation in this bin.",
        "total_cu_value_usd": "Total copper value in this bin.",
        "accuracy_rate": "correct_classifications / total_loads. Should increase with S-V correlation.",
        "diversion_rate": "1 - accuracy_rate. Should decrease with S-V correlation.",
    },

    # fact_sensor_performance
    "fact_sensor_performance": {
        "measurement_date": "Date for this performance record.",
        "measurement_date_key": "Foreign key to dim_date.",
        "shovel_id": "Foreign key to dim_shovels.",
        "total_measurements": "Total XRF measurements from this shovel on this date.",
        "avg_confidence": "Average XRF confidence score. Trend indicates calibration health.",
        "min_confidence": "Minimum confidence. Low values may indicate sensor issues.",
        "max_confidence": "Maximum confidence.",
        "high_confidence_count": "Measurements with confidence >= 0.90.",
        "both_sensors_active_count": "Measurements with dual-sensor redundancy.",
        "sensor_1_failures": "Primary sensor failure count.",
        "sensor_2_failures": "Secondary sensor failure count.",
        "high_confidence_rate": "high_confidence_count / total_measurements.",
        "dual_sensor_rate": "both_sensors_active_count / total_measurements. Target >95%.",
        "sensor_1_failure_rate": "Primary sensor failure rate.",
        "sensor_2_failure_rate": "Secondary sensor failure rate.",
    },

    # summary_overall_performance
    "summary_overall_performance": {
        "total_trucks": "Total truck loads in dataset.",
        "total_diversions": "Total diverted loads (planned != shovelsense).",
        "total_ore_from_waste": "Total Ore from Waste diversions (value capture).",
        "total_waste_from_ore": "Total Waste from Ore diversions (dilution prevention).",
        "total_tonnes_processed": "Total payload tonnes processed.",
        "total_cu_tonnes": "Total contained copper tonnes.",
        "avg_daily_diversion_rate": "Average daily diversion rate. Compare to 11% target.",
        "avg_accuracy": "Average daily classification accuracy.",
        "avg_precision": "Average daily ore precision.",
        "avg_recall": "Average daily ore recall.",
        "avg_f1": "Average daily F1 score. Key baseline metric from Round 2.",
        "total_cu_value_usd": "Total copper value processed (USD).",
        "avg_head_grade_pct": "Average head grade (%). Compare to 0.45% target.",
        "avg_sv_correlation": "Average surface-volume correlation. The critical unknown.",
        "avg_xrf_confidence": "Average XRF confidence across all measurements.",
    },
}


def run_sql(client, statement: str, description: str = "") -> bool:
    """Execute a SQL statement and return success status."""
    try:
        response = client.statement_execution.execute_statement(
            warehouse_id=WAREHOUSE_ID,
            statement=statement,
            wait_timeout="50s",
        )

        if response.status.state in [StatementState.SUCCEEDED, StatementState.CLOSED]:
            return True
        else:
            error_msg = response.status.error.message if response.status.error else "Unknown error"
            print(f"  FAILED: {description or statement[:60]}...")
            print(f"    Error: {error_msg}")
            return False
    except Exception as e:
        print(f"  ERROR: {description or statement[:60]}...")
        print(f"    Exception: {e}")
        return False


def apply_table_comments(client) -> tuple[int, int]:
    """Apply table-level comments."""
    print("\n" + "=" * 70)
    print("APPLYING TABLE COMMENTS")
    print("=" * 70)

    success = 0
    failed = 0

    for table, comment in TABLE_COMMENTS.items():
        full_table = f"{CATALOG}.{SCHEMA}.{table}"
        # Escape single quotes in comment
        escaped_comment = comment.replace("'", "''")
        sql = f"COMMENT ON TABLE {full_table} IS '{escaped_comment}'"

        if run_sql(client, sql, f"Table comment: {table}"):
            print(f"  OK: {table}")
            success += 1
        else:
            failed += 1

    return success, failed


def get_table_types(client) -> dict[str, str]:
    """Query information_schema to get table types."""
    sql = f"""
        SELECT table_name, table_type
        FROM {CATALOG}.information_schema.tables
        WHERE table_schema = '{SCHEMA}'
    """
    try:
        response = client.statement_execution.execute_statement(
            warehouse_id=WAREHOUSE_ID,
            statement=sql,
            wait_timeout="50s",
        )
        if response.status.state in [StatementState.SUCCEEDED, StatementState.CLOSED]:
            result = {}
            for row in response.result.data_array:
                result[row[0]] = row[1]
            return result
    except Exception as e:
        print(f"  Warning: Could not query table types: {e}")
    return {}


def apply_column_comments(client, table_types: dict[str, str]) -> tuple[int, int, int]:
    """Apply column-level comments (only to MANAGED tables, not views)."""
    print("\n" + "=" * 70)
    print("APPLYING COLUMN COMMENTS")
    print("=" * 70)

    success = 0
    failed = 0
    skipped = 0

    for table, columns in COLUMN_COMMENTS.items():
        table_type = table_types.get(table, "UNKNOWN")

        if table_type in ["MATERIALIZED_VIEW", "VIEW"]:
            print(f"\n  Table: {table} (SKIPPED - {table_type})")
            print(f"    Column comments cannot be applied to views.")
            print(f"    {len(columns)} columns documented in pipeline-documentation.md")
            skipped += len(columns)
            continue

        print(f"\n  Table: {table} ({table_type})")
        full_table = f"{CATALOG}.{SCHEMA}.{table}"

        for column, comment in columns.items():
            # Escape single quotes in comment
            escaped_comment = comment.replace("'", "''")
            sql = f"ALTER TABLE {full_table} ALTER COLUMN {column} COMMENT '{escaped_comment}'"

            if run_sql(client, sql, f"{table}.{column}"):
                print(f"    OK: {column}")
                success += 1
            else:
                failed += 1

    return success, failed, skipped


def apply_table_tags(client) -> tuple[int, int]:
    """Apply table tags for categorization."""
    print("\n" + "=" * 70)
    print("APPLYING TABLE TAGS")
    print("=" * 70)

    # Define tags by table category
    # Note: "source" tag removed due to workspace tag policy restrictions
    TAGS = {
        "layer": {
            "bronze": ["bronze_block_model", "bronze_shovels", "bronze_trucks",
                      "bronze_bucket_measurements", "bronze_truck_loads", "bronze_shift_summaries"],
            "silver": ["silver_block_model", "silver_shovels", "silver_trucks",
                      "silver_bucket_measurements", "silver_truck_loads", "silver_shift_summaries"],
            "gold": ["dim_shovels", "dim_trucks", "dim_block_model", "dim_date",
                    "fact_bucket_measurements", "fact_truck_loads", "fact_daily_diversions",
                    "fact_classification_accuracy", "fact_grade_distribution", "fact_sensor_performance",
                    "fact_domain_classification_accuracy", "fact_sv_correlation_analysis",
                    "summary_overall_performance"],
        },
        "table_type": {
            "dimension": ["dim_shovels", "dim_trucks", "dim_block_model", "dim_date"],
            "fact": ["fact_bucket_measurements", "fact_truck_loads"],
            "aggregate": ["fact_daily_diversions", "fact_classification_accuracy", "fact_grade_distribution",
                         "fact_sensor_performance", "fact_domain_classification_accuracy",
                         "fact_sv_correlation_analysis", "summary_overall_performance"],
        },
    }

    success = 0
    failed = 0

    for tag_key, tag_values in TAGS.items():
        for tag_value, tables in tag_values.items():
            for table in tables:
                full_table = f"{CATALOG}.{SCHEMA}.{table}"
                sql = f"ALTER TABLE {full_table} SET TAGS ('{tag_key}' = '{tag_value}')"

                if run_sql(client, sql, f"Tag {table}: {tag_key}={tag_value}"):
                    success += 1
                else:
                    failed += 1

    print(f"\n  Applied {success} tags, {failed} failed")
    return success, failed


def create_data_dictionary(client, table_types: dict[str, str]) -> tuple[int, int]:
    """Create and populate a data dictionary table with column descriptions."""
    print("\n" + "=" * 70)
    print("CREATING DATA DICTIONARY TABLE")
    print("=" * 70)

    full_table = f"{CATALOG}.{SCHEMA}.data_dictionary"

    # Drop and recreate the table
    drop_sql = f"DROP TABLE IF EXISTS {full_table}"
    run_sql(client, drop_sql, "Drop existing data_dictionary")

    create_sql = f"""
        CREATE TABLE {full_table} (
            table_name STRING NOT NULL COMMENT 'Name of the table',
            column_name STRING NOT NULL COMMENT 'Name of the column',
            column_position INT COMMENT 'Position of column in table (1-based)',
            data_type STRING COMMENT 'SQL data type of the column',
            description STRING COMMENT 'Human-readable description of the column',
            is_primary_key BOOLEAN COMMENT 'Whether this column is a primary key',
            is_foreign_key BOOLEAN COMMENT 'Whether this column is a foreign key',
            foreign_key_table STRING COMMENT 'Referenced table if foreign key',
            dialectic_reference STRING COMMENT 'Reference to dialectical analysis round',
            updated_at TIMESTAMP COMMENT 'When this entry was last updated'
        )
        USING DELTA
        COMMENT 'Data dictionary containing column descriptions for all pipeline tables. Workaround for materialized view column comment limitation.'
        TBLPROPERTIES (
            'delta.columnMapping.mode' = 'name'
        )
    """

    if not run_sql(client, create_sql, "Create data_dictionary table"):
        print("  ERROR: Failed to create data_dictionary table")
        return 0, 1

    print("  Created data_dictionary table")

    # Build insert statements for all documented columns
    success = 0
    failed = 0

    # Get column info from information_schema for each table
    for table_name, columns in COLUMN_COMMENTS.items():
        # Query actual column info from the table
        col_info_sql = f"""
            SELECT column_name, ordinal_position, data_type
            FROM {CATALOG}.information_schema.columns
            WHERE table_schema = '{SCHEMA}' AND table_name = '{table_name}'
        """

        col_info = {}
        try:
            response = client.statement_execution.execute_statement(
                warehouse_id=WAREHOUSE_ID,
                statement=col_info_sql,
                wait_timeout="50s",
            )
            if response.status.state in [StatementState.SUCCEEDED, StatementState.CLOSED]:
                if response.result and response.result.data_array:
                    for row in response.result.data_array:
                        col_info[row[0]] = {"position": row[1], "data_type": row[2]}
        except Exception as e:
            print(f"  Warning: Could not get column info for {table_name}: {e}")

        # Insert each column
        for col_name, description in columns.items():
            info = col_info.get(col_name, {"position": None, "data_type": None})

            # Determine if primary/foreign key based on naming conventions
            is_pk = col_name.endswith("_id") and col_name in ["load_id", "measurement_id", "block_id", "shovel_id", "truck_id"]
            is_fk = col_name.endswith("_id") or col_name.endswith("_key")
            fk_table = None
            if is_fk and not is_pk:
                if col_name == "load_date_key" or col_name == "measurement_date_key":
                    fk_table = "dim_date"
                elif col_name == "shovel_id" and table_name != "dim_shovels":
                    fk_table = "dim_shovels"
                elif col_name == "truck_id" and table_name != "dim_trucks":
                    fk_table = "dim_trucks"
                elif col_name == "block_id" and table_name != "dim_block_model":
                    fk_table = "dim_block_model"

            # Determine dialectic reference from description
            dialectic_ref = None
            if "Round 1" in description:
                dialectic_ref = "Round 1"
            elif "Round 2" in description:
                dialectic_ref = "Round 2"
            elif "Round 3" in description:
                dialectic_ref = "Round 3"
            elif "Critical Assessment" in description:
                dialectic_ref = "Critical Assessment"

            # Escape quotes
            escaped_desc = description.replace("'", "''")

            insert_sql = f"""
                INSERT INTO {full_table}
                (table_name, column_name, column_position, data_type, description,
                 is_primary_key, is_foreign_key, foreign_key_table, dialectic_reference, updated_at)
                VALUES (
                    '{table_name}',
                    '{col_name}',
                    {info['position'] if info['position'] else 'NULL'},
                    {f"'{info['data_type']}'" if info['data_type'] else 'NULL'},
                    '{escaped_desc}',
                    {str(is_pk).lower()},
                    {str(is_fk).lower()},
                    {f"'{fk_table}'" if fk_table else 'NULL'},
                    {f"'{dialectic_ref}'" if dialectic_ref else 'NULL'},
                    current_timestamp()
                )
            """

            if run_sql(client, insert_sql, f"Insert {table_name}.{col_name}"):
                success += 1
            else:
                failed += 1

        print(f"  {table_name}: {len(columns)} columns")

    # Add column comments to the data_dictionary table itself
    print("\n  Adding column comments to data_dictionary table...")
    dd_columns = {
        "table_name": "Name of the table",
        "column_name": "Name of the column",
        "column_position": "Position of column in table (1-based)",
        "data_type": "SQL data type of the column",
        "description": "Human-readable description of the column",
        "is_primary_key": "Whether this column is a primary key",
        "is_foreign_key": "Whether this column is a foreign key",
        "foreign_key_table": "Referenced table if foreign key",
        "dialectic_reference": "Reference to dialectical analysis round",
        "updated_at": "When this entry was last updated",
    }
    for col, comment in dd_columns.items():
        sql = f"ALTER TABLE {full_table} ALTER COLUMN {col} COMMENT '{comment}'"
        run_sql(client, sql, f"data_dictionary.{col}")

    return success, failed


def main():
    print("=" * 70)
    print("ShovelSense Delta Table Metadata Application")
    print("=" * 70)
    print(f"\nCatalog: {CATALOG}")
    print(f"Schema: {SCHEMA}")
    print(f"Warehouse: {WAREHOUSE_ID}")
    print(f"Profile: {PROFILE}")

    # Initialize client
    try:
        client = WorkspaceClient(profile=PROFILE)
        print("\nDatabricks client initialized successfully.")
    except Exception as e:
        print(f"\nERROR: Failed to initialize Databricks client: {e}")
        sys.exit(1)

    # Get table types to know which support column comments
    table_types = get_table_types(client)
    print(f"\nFound {len(table_types)} objects in schema.")

    # Apply table comments
    table_success, table_failed = apply_table_comments(client)

    # Apply table tags
    tag_success, tag_failed = apply_table_tags(client)

    # Apply column comments (only to tables, not views)
    col_success, col_failed, col_skipped = apply_column_comments(client, table_types)

    # Create data dictionary table
    dd_success, dd_failed = create_data_dictionary(client, table_types)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Table comments:   {table_success} succeeded, {table_failed} failed")
    print(f"Table tags:       {tag_success} succeeded, {tag_failed} failed")
    print(f"Column comments:  {col_success} succeeded, {col_failed} failed, {col_skipped} skipped (views)")
    print(f"Data dictionary:  {dd_success} columns inserted, {dd_failed} failed")

    if col_skipped > 0:
        print(f"\nNote: {col_skipped} column comments were skipped because DLT creates")
        print("materialized views, not tables. Column descriptions are now available in:")
        print(f"  - {CATALOG}.{SCHEMA}.data_dictionary (queryable table)")
        print("  - docs/pipeline-documentation.md")

    if table_failed > 0:
        print("\nSome table comments failed. Check permissions and table existence.")
        sys.exit(1)
    else:
        print("\nTable metadata applied successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
