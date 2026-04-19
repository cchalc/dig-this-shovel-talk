# Databricks notebook source
"""
ShovelSense Spark Declarative Pipeline

Implements a medallion architecture (Bronze → Silver → Gold) for mining operations data.
Creates dimension and fact tables following Kimball star schema principles.

Data Model:
- Bronze: Raw ingestion from parquet files
- Silver: Cleaned, validated, enriched
- Gold: Dimension tables (dim_*) and Fact tables (fact_*)
"""
from pyspark import pipelines as dp
from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.sql.window import Window

# =============================================================================
# CONFIGURATION
# =============================================================================
# Get configuration from pipeline settings
catalog = spark.conf.get("catalog", "cjc_aws_workspace_catalog")
schema = spark.conf.get("schema", "shovelsense")
volume_path = spark.conf.get("volume_path", f"/Volumes/{catalog}/{schema}/raw_data")

# Grade cutoff for ore vs waste classification
CU_CUTOFF = 0.20

# =============================================================================
# BRONZE LAYER - Raw Ingestion
# =============================================================================

@dp.table(
    name="bronze_block_model",
    comment="Raw geological block model data ingested from parquet"
)
def bronze_block_model():
    """Ingest raw block model data."""
    return (
        spark.read.parquet(f"{volume_path}/block_model.parquet")
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_source_file", F.lit(f"{volume_path}/block_model.parquet"))
    )


@dp.table(
    name="bronze_shovels",
    comment="Raw shovel fleet master data"
)
def bronze_shovels():
    """Ingest raw shovel fleet data."""
    return (
        spark.read.parquet(f"{volume_path}/shovels.parquet")
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_source_file", F.lit(f"{volume_path}/shovels.parquet"))
    )


@dp.table(
    name="bronze_trucks",
    comment="Raw truck fleet master data"
)
def bronze_trucks():
    """Ingest raw truck fleet data."""
    return (
        spark.read.parquet(f"{volume_path}/trucks.parquet")
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_source_file", F.lit(f"{volume_path}/trucks.parquet"))
    )


@dp.table(
    name="bronze_bucket_measurements",
    comment="Raw XRF bucket measurement data from ShovelSense sensors"
)
def bronze_bucket_measurements():
    """Ingest raw XRF bucket measurements."""
    return (
        spark.read.parquet(f"{volume_path}/bucket_measurements.parquet")
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_source_file", F.lit(f"{volume_path}/bucket_measurements.parquet"))
    )


@dp.table(
    name="bronze_truck_loads",
    comment="Raw truck load data with diversion classifications"
)
def bronze_truck_loads():
    """Ingest raw truck load data."""
    return (
        spark.read.parquet(f"{volume_path}/truck_loads.parquet")
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_source_file", F.lit(f"{volume_path}/truck_loads.parquet"))
    )


@dp.table(
    name="bronze_shift_summaries",
    comment="Raw shift-level summary statistics"
)
def bronze_shift_summaries():
    """Ingest raw shift summaries."""
    return (
        spark.read.parquet(f"{volume_path}/shift_summaries.parquet")
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_source_file", F.lit(f"{volume_path}/shift_summaries.parquet"))
    )


# =============================================================================
# SILVER LAYER - Cleaned and Validated
# =============================================================================

@dp.table(
    name="silver_block_model",
    comment="Cleaned geological block model with derived classification fields"
)
@dp.expect_or_drop("valid_block_id", "block_id IS NOT NULL")
@dp.expect_or_drop("valid_cu_grade", "planned_cu_grade >= 0 AND planned_cu_grade <= 5")
def silver_block_model():
    """Clean and enrich block model data."""
    return (
        spark.read.table("bronze_block_model")
        .withColumn("is_ore", F.col("planned_cu_grade") >= CU_CUTOFF)
        .withColumn("grade_bin",
            F.when(F.col("planned_cu_grade") >= 1.0, "HIGH")
            .when(F.col("planned_cu_grade") >= 0.5, "MEDIUM")
            .when(F.col("planned_cu_grade") >= CU_CUTOFF, "LOW")
            .otherwise("WASTE")
        )
        .withColumn("block_volume_m3", F.lit(15 * 15 * 15))  # 15m block size assumption
    )


