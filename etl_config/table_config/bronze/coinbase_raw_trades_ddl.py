# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS cryptopulse_catalog.bronze.coinbase_raw_trades (
# MAGIC   body STRING,
# MAGIC   partition STRING,
# MAGIC   offset STRING,
# MAGIC   sequenceNumber LONG,
# MAGIC   enqueuedTime TIMESTAMP,
# MAGIC   publisher STRING,
# MAGIC   partitionKey STRING,
# MAGIC   properties MAP<STRING,STRING>,
# MAGIC   systemProperties MAP<STRING,STRING>,
# MAGIC   bronze_ingestion_time TIMESTAMP
# MAGIC )
# MAGIC USING DELTA 
# MAGIC TBLPROPERTIES(
# MAGIC   'delta.enableChangeDataFeed' = 'true',
# MAGIC   'delta.autoOptimize.optimizeWrite' = 'true',
# MAGIC   'delta.autoOptimize.autoCompact' = 'true'
# MAGIC );
