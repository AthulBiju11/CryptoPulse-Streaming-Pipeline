# 🚀 CryptoPulse: Real-Time High-Frequency Streaming Pipeline

**An End-to-End Medallion Architecture for Cryptocurrency Market Monitoring & Anomaly Detection.**

![Dashboard Preview](images/dashboard_screenshot.png)  
*Live Monitoring Dashboard showing Price Trajectory, Market Sentiment, and Pipeline Latency.*

---

## 📖 Project Overview
CryptoPulse is a production-grade data engineering project designed to ingest, process, and analyze high-frequency cryptocurrency trade data in real-time. By leveraging a **Hybrid Cloud Architecture** (Local Python Microservices + Azure Cloud Infrastructure + Databricks), the pipeline transforms raw WebSocket "firehose" data into actionable market insights with sub-minute latency.

### The Business Case
In volatile markets, every second counts. CryptoPulse acts as a **Market Watchdog**, detecting "Flash Crashes" (price drops >1% in 2 minutes) and calculating real-time Volume-Weighted Average Prices (VWAP) to assist in high-frequency decision-making.

---

## 🏗️ Architecture
The project implements a **Medallion Architecture** managed via **Databricks Unity Catalog**.

![Pipeline Architecture](images/architecture_diagram.png)

1.  **Ingestion (The Producer):** A Python script using `asyncio` and `WebSockets` containerized with **Docker** and deployed on **Azure Container Instances (ACI)** for 24/7 uptime.
2.  **Buffering (The Broker):** **Azure Event Hubs** acts as the high-speed entry point, ensuring zero data loss during peak volatility.
3.  **Processing (Databricks):** A 4-stage **Spark Structured Streaming** workflow running on DBR 16.4 LTS.
4.  **Storage:** **Delta Lake** tables stored on **ADLS Gen2** with fine-grained access control via Unity Catalog.

---

## 🛠️ Tech Stack
*   **Languages:** Python, SQL, PySpark.
*   **Infrastructure:** Azure (ACI, Event Hubs, ACR, ADLS Gen2).
*   **Data Platform:** Databricks (Unity Catalog, Workflows, AI/BI Dashboards).
*   **DevOps:** Docker, GitHub Secret Scanning, Databricks-backed Secret Scopes.

---

## 📂 Repository Structure
Following enterprise standards, the repository separates DDL (Configuration) from ETL (Logic).

```text
CryptoPulse-Pipeline/
├── producer/
│   ├── producer.py             # Async WebSocket Producer
│   ├── Dockerfile              # Containerization for Azure ACI
│   └── .env                    # Local environment variables (Git Ignored)
├── databricks/
│   ├── etl_config/             # SQL DDL & Table Configurations
│   │   └── table_config/
│   │       ├── bronze/         # coinbase_raw_trades_config.sql
│   │       ├── silver/         # fact_crypto_trades_config.sql
│   │       └── gold/           # dm_crypto_price_stats_config.sql
│   ├── etl_notebooks/          # PySpark Streaming Logic
│   │       ├── bronze/         # coinbase_raw_trades_load.py
│   │       ├── silver/         # fact_crypto_trades_load.py
│   │       └── gold/           # dm_crypto_price_stats_load.py
└── README.md