@dp.table(
    name="silver_shovels",
    comment="Cleaned shovel fleet data with parsed dates"
)
@dp.expect_or_drop("valid_shovel_id", "shovel_id IS NOT NULL")
def silver_shovels():
    """Clean shovel fleet data."""
    return (
        spark.read.table("bronze_shovels")
        .withColumn("commissioned_date", F.to_date("commissioned_date"))
        .withColumn("days_in_service",
            F.datediff(F.current_date(), F.col("commissioned_date")))
    )


@dp.table(
    name="silver_trucks",
    comment="Cleaned truck fleet data"
)
@dp.expect_or_drop("valid_truck_id", "truck_id IS NOT NULL")
def silver_trucks():
    """Clean truck fleet data."""
    return spark.read.table("bronze_trucks")


@dp.table(
    name="silver_bucket_measurements",
    comment="Cleaned XRF measurements with quality flags and parsed timestamps",
    cluster_by=["measurement_date"]
)
@dp.expect_or_drop("valid_measurement_id", "measurement_id IS NOT NULL")
@dp.expect_or_drop("valid_cu_grade", "cu_grade_pct >= 0")
@dp.expect_or_drop("valid_confidence", "xrf_confidence >= 0.5")
def silver_bucket_measurements():
    """Clean and enrich XRF bucket measurements."""
    return (
        spark.read.table("bronze_bucket_measurements")
        .withColumn("timestamp", F.to_timestamp("timestamp"))
        .withColumn("measurement_date", F.to_date("timestamp"))
        .withColumn("measurement_hour", F.hour("timestamp"))
        .withColumn("measurement_date_key",
            F.date_format("timestamp", "yyyyMMdd").cast("int"))
        .withColumn("is_high_confidence", F.col("xrf_confidence") >= 0.90)
        .withColumn("both_sensors_active",
            F.col("sensor_head_1_active") & F.col("sensor_head_2_active"))
        .withColumn("grade_category",
            F.when(F.col("cu_grade_pct") >= 1.0, "HIGH_GRADE")
            .when(F.col("cu_grade_pct") >= 0.5, "MEDIUM_GRADE")
            .when(F.col("cu_grade_pct") >= CU_CUTOFF, "LOW_GRADE")
            .otherwise("WASTE")
        )
    )


@dp.table(
    name="silver_truck_loads",
    comment="Cleaned truck loads with diversion analysis flags",
    cluster_by=["load_date"]
)
@dp.expect_or_drop("valid_load_id", "load_id IS NOT NULL")
@dp.expect_or_drop("valid_grade", "avg_cu_grade_pct >= 0")
def silver_truck_loads():
    """Clean and enrich truck load data."""
    return (
        spark.read.table("bronze_truck_loads")
        .withColumn("timestamp", F.to_timestamp("timestamp"))
        .withColumn("load_date", F.to_date("timestamp"))
        .withColumn("load_hour", F.hour("timestamp"))
        .withColumn("load_date_key",
            F.date_format("timestamp", "yyyyMMdd").cast("int"))
        .withColumn("shift",
            F.when(F.hour("timestamp").between(6, 17), "DAY")
            .otherwise("NIGHT"))
        .withColumn("day_of_week", F.dayofweek("timestamp"))
        .withColumn("is_weekend", F.dayofweek("timestamp").isin([1, 7]))
        .withColumn("is_diverted", F.col("diversion_type") != "ALIGNED")
        .withColumn("is_ore_recovery", F.col("diversion_type") == "ORE_FROM_WASTE")
        .withColumn("is_dilution_prevention", F.col("diversion_type") == "WASTE_FROM_ORE")
        .withColumn("grade_bin",
            F.when(F.col("avg_cu_grade_pct") >= 1.0, "HIGH")
            .when(F.col("avg_cu_grade_pct") >= 0.5, "MEDIUM")
            .when(F.col("avg_cu_grade_pct") >= CU_CUTOFF, "LOW")
            .otherwise("WASTE")
        )
        # Economic value estimate (simplified)
        .withColumn("estimated_cu_tonnes",
            F.col("payload_tonnes") * F.col("avg_cu_grade_pct") / 100)
    )


