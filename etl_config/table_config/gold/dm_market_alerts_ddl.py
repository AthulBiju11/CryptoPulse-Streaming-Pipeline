# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS cryptopulse_catalog.gold.dm_market_alerts (
# MAGIC   symbol STRING,
# MAGIC   alert_type STRING,
# MAGIC   price_change_pct DECIMAL(10,4),
# MAGIC   start_price DECIMAL(18,2),
# MAGIC   end_price DECIMAL(18,2),
# MAGIC   window_start TIMESTAMP,
# MAGIC   window_end TIMESTAMP,
# MAGIC   detected_at TIMESTAMP
# MAGIC )
# MAGIC USING DELTA;
