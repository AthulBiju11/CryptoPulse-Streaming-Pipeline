# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE VOLUME IF NOT EXISTS cryptopulse_catalog.bronze.checkpoints;
# MAGIC
# MAGIC CREATE VOLUME IF NOT EXISTS cryptopulse_catalog.silver.checkpoints;
# MAGIC
# MAGIC CREATE VOLUME IF NOT EXISTS cryptopulse_catalog.gold.checkpoints;