@dp.table(
    name="silver_shift_summaries",
    comment="Cleaned shift-level summaries"
)
def silver_shift_summaries():
    """Clean shift summary data."""
    return (
        spark.read.table("bronze_shift_summaries")
        .withColumn("date", F.to_date("date"))
        .withColumn("date_key", F.date_format("date", "yyyyMMdd").cast("int"))
    )


# =============================================================================
# GOLD LAYER - Dimension Tables
# =============================================================================

@dp.table(
    name="dim_shovels",
    comment="Shovel dimension table with equipment attributes"
)
def dim_shovels():
    """Create shovel dimension."""
    return (
        spark.read.table("silver_shovels")
        .select(
            F.col("shovel_id"),
            F.col("shovel_type"),
            F.col("bucket_capacity_m3"),
            F.col("minesense_equipped"),
            F.col("sensor_heads"),
            F.col("commissioned_date"),
            F.col("days_in_service"),
            F.current_timestamp().alias("_updated_at")
        )
    )


@dp.table(
    name="dim_trucks",
    comment="Truck dimension table with vehicle attributes"
)
def dim_trucks():
    """Create truck dimension."""
    return (
        spark.read.table("silver_trucks")
        .select(
            F.col("truck_id"),
            F.col("truck_model"),
            F.col("payload_capacity_tonnes"),
            F.col("fms_system"),
            F.current_timestamp().alias("_updated_at")
        )
    )


@dp.table(
    name="dim_block_model",
    comment="Block model dimension with geological attributes"
)
def dim_block_model():
    """Create block model dimension."""
    return (
        spark.read.table("silver_block_model")
        .select(
            F.col("block_id"),
            F.col("bench"),
            F.col("easting"),
            F.col("northing"),
            F.col("elevation"),
            F.col("planned_cu_grade"),
            F.col("planned_fe_grade"),
            F.col("planned_classification"),
            F.col("geological_domain"),
            F.col("is_dyke"),
            F.col("blast_movement_m"),
            F.col("is_ore"),
            F.col("grade_bin"),
            F.col("block_volume_m3"),
            F.current_timestamp().alias("_updated_at")
        )
    )


@dp.table(
    name="dim_date",
    comment="Date dimension for time-based analysis"
)
def dim_date():
    """Create date dimension covering the data range."""
    # Get date range from truck loads
    date_range = (
        spark.read.table("silver_truck_loads")
        .agg(
            F.min("load_date").alias("min_date"),
            F.max("load_date").alias("max_date")
        )
        .collect()[0]
    )

    min_date = date_range["min_date"]
    max_date = date_range["max_date"]

    # Generate date sequence
    return (
        spark.sql(f"""
            SELECT explode(sequence(
                to_date('{min_date}'),
                to_date('{max_date}'),
                interval 1 day
            )) AS date
        """)
        .withColumn("date_key", F.date_format("date", "yyyyMMdd").cast("int"))
        .withColumn("year", F.year("date"))
        .withColumn("quarter", F.quarter("date"))
        .withColumn("month", F.month("date"))
        .withColumn("month_name", F.date_format("date", "MMMM"))
        .withColumn("week_of_year", F.weekofyear("date"))
        .withColumn("day_of_month", F.dayofmonth("date"))
        .withColumn("day_of_week", F.dayofweek("date"))
        .withColumn("day_name", F.date_format("date", "EEEE"))
        .withColumn("is_weekend", F.dayofweek("date").isin([1, 7]))
        .withColumn("is_weekday", ~F.dayofweek("date").isin([1, 7]))
    )


# =============================================================================
# GOLD LAYER - Fact Tables
# =============================================================================

@dp.table(
    name="fact_bucket_measurements",
    comment="Fact table for XRF bucket measurements",
    cluster_by=["measurement_date_key"]
)
def fact_bucket_measurements():
    """Create bucket measurement fact table."""
    return (
        spark.read.table("silver_bucket_measurements")
        .select(
            # Keys
            F.col("measurement_id"),
            F.col("measurement_date_key"),
            F.col("shovel_id"),
            F.col("truck_id"),
            F.col("block_id"),
            # Timestamp
            F.col("timestamp"),
            F.col("measurement_date"),
            F.col("measurement_hour"),
            # Measures
            F.col("bucket_number"),
            F.col("cu_grade_pct"),
            F.col("fe_grade_pct"),
            F.col("zn_grade_ppm"),
            F.col("as_grade_ppm"),
            F.col("laser_fill_level_pct"),
            F.col("xrf_confidence"),
            # Flags
            F.col("sensor_head_1_active"),
            F.col("sensor_head_2_active"),
            F.col("both_sensors_active"),
            F.col("is_high_confidence"),
            F.col("grade_category")
        )
    )


