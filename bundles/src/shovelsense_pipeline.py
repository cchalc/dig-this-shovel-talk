# Databricks notebook source
"""
ShovelSense Spark Declarative Pipeline

Implements a medallion architecture (Bronze → Silver → Gold) for mining operations data.
Creates dimension and fact tables following Kimball star schema principles.

Based on the ShovelSense ROI Dialectical Analysis, this pipeline processes data for a
heterogeneous copper porphyry deposit with the following characteristics:

Deposit Parameters:
- Cutoff grade: 0.32% Cu (from Round 1 Context Briefing)
- Average head grade: 0.45% Cu
- Mineralogy: ~80% chalcopyrite (CuFeS₂), ~20% bornite (Cu₅FeS₄)
- Geological zonation: Bornite core → Chalcopyrite zone → Pyrite halo

Key Metrics Tracked (from Dialectical Analysis):
- Diversion rate (~11%): Ore from Waste + Waste from Ore
- F1 score for classification accuracy
- Surface-volume correlation by geological domain
- XRF confidence and matrix effects

Data Model:
- Bronze: Raw ingestion from parquet files
- Silver: Cleaned, validated, enriched with domain terminology
- Gold: Dimension tables (dim_*) and Fact tables (fact_*)
"""
from pyspark import pipelines as dp
from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.sql.window import Window

# =============================================================================
# CONFIGURATION - Based on Dialectical Analysis Parameters
# =============================================================================
# Get configuration from pipeline settings
catalog = spark.conf.get("catalog", "cjc_aws_workspace_catalog")
schema = spark.conf.get("schema", "shovelsense")
volume_path = spark.conf.get("volume_path", f"/Volumes/{catalog}/{schema}/raw_data")

# Grade cutoff for ore vs waste classification
# From Round 1 Context Briefing: Cutoff grade 0.32% Cu
CU_CUTOFF = 0.32

# Economic parameters (from Round 3, Direction C)
COPPER_PRICE_PER_TONNE = 8820  # $4/lb
METALLURGICAL_RECOVERY = 0.85  # 85%

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
    comment="Cleaned geological block model with mineralogy and zonation data"
)
@dp.expect_or_drop("valid_block_id", "block_id IS NOT NULL")
@dp.expect_or_drop("valid_cu_grade", "planned_cu_grade >= 0 AND planned_cu_grade <= 5")
def silver_block_model():
    """
    Clean and enrich block model data.

    Includes new fields from dialectical analysis:
    - Mineralogy: chalcopyrite_pct, bornite_pct
    - Surface-volume correlation estimate by zone
    - Vein density classification
    """
    return (
        spark.read.table("bronze_block_model")
        .withColumn("is_ore", F.col("planned_cu_grade") >= CU_CUTOFF)
        .withColumn("grade_bin",
            F.when(F.col("planned_cu_grade") >= 1.0, "HIGH")
            .when(F.col("planned_cu_grade") >= 0.5, "MEDIUM")
            .when(F.col("planned_cu_grade") >= CU_CUTOFF, "LOW")
            .otherwise("WASTE")
        )
        .withColumn("block_volume_m3", F.lit(15 * 15 * 15))  # 15m block size
        # Mineralogy classification (from Round 1: 80% chalcopyrite, 20% bornite)
        .withColumn("mineralogy_class",
            F.when(F.col("bornite_pct") >= 50, "BORNITE_DOMINANT")
            .when(F.col("chalcopyrite_pct") >= 70, "CHALCOPYRITE_DOMINANT")
            .otherwise("MIXED")
        )
        # Surface-volume correlation quality indicator
        # From Round 1: This is the critical unknown for XRF value
        .withColumn("sv_correlation_quality",
            F.when(F.col("surface_volume_correlation") >= 0.70, "HIGH")
            .when(F.col("surface_volume_correlation") >= 0.50, "MODERATE")
            .otherwise("LOW")
        )
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
    comment="Cleaned XRF measurements with matrix effects and heterogeneity analysis",
    cluster_by=["measurement_date"]
)
@dp.expect_or_drop("valid_measurement_id", "measurement_id IS NOT NULL")
@dp.expect_or_drop("valid_cu_grade", "cu_grade_pct >= 0")
@dp.expect_or_drop("valid_confidence", "xrf_confidence >= 0.5")
def silver_bucket_measurements():
    """
    Clean and enrich XRF bucket measurements.

    From Round 1 (XRF Physics):
    - XRF penetration depth: <1mm (surface only)
    - Matrix effects: Fe absorbs Cu X-rays in chalcopyrite (30.5% Fe)
    - Heterogeneity error: Surface may not represent volume
    """
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
        # Matrix effect severity indicator
        # From Round 1: Chalcopyrite (30.5% Fe) absorbs Cu X-rays
        .withColumn("matrix_effect_severity",
            F.when(F.col("matrix_effect_factor") < 0.95, "HIGH")
            .when(F.col("matrix_effect_factor") < 0.98, "MODERATE")
            .otherwise("LOW")
        )
        # Measurement quality composite score
        .withColumn("measurement_quality_score",
            (F.col("xrf_confidence") * 0.5 +
             F.col("matrix_effect_factor") * 0.3 +
             F.when(F.col("both_sensors_active"), 0.2).otherwise(0.0))
        )
    )


