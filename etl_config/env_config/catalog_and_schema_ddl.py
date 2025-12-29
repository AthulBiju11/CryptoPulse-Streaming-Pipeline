# Databricks notebook source
# MAGIC %sql
# MAGIC -- Schema Creation at Managed location for fine grain control
# MAGIC
# MAGIC CREATE CATALOG IF NOT EXISTS cryptopulse_catalog
# MAGIC MANAGED LOCATION 'abfss://metastore@dbdeltalabstorageacct01.dfs.core.windows.net/cryptopulse_catalog/'

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Creating the Medallion Schemas
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS cryptopulse_catalog.bronze;
# MAGIC CREATE SCHEMA IF NOT EXISTS cryptopulse_catalog.silver;
# MAGIC CREATE SCHEMA IF NOT EXISTS cryptopulse_catalog.gold;