@dp.table(
    name="fact_truck_loads",
    comment="Fact table for truck loads with diversion classification",
    cluster_by=["load_date_key"]
)
def fact_truck_loads():
    """Create truck load fact table."""
    return (
        spark.read.table("silver_truck_loads")
        .select(
            # Keys
            F.col("load_id"),
            F.col("load_date_key"),
            F.col("shovel_id"),
            F.col("truck_id"),
            F.col("block_id"),
            # Timestamp
            F.col("timestamp"),
            F.col("load_date"),
            F.col("load_hour"),
            F.col("shift"),
            F.col("day_of_week"),
            F.col("is_weekend"),
            # Measures
            F.col("n_buckets"),
            F.col("avg_cu_grade_pct"),
            F.col("avg_fe_grade_pct"),
            F.col("payload_tonnes"),
            F.col("cycle_time_minutes"),
            F.col("estimated_cu_tonnes"),
            # Classification
            F.col("planned_classification"),
            F.col("shovelsense_classification"),
            F.col("diversion_type"),
            F.col("destination"),
            F.col("grade_bin"),
            # Flags
            F.col("is_diverted"),
            F.col("is_ore_recovery"),
            F.col("is_dilution_prevention")
        )
    )


# =============================================================================
# GOLD LAYER - Aggregate Fact Tables
# =============================================================================

@dp.materialized_view(
    name="fact_daily_diversions",
    comment="Daily diversion statistics aggregated by shovel"
)
def fact_daily_diversions():
    """Aggregate daily diversion statistics."""
    return (
        spark.read.table("fact_truck_loads")
        .groupBy("load_date", "load_date_key", "shovel_id")
        .agg(
            F.count("*").alias("total_trucks"),
            F.sum(F.when(F.col("is_diverted"), 1).otherwise(0)).alias("diverted_trucks"),
            F.sum(F.when(F.col("is_ore_recovery"), 1).otherwise(0)).alias("ore_from_waste_count"),
            F.sum(F.when(F.col("is_dilution_prevention"), 1).otherwise(0)).alias("waste_from_ore_count"),
            F.avg("avg_cu_grade_pct").alias("avg_cu_grade"),
            F.sum("payload_tonnes").alias("total_tonnes"),
            F.sum("estimated_cu_tonnes").alias("total_cu_tonnes"),
            F.avg("cycle_time_minutes").alias("avg_cycle_time")
        )
        .withColumn("diversion_rate",
            F.col("diverted_trucks") / F.col("total_trucks"))
        .withColumn("ore_recovery_rate",
            F.col("ore_from_waste_count") / F.col("total_trucks"))
        .withColumn("dilution_prevention_rate",
            F.col("waste_from_ore_count") / F.col("total_trucks"))
    )


@dp.materialized_view(
    name="fact_classification_accuracy",
    comment="Classification accuracy metrics (confusion matrix) by date"
)
def fact_classification_accuracy():
    """Calculate classification accuracy metrics."""
    return (
        spark.read.table("fact_truck_loads")
        .groupBy("load_date", "load_date_key")
        .agg(
            F.count("*").alias("total_loads"),
            # True Positives: planned ORE, classified ORE
            F.sum(F.when(
                (F.col("planned_classification") == "ORE") &
                (F.col("shovelsense_classification") == "ORE"), 1
            ).otherwise(0)).alias("true_positive"),
            # True Negatives: planned WASTE, classified WASTE
            F.sum(F.when(
                (F.col("planned_classification") == "WASTE") &
                (F.col("shovelsense_classification") == "WASTE"), 1
            ).otherwise(0)).alias("true_negative"),
            # False Positives: planned WASTE, classified ORE (ore from waste)
            F.sum(F.when(
                (F.col("planned_classification") == "WASTE") &
                (F.col("shovelsense_classification") == "ORE"), 1
            ).otherwise(0)).alias("false_positive"),
            # False Negatives: planned ORE, classified WASTE (waste from ore)
            F.sum(F.when(
                (F.col("planned_classification") == "ORE") &
                (F.col("shovelsense_classification") == "WASTE"), 1
            ).otherwise(0)).alias("false_negative")
        )
        .withColumn("accuracy",
            (F.col("true_positive") + F.col("true_negative")) / F.col("total_loads"))
        .withColumn("precision_ore",
            F.col("true_positive") / (F.col("true_positive") + F.col("false_positive")))
        .withColumn("recall_ore",
            F.col("true_positive") / (F.col("true_positive") + F.col("false_negative")))
        .withColumn("f1_score",
            2 * F.col("precision_ore") * F.col("recall_ore") /
            (F.col("precision_ore") + F.col("recall_ore")))
    )