@dp.table(
    name="silver_truck_loads",
    comment="Cleaned truck loads with diversion analysis and economic valuation",
    cluster_by=["load_date"]
)
@dp.expect_or_drop("valid_load_id", "load_id IS NOT NULL")
@dp.expect_or_drop("valid_grade", "avg_cu_grade_pct >= 0")
def silver_truck_loads():
    """
    Clean and enrich truck load data.

    From Round 3 (Economic Model):
    - Value per 0.01% grade improvement: $7.2M/year
    - Copper price: $8,820/tonne ($4/lb)
    - Metallurgical recovery: 85%
    """
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
        # Economic value estimates (from Round 3, Direction C)
        # Copper value: tonnes * grade * recovery * price
        .withColumn("estimated_cu_value_usd",
            F.col("payload_tonnes") *
            F.col("avg_cu_grade_pct") / 100 *
            F.lit(METALLURGICAL_RECOVERY) *
            F.lit(COPPER_PRICE_PER_TONNE)
        )
        # Surface-volume correlation quality for this load
        .withColumn("sv_correlation_quality",
            F.when(F.col("surface_volume_correlation") >= 0.70, "HIGH")
            .when(F.col("surface_volume_correlation") >= 0.50, "MODERATE")
            .otherwise("LOW")
        )
        # XRF reliability indicator
        .withColumn("xrf_reliability",
            F.when(
                (F.col("avg_xrf_confidence") >= 0.90) &
                (F.col("surface_volume_correlation") >= 0.60),
                "HIGH"
            ).when(
                (F.col("avg_xrf_confidence") >= 0.80) &
                (F.col("surface_volume_correlation") >= 0.45),
                "MODERATE"
            ).otherwise("LOW")
        )
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
    comment="Block model dimension with mineralogy and XRF suitability indicators"
)
def dim_block_model():
    """
    Create block model dimension.

    Includes new fields from dialectical analysis:
    - Mineralogy (chalcopyrite/bornite)
    - Surface-volume correlation (key XRF accuracy predictor)
    - Vein density (affects heterogeneity error)
    """
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
            # New mineralogy fields (from Round 1: 80% chalcopyrite, 20% bornite)
            F.col("chalcopyrite_pct"),
            F.col("bornite_pct"),
            F.col("mineralogy_class"),
            # Surface-volume correlation (from Round 1: the critical unknown)
            F.col("surface_volume_correlation"),
            F.col("sv_correlation_quality"),
            # Vein density and nugget effect
            F.col("nugget_effect_variance"),
            F.col("vein_density_class"),
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
    comment="Fact table for XRF bucket measurements with matrix effect analysis",
    cluster_by=["measurement_date_key"]
)
def fact_bucket_measurements():
    """
    Create bucket measurement fact table.

    From Round 1 (XRF Physics):
    - Matrix effects: Fe absorbs Cu X-rays (chalcopyrite has 30.5% Fe)
    - Heterogeneity error: Surface may not represent volume
    """
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
            # Matrix effect analysis (from Round 1)
            F.col("matrix_effect_factor"),
            F.col("matrix_effect_severity"),
            F.col("measurement_quality_score"),
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
    comment="Fact table for truck loads with diversion classification and XRF quality metrics",
    cluster_by=["load_date_key"]
)
def fact_truck_loads():
    """
    Create truck load fact table.

    Includes fields from dialectical analysis:
    - geological_domain: Zone-based classification for stratified accuracy analysis
    - surface_volume_correlation: Key unknown from Round 1
    - avg_xrf_confidence: Sensor reliability indicator
    - estimated_cu_value_usd: Economic impact per load (Round 3)
    """
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
            # XRF quality metrics (from dialectical analysis)
            F.col("avg_xrf_confidence"),
            F.col("surface_volume_correlation"),
            F.col("sv_correlation_quality"),
            F.col("xrf_reliability"),
            # Geological context
            F.col("geological_domain"),
            # Economic value (from Round 3, Direction C)
            F.col("estimated_cu_value_usd"),
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


