# Databricks notebook source
from pyspark.sql.functions import col,window,avg,max,min,sum,count

checkpoint_path = "/Volumes/cryptopulse_catalog/gold/checkpoints/dm_crypto_price_stats"

# COMMAND ----------

silver_stream = (
    spark.readStream
    .table("cryptopulse_catalog.silver.fact_crypto_trades")
)

gold_stats_df = (
    silver_stream.withWatermark("event_time","2 minutes")
    .groupBy(
        col("symbol"),
        window(col("event_time"),"5 minutes")
    )
    .agg(
        avg("price").alias("avg_price"),
        max("price").alias("max_price"),
        min("price").alias("min_price"),
        sum("trade_size").alias("total_trade_volume"),
        count("trade_id").alias("trade_count")
    )
    .select(
        col("symbol"),
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        "avg_price","max_price","min_price","total_trade_volume","trade_count"
    )
)

# COMMAND ----------

(
    gold_stats_df.writeStream
    .format("delta")
    .outputMode("complete")
    .option("checkpointLocation", checkpoint_path)
    .toTable("cryptopulse_catalog.gold.dm_crypto_price_stats")
)
