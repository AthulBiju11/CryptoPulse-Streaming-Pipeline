# Databricks notebook source
from pyspark.sql.functions import from_json,col,current_timestamp
from pyspark.sql.types import StructType,StructField,StringType

checkpoint_path = "/Volumes/cryptopulse_catalog/silver/checkpoints/fact_crypto_trades"

# COMMAND ----------

json_schema = StructType([
    StructField("trade_id", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("price", StringType(), True),
    StructField("last_size", StringType(), True),
    StructField("side", StringType(), True),
    StructField("time", StringType(), True),
    StructField("type", StringType(), True),
])

bronze_df = (spark.readStream
    .format("delta")
    .option("ignoreChanges", "true")
    .table("cryptopulse_catalog.bronze.coinbase_raw_trades")
)


silver_df_uncleaned = bronze_df.withColumn("json_data", from_json(col("body"), json_schema)) \
    .select(
        col("json_data.trade_id"),
        col("json_data.product_id").alias("symbol"),
        col("json_data.price").cast("decimal(18,2)").alias("price"),
        col("json_data.last_size").cast("decimal(18,8)").alias("trade_size"),
        col("json_data.side"),
        col("json_data.time").cast("timestamp").alias("event_time"),
        col("enqueuedTime").alias("ingestion_time"),  # Pass this through for latency calcs
        current_timestamp().alias("load_timestamp")
    ) \
    .filter(col("symbol").isNotNull())

silver_df = silver_df_uncleaned \
    .withWatermark("event_time", "1 minute") \
    .dropDuplicates(["trade_id"])
(
    silver_df.writeStream
    .format("delta")
    .outputMode("append")  # You can now use the faster 'append' mode
    .option("checkpointLocation", checkpoint_path)
    .toTable("cryptopulse_catalog.silver.fact_crypto_trades")
)