@dp.materialized_view(
    name="fact_domain_classification_accuracy",
    comment="Classification accuracy by geological domain - key for evaluating zone-dependent XRF value"
)
def fact_domain_classification_accuracy():
    """
    Classification accuracy stratified by geological domain.

    From Round 1 Determinate Negation:
    "The surface-volume correlation may be low, but 'low' is not 'zero.'
    And even low correlation can have positive expected value if the
    decision problem is structured correctly."

    From Round 2 Direction D:
    "The 80/20 chalcopyrite/bornite split suggests XRF accuracy may vary
    spatially. A pilot could test this."
    """
    return (
        spark.read.table("fact_truck_loads")
        .groupBy("geological_domain")
        .agg(
            F.count("*").alias("total_loads"),
            # True Positives
            F.sum(F.when(
                (F.col("planned_classification") == "ORE") &
                (F.col("shovelsense_classification") == "ORE"), 1
            ).otherwise(0)).alias("true_positive"),
            # True Negatives
            F.sum(F.when(
                (F.col("planned_classification") == "WASTE") &
                (F.col("shovelsense_classification") == "WASTE"), 1
            ).otherwise(0)).alias("true_negative"),
            # False Positives (ore from waste)
            F.sum(F.when(
                (F.col("planned_classification") == "WASTE") &
                (F.col("shovelsense_classification") == "ORE"), 1
            ).otherwise(0)).alias("false_positive"),
            # False Negatives (waste from ore)
            F.sum(F.when(
                (F.col("planned_classification") == "ORE") &
                (F.col("shovelsense_classification") == "WASTE"), 1
            ).otherwise(0)).alias("false_negative"),
            # Surface-volume correlation stats
            F.avg("surface_volume_correlation").alias("avg_surface_volume_corr"),
            F.avg("avg_xrf_confidence").alias("avg_xrf_confidence"),
            # Economic impact
            F.sum("estimated_cu_value_usd").alias("total_cu_value_usd")
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
        .withColumn("diversion_rate",
            (F.col("false_positive") + F.col("false_negative")) / F.col("total_loads"))
    )


@dp.materialized_view(
    name="fact_sv_correlation_analysis",
    comment="Surface-volume correlation analysis - the key unknown from Round 1"
)
def fact_sv_correlation_analysis():
    """
    Analyze surface-volume correlation and its impact on classification.

    From Round 1 Context Briefing:
    "The relationship between multi-surface XRF readings and true
    volumetric grade of a heterogeneous bucket load is NOT
    well-characterized in published literature."

    This view helps answer: Does higher surface-volume correlation
    lead to better classification accuracy?
    """
    return (
        spark.read.table("fact_truck_loads")
        .withColumn("sv_corr_bin",
            F.when(F.col("surface_volume_correlation") >= 0.70, "0.70-1.00")
            .when(F.col("surface_volume_correlation") >= 0.55, "0.55-0.70")
            .when(F.col("surface_volume_correlation") >= 0.40, "0.40-0.55")
            .otherwise("0.00-0.40")
        )
        .groupBy("sv_corr_bin")
        .agg(
            F.count("*").alias("total_loads"),
            F.sum(F.when(F.col("diversion_type") == "ALIGNED", 1).otherwise(0)).alias("correct_classifications"),
            F.sum(F.when(F.col("is_ore_recovery"), 1).otherwise(0)).alias("ore_from_waste"),
            F.sum(F.when(F.col("is_dilution_prevention"), 1).otherwise(0)).alias("waste_from_ore"),
            F.avg("avg_xrf_confidence").alias("avg_xrf_confidence"),
            F.avg("surface_volume_correlation").alias("avg_sv_correlation"),
            F.sum("estimated_cu_value_usd").alias("total_cu_value_usd")
        )
        .withColumn("accuracy_rate",
            F.col("correct_classifications") / F.col("total_loads"))
        .withColumn("diversion_rate",
            1 - F.col("accuracy_rate"))
    )


# =============================================================================
# SUMMARY VIEW
# =============================================================================

@dp.materialized_view(
    name="summary_overall_performance",
    comment="Overall performance summary with economic metrics aligned to dialectical analysis"
)
def summary_overall_performance():
    """
    Create overall performance summary.

    Key metrics from Round 3 (Economic Model):
    - Total copper value processed
    - Required grade improvement for breakeven (0.033% Cu for ShovelSense)
    - Value per 0.01% grade improvement: $7.2M/year

    From Round 1 Context Briefing:
    - Target diversion rate: ~11%
    - Ore from Waste: ~6.4%
    - Waste from Ore: ~4.7%
    """
    daily = spark.read.table("fact_daily_diversions")
    accuracy = spark.read.table("fact_classification_accuracy")
    truck_loads = spark.read.table("fact_truck_loads")

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

    # Economic value metrics
    economic_agg = truck_loads.agg(
        F.sum("estimated_cu_value_usd").alias("total_cu_value_usd"),
        F.avg("avg_cu_grade_pct").alias("avg_head_grade_pct"),
        F.avg("surface_volume_correlation").alias("avg_sv_correlation"),
        F.avg("avg_xrf_confidence").alias("avg_xrf_confidence")
    )

    return daily_agg.crossJoin(accuracy_agg).crossJoin(economic_agg)