@dp.materialized_view(
    name="fact_grade_distribution",
    comment="Grade distribution statistics by geological domain"
)
def fact_grade_distribution():
    """Aggregate grade distribution by geological domain."""
    return (
        spark.read.table("dim_block_model")
        .groupBy("geological_domain", "grade_bin")
        .agg(
            F.count("*").alias("block_count"),
            F.avg("planned_cu_grade").alias("avg_cu_grade"),
            F.stddev("planned_cu_grade").alias("std_cu_grade"),
            F.min("planned_cu_grade").alias("min_cu_grade"),
            F.max("planned_cu_grade").alias("max_cu_grade"),
            F.sum("block_volume_m3").alias("total_volume_m3")
        )
    )


@dp.materialized_view(
    name="fact_sensor_performance",
    comment="XRF sensor performance metrics by shovel and date"
)
def fact_sensor_performance():
    """Aggregate sensor performance metrics."""
    return (
        spark.read.table("fact_bucket_measurements")
        .groupBy("measurement_date", "measurement_date_key", "shovel_id")
        .agg(
            F.count("*").alias("total_measurements"),
            F.avg("xrf_confidence").alias("avg_confidence"),
            F.min("xrf_confidence").alias("min_confidence"),
            F.max("xrf_confidence").alias("max_confidence"),
            F.sum(F.when(F.col("is_high_confidence"), 1).otherwise(0)).alias("high_confidence_count"),
            F.sum(F.when(F.col("both_sensors_active"), 1).otherwise(0)).alias("both_sensors_active_count"),
            F.sum(F.when(~F.col("sensor_head_1_active"), 1).otherwise(0)).alias("sensor_1_failures"),
            F.sum(F.when(~F.col("sensor_head_2_active"), 1).otherwise(0)).alias("sensor_2_failures")
        )
        .withColumn("high_confidence_rate",
            F.col("high_confidence_count") / F.col("total_measurements"))
        .withColumn("dual_sensor_rate",
            F.col("both_sensors_active_count") / F.col("total_measurements"))
        .withColumn("sensor_1_failure_rate",
            F.col("sensor_1_failures") / F.col("total_measurements"))
        .withColumn("sensor_2_failure_rate",
            F.col("sensor_2_failures") / F.col("total_measurements"))
    )


# =============================================================================
# SUMMARY VIEW
# =============================================================================

@dp.materialized_view(
    name="summary_overall_performance",
    comment="Overall pipeline performance summary"
)
def summary_overall_performance():
    """Create overall performance summary."""
    daily = spark.read.table("fact_daily_diversions")
    accuracy = spark.read.table("fact_classification_accuracy")

    daily_agg = daily.agg(
        F.sum("total_trucks").alias("total_trucks"),
        F.sum("diverted_trucks").alias("total_diversions"),
        F.sum("ore_from_waste_count").alias("total_ore_from_waste"),
        F.sum("waste_from_ore_count").alias("total_waste_from_ore"),
        F.sum("total_tonnes").alias("total_tonnes_processed"),
        F.sum("total_cu_tonnes").alias("total_cu_tonnes"),
        F.avg("diversion_rate").alias("avg_daily_diversion_rate")
    )

    accuracy_agg = accuracy.agg(
        F.avg("accuracy").alias("avg_accuracy"),
        F.avg("precision_ore").alias("avg_precision"),
        F.avg("recall_ore").alias("avg_recall"),
        F.avg("f1_score").alias("avg_f1")
    )

    return daily_agg.crossJoin(accuracy_agg)
