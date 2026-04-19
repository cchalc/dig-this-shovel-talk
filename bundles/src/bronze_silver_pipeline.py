# Databricks notebook source
# MAGIC %md
# MAGIC # ShovelSense Bronze-Silver Pipeline
# MAGIC
# MAGIC Ingests raw parquet data from volumes and creates bronze/silver tables.
# MAGIC
# MAGIC ## Data Flow
# MAGIC ```
# MAGIC Volume (raw_data/)
# MAGIC     ├── block_model.parquet      → bronze_block_model      → silver_block_model
# MAGIC     ├── shovels.parquet          → bronze_shovels          → silver_shovels
# MAGIC     ├── trucks.parquet           → bronze_trucks           → silver_trucks
# MAGIC     ├── bucket_measurements.parquet → bronze_bucket_measurements → silver_bucket_measurements
# MAGIC     ├── truck_loads.parquet      → bronze_truck_loads      → silver_truck_loads
# MAGIC     └── shift_summaries.parquet  → bronze_shift_summaries  → silver_shift_summaries
# MAGIC ```

# COMMAND ----------

import dlt
from pyspark.sql import functions as F
from pyspark.sql.types import *

# Configuration
catalog = spark.conf.get("catalog", "ai_dev_kit")
schema = spark.conf.get("schema", "shovelsense")
volume_path = spark.conf.get("volume_path", f"/Volumes/{catalog}/{schema}/raw_data")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Bronze Layer: Raw Ingestion

# COMMAND ----------

@dlt.table(
    name="bronze_block_model",
    comment="Raw geological block model data"
)
def bronze_block_model():
    return spark.read.parquet(f"{volume_path}/block_model.parquet")


@dlt.table(
    name="bronze_shovels",
    comment="Raw shovel fleet data"
)
def bronze_shovels():
    return spark.read.parquet(f"{volume_path}/shovels.parquet")


@dlt.table(
    name="bronze_trucks",
    comment="Raw truck fleet data"
)
def bronze_trucks():
    return spark.read.parquet(f"{volume_path}/trucks.parquet")


@dlt.table(
    name="bronze_bucket_measurements",
    comment="Raw XRF bucket measurements"
)
def bronze_bucket_measurements():
    return spark.read.parquet(f"{volume_path}/bucket_measurements.parquet")


@dlt.table(
    name="bronze_truck_loads",
    comment="Raw truck load data with diversions"
)
def bronze_truck_loads():
    return spark.read.parquet(f"{volume_path}/truck_loads.parquet")


@dlt.table(
    name="bronze_shift_summaries",
    comment="Raw shift-level summaries"
)
def bronze_shift_summaries():
    return spark.read.parquet(f"{volume_path}/shift_summaries.parquet")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver Layer: Cleaned and Enriched

# COMMAND ----------

@dlt.table(
    name="silver_block_model",
    comment="Cleaned geological block model with derived fields"
)
@dlt.expect_or_drop("valid_cu_grade", "planned_cu_grade >= 0 AND planned_cu_grade <= 5")
@dlt.expect_or_drop("valid_block_id", "block_id IS NOT NULL")
def silver_block_model():
    return (
        dlt.read("bronze_block_model")
        .withColumn("is_ore", F.col("planned_cu_grade") >= 0.20)
        .withColumn("grade_bin",
            F.when(F.col("planned_cu_grade") >= 1.0, "HIGH")
            .when(F.col("planned_cu_grade") >= 0.5, "MEDIUM")
            .when(F.col("planned_cu_grade") >= 0.2, "LOW")
            .otherwise("WASTE")
        )
    )


@dlt.table(
    name="silver_shovels",
    comment="Cleaned shovel fleet data"
)
@dlt.expect_or_drop("valid_shovel_id", "shovel_id IS NOT NULL")
def silver_shovels():
    return (
        dlt.read("bronze_shovels")
        .withColumn("commissioned_date", F.to_date("commissioned_date"))
    )


@dlt.table(
    name="silver_trucks",
    comment="Cleaned truck fleet data"
)
@dlt.expect_or_drop("valid_truck_id", "truck_id IS NOT NULL")
def silver_trucks():
    return dlt.read("bronze_trucks")


@dlt.table(
    name="silver_bucket_measurements",
    comment="Cleaned XRF measurements with quality flags"
)
@dlt.expect_or_drop("valid_measurement", "measurement_id IS NOT NULL")
@dlt.expect_or_drop("valid_cu_grade", "cu_grade_pct >= 0")
@dlt.expect_or_drop("valid_confidence", "xrf_confidence >= 0.5")
def silver_bucket_measurements():
    return (
        dlt.read("bronze_bucket_measurements")
        .withColumn("timestamp", F.to_timestamp("timestamp"))
        .withColumn("measurement_date", F.to_date("timestamp"))
        .withColumn("measurement_hour", F.hour("timestamp"))
        .withColumn("is_high_confidence", F.col("xrf_confidence") >= 0.90)
        .withColumn("both_sensors_active",
            F.col("sensor_head_1_active") & F.col("sensor_head_2_active"))
    )


