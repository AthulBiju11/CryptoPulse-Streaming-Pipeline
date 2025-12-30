# Databricks notebook source
from pyspark.sql.functions import col, window, first, last, current_timestamp, abs

checkpoint_path = "/Volumes/cryptopulse_catalog/gold/checkpoints/dm_market_alerts"

# COMMAND ----------

from pyspark.sql.functions import when, col

silver_stream = spark.readStream.table("cryptopulse_catalog.silver.fact_crypto_trades")

alerts_logic_df = (
    silver_stream.withWatermark("event_time","1 minute")
    .groupBy(
        col("symbol"),
        window(col("event_time"),"2 minutes","1 minute")
    )
    .agg(
        first("price").alias("start_price"),
        last("price").alias("end_price")
    )
    .withColumn(
        "price_change_pct",
        ((col("end_price") - col("start_price")) / col("start_price")) * 100
    )
    .filter(abs(col("price_change_pct")) >= 1.0)
    .select(
        col("symbol"),
        (col("price_change_pct") < 0).cast("string").alias("is_crash"),
        col("price_change_pct"),
        col("start_price"),
        col("end_price"),
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        current_timestamp().alias("detected_at")
    )
    .withColumn(
        "alert_type",
        when(col("is_crash") == "true", "FLASH_CRASH").otherwise("PRICE_SURGE")
    )
    .drop("is_crash")
)

# COMMAND ----------

(
    alerts_logic_df.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation",checkpoint_path)
    .toTable("cryptopulse_catalog.gold.dm_market_alerts")
)
