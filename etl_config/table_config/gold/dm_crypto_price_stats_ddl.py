# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS cryptopulse_catalog.gold.dm_crypto_price_stats(
# MAGIC   symbol STRING,
# MAGIC   window_start TIMESTAMP,
# MAGIC   window_end TIMESTAMP,
# MAGIC   avg_price DECIMAL(18,2),
# MAGIC   max_price DECIMAL(18,2),
# MAGIC   min_price DECIMAL(18,2),
# MAGIC   total_trade_volume DECIMAL(18,8),
# MAGIC   trade_count LONG
# MAGIC )
# MAGIC USING DELTA;