@dlt.table(
    name="silver_truck_loads",
    comment="Cleaned truck loads with diversion analysis"
)
@dlt.expect_or_drop("valid_load", "load_id IS NOT NULL")
@dlt.expect_or_drop("valid_grade", "avg_cu_grade_pct >= 0")
def silver_truck_loads():
    return (
        dlt.read("bronze_truck_loads")
        .withColumn("timestamp", F.to_timestamp("timestamp"))
        .withColumn("load_date", F.to_date("timestamp"))
        .withColumn("load_hour", F.hour("timestamp"))
        .withColumn("shift",
            F.when(F.hour("timestamp").between(6, 17), "DAY")
            .otherwise("NIGHT"))
        .withColumn("is_diverted", F.col("diversion_type") != "ALIGNED")
        .withColumn("is_ore_recovery", F.col("diversion_type") == "ORE_FROM_WASTE")
        .withColumn("is_dilution_prevention", F.col("diversion_type") == "WASTE_FROM_ORE")
        .withColumn("grade_bin",
            F.when(F.col("avg_cu_grade_pct") >= 1.0, "HIGH")
            .when(F.col("avg_cu_grade_pct") >= 0.5, "MEDIUM")
            .when(F.col("avg_cu_grade_pct") >= 0.2, "LOW")
            .otherwise("WASTE")
        )
    )


@dlt.table(
    name="silver_shift_summaries",
    comment="Cleaned shift summaries"
)
def silver_shift_summaries():
    return (
        dlt.read("bronze_shift_summaries")
        .withColumn("date", F.to_date("date"))
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold Layer: Aggregated Analytics

# COMMAND ----------

@dlt.table(
    name="gold_daily_diversions",
    comment="Daily diversion statistics by shovel"
)
def gold_daily_diversions():
    return (
        dlt.read("silver_truck_loads")
        .groupBy("load_date", "shovel_id")
        .agg(
            F.count("*").alias("total_trucks"),
            F.sum(F.when(F.col("is_diverted"), 1).otherwise(0)).alias("diverted_trucks"),
            F.sum(F.when(F.col("is_ore_recovery"), 1).otherwise(0)).alias("ore_from_waste"),
            F.sum(F.when(F.col("is_dilution_prevention"), 1).otherwise(0)).alias("waste_from_ore"),
            F.avg("avg_cu_grade_pct").alias("avg_cu_grade"),
            F.sum("payload_tonnes").alias("total_tonnes")
        )
        .withColumn("diversion_rate", F.col("diverted_trucks") / F.col("total_trucks"))
    )


@dlt.table(
    name="gold_classification_accuracy",
    comment="Classification accuracy metrics"
)
def gold_classification_accuracy():
    loads = dlt.read("silver_truck_loads")

    return (
        loads
        .groupBy("load_date")
        .agg(
            F.count("*").alias("total_loads"),
            # True Positives: planned ORE, classified ORE
            F.sum(F.when(
                (F.col("planned_classification") == "ORE") &
                (F.col("shovelsense_classification") == "ORE"), 1
            ).otherwise(0)).alias("true_positive_ore"),
            # True Negatives: planned WASTE, classified WASTE
            F.sum(F.when(
                (F.col("planned_classification") == "WASTE") &
                (F.col("shovelsense_classification") == "WASTE"), 1
            ).otherwise(0)).alias("true_negative_waste"),
            # False Positives: planned WASTE, classified ORE
            F.sum(F.when(
                (F.col("planned_classification") == "WASTE") &
                (F.col("shovelsense_classification") == "ORE"), 1
            ).otherwise(0)).alias("false_positive"),
            # False Negatives: planned ORE, classified WASTE
            F.sum(F.when(
                (F.col("planned_classification") == "ORE") &
                (F.col("shovelsense_classification") == "WASTE"), 1
            ).otherwise(0)).alias("false_negative")
        )
        .withColumn("accuracy",
            (F.col("true_positive_ore") + F.col("true_negative_waste")) / F.col("total_loads"))
        .withColumn("precision_ore",
            F.col("true_positive_ore") / (F.col("true_positive_ore") + F.col("false_positive")))
        .withColumn("recall_ore",
            F.col("true_positive_ore") / (F.col("true_positive_ore") + F.col("false_negative")))
    )


@dlt.table(
    name="gold_grade_distribution",
    comment="Grade distribution by geological domain"
)
def gold_grade_distribution():
    blocks = dlt.read("silver_block_model")

    return (
        blocks
        .groupBy("geological_domain", "grade_bin")
        .agg(
            F.count("*").alias("block_count"),
            F.avg("planned_cu_grade").alias("avg_cu_grade"),
            F.stddev("planned_cu_grade").alias("std_cu_grade"),
            F.min("planned_cu_grade").alias("min_cu_grade"),
            F.max("planned_cu_grade").alias("max_cu_grade")
        )
    )
