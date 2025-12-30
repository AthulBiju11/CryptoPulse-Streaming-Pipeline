# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS cryptopulse_catalog.silver.fact_crypto_trades (
# MAGIC     trade_id STRING,
# MAGIC     symbol STRING,
# MAGIC     price DECIMAL(18,2),
# MAGIC     trade_size DECIMAL(18,8),
# MAGIC     side STRING,
# MAGIC     event_time TIMESTAMP,
# MAGIC     ingestion_time TIMESTAMP,
# MAGIC     load_timestamp TIMESTAMP
# MAGIC ) 
# MAGIC USING DELTA
# MAGIC PARTITIONED BY (symbol)
# MAGIC TBLPROPERTIES (
# MAGIC     'delta.enableChangeDataFeed' = 'true',
# MAGIC     'delta.autoOptimize.optimizeWrite' = 'true',
# MAGIC     'delta.autoOptimize.autoCompact' = 'true'
# MAGIC )
