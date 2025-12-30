# Databricks notebook source
# DBTITLE 1,Imports
# Imports
import json
from pyspark.sql.functions import col, current_timestamp  

# COMMAND ----------

# DBTITLE 1,Configuration
connection_string = dbutils.secrets.get(scope="cryptopulse-scope", key="eventhub-conn-string")

startingEventPosition = {
 "offset": "-1", 
 "seqNo": -1,
 "enqueuedTime": None,
 "isInclusive": True
}

eh_conf = {
 'eventhubs.connectionString' : sc._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(connection_string),
 'eventhubs.startingPosition' : json.dumps(startingEventPosition) 
}

checkpoint_path = "/Volumes/cryptopulse_catalog/bronze/checkpoints/coinbase_raw_trades"

# COMMAND ----------

raw_df = spark.readStream \
    .format("eventhubs") \
    .options(**eh_conf) \
    .load()


coinbase_raw_trades_df = (
    raw_df.withColumn("body", col("body").cast("string"))
            .withColumn("bronze_ingestion_time",current_timestamp())
)

coinbase_raw_trades_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation",checkpoint_path) \
    .toTable("cryptopulse_catalog.bronze.coinbase_raw_trades")
