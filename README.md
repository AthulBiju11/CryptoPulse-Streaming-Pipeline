# CryptoPulse Streaming Pipeline 🚀

**CryptoPulse** is an end-to-end real-time data streaming pipeline designed to ingest, process, and analyze cryptocurrency trade data from Coinbase. It leverages the **Azure** cloud ecosystem for robust infrastructure and **Databricks** for high-performance extraction, transformation, and loading (ETL) using the Medallion Architecture.

## 🏗️ Architecture

![Architecture Diagram](https://mermaid.ink/img/pako:eNqNVMtu2zAQ_BWBTy3gA_RDc2hToC3qoCnakBwcW1RESqJIhSKNgn4N_fsupTix08Z9sDkyM9wd7q6QrJSCJPDq51oK9Ebes4q83-1L_LDfl7Dfb8r93-vN5vrt9e262GzK4rrc_irLzWpdlviFvM5e4J1kUsmUvK64Eoy_J2-4lEyq95y9Iq9kKqmS6A15VcqMvF69f4dXyWskf4F7yV9h_QruwT8gbyVn8q3gQpYScUBeYc2EvOGM4R35wN4qJtiDF1xx9hP6wL6R97CQgnF0k0IqmWBf8FdyLphC3ygueMIY-om8J5LCi_7E2R25wF4rLnmK78h7yYngCn3DXiqp0I-KCy4Zg37BXiip0E88f8d-4jli_x6d90rO0VeKC5Exhn6FviqpoJ94jthP_I7Yf0DnvZJz9I3iQmiMof-gvygpo594jthP_IHYf0znvZZz9I3iQmiMof-EfiupoZ94vpJ-4g9K-l84742co28VF0JjDP1X9FslDfQzzz-hn3j-lP53znuj5OhbxYXIGEP_Hf1OSQv9Is9P6BefP6X_g857K-foO8WFyBhDv0O_U9JBv_L8hH7l-VP6P-m8d3KOvlNciIwx9L_Q75X00G88P6HfeP6U_i86772co-8VFyJjDP1X9FslDfQzzz-hn3j-lP53znuj5OhbxYXIGEP_Hf1OSQv9Is9P6BefP6X_g857K-foO8WFyBhDv0O_U9JBv_L8hH7l-VP6P-m8d3KOvlNciIwx9L_Q75X00G88P6HfeP6U_i86772co-8VFyJjDP0v9AclA_Q7z9-h33n-H_qDkv1P9F8lI_QHz9-hP3j-H_qjkv1P9CclY_Qnz9-hP3n-H_qTkv1P9GclE_Rnzz-hP3v-n_qzkuNP9BclU_SXzj-hv3T-n_qrkuNP9DclM_Q3zz-hP3v-n_q7kuNP9A8lM_SPsH-F_qHkzCfc1YrPMeC25iX6oWSC_sE9F_QPJXf0v5QcfaP4HDFG0H_FPhX0XyV39I3ic0QYQf8N-1zQf5Xc0TeK696wT2dE1hT03yT39I3iQmiMkf6H3Cjp2f9CbpT07L9K7ukbxaXQD1V8T0lC3yj-oIoxgo6R_rGSlr5RXKAfqxgj6BjpHytp6RvFBf2DijGCjpH-sZKWe_pGccl4tIpPMeC8lQf6kZKOvlFciIwxdMy56BjpHytp6RvFBfaX_FvKD_lJyl77R_Ar9Q8oe-UVyK3qtiI-gY6Z8q6ekbxaXovSo2go6R_qmSnr5RXGkHVWwEHSP_pZKWvnn_L1DFRNAx8t8qaekbxaXoNxTfUtLTN4pL0W8ovqWkp28Ul6LfUHxLSU_fKC6FfqPiW0p6NjSK6_q_nf8Br41S3A)

---

## 📸 Project Visuals

### Real-Time Dashboard
*A view of the Databricks SQL Dashboard monitoring live crypto prices and market alerts.*

![Databricks SQL Dashboard](https://res.cloudinary.com/doet8xhyx/image/upload/v1767179444/IMG_5326_qo9ovh.png)

### Pipeline Execution
*Below is a snapshot of the Databricks Workflow executing the Medallion Architecture (Bronze -> Silver -> Gold).*

![Pipeline Execution - Databricks Workflow](https://res.cloudinary.com/doet8xhyx/image/upload/v1767179443/IMG_5328_didzt1.png)

---

## 🛠️ Infrastructure & Cloud Services 

This project integrates several key Azure services to create a scalable, production-grade data pipeline. Below is a detailed breakdown of each component and its role:

| Service | Architecture Component | Implementation Details |
| :--- | :--- | :--- |
| **Azure Event Hubs** | **Ingestion / Buffer** | Acts as the entry point for the pipeline. We provisioned a dedicated Namespace and a single Event Hub entity (`coinbase-raw-trades`). Configured with **1 Throughput Unit (TU)** and **1 Partition** to efficiently handle the streaming load from the producer while maintaining cost-effectiveness for our volume. |
| **Azure Container Registry (ACR)** | **Artifact Management** | Used to store and version-control our Docker images. The producer application was built locally and pushed to this private registry, ensuring secure and reliable deployment artifacts. |
| **Azure Container Instances (ACI)** | **Compute (Producer)** | Provides a serverless environment to run our producer. ACI pulls the Docker image directly from our ACR and runs it as a container group. This setup ensures our producer runs 24/7 without needing to manage underlying VMs. |
| **Azure Data Lake Storage Gen2 (ADLS)** | **Data Lake Storage** | Serves as the primary storage backend for our Lakehouse. We utilized a hierarchical namespace enabled storage account (`dbdeltalabstorageacct01`) to store all data files (Parquet/Delta) and checkpoints, offering fine-grained access control and limitless scalability. |
| **Azure Databricks** | **Processing & Analytics** | The heart of our ETL. We deployed a **Single Node Cluster** (Standard_D4s_v3) running **Databricks Runtime 16.4 LTS**. This environment executes our Spark Structured Streaming jobs and manages the Unity Catalog for data governance. |

---

## � Performance & Reliability

### Latency Characteristics
*   **End-to-End Latency**: Through testing, we observed a typical latency of **~10 seconds** from event generation to the Silver Layer under normal load.
*   **Heavy Load Handling**: During peak trading periods, latency can momentarily spike to **~1 minute**. This is due to the conscious architectural decision to use a cost-effective **Single Node (D4s_v3)** cluster. The system is designed to naturally buffer this backpressure and catch up without data loss.

### Operational Resilience
*   **Databricks Jobs**: The processing pipeline is orchestrated via Databricks Workflows configured with a **Continuous** trigger. 
*   **Self-Healing**: If the driver restarts or a transient failure occurs, the Continuous trigger ensures the job automatically restarts immediately, resuming processing exactly from the last checkpoint using Delta Lake's transactional guarantees.

---

## �📂 Repository Structure

```graphql
CryptoPulse-Streaming-Pipeline/
├── producer/
│   ├── producer.py            # Async Python script for Coinbase WS -> Event Hub
│   ├── Dockerfile             # Docker image definition for ACI
│   └── .env                   # Local configuration (GitIgnored)
│
├── etl_config/
│   ├── env_config/            # Catalog, Schema, and Volume DDLs
│   └── table_config/          # Delta Table definitions (Bronze/Silver/Gold)
│
├── etl_notebooks/
│   ├── bronze/                # Event Hubs extraction logic
│   ├── silver/                # Cleaning, JSON Parsing, Deduplication
│   └── gold/                  # Aggregations & Anomaly Detection logic
│       ├── dm_crypto_price_stats_load.py
│       └── dm_market_alerts_load.py
│
├── databricks/
│   └── dashboard_queries.sql  # SQL queries used for the Visualization Dashboard
│
└── reusable_components/       # Utilities (e.g., Secret Management)
```

---

## 🚀 Setup & Deployment

### 1. Prerequisites
- **Azure Subscription**: (Visual Studio Enterprise) Access to create Event Hubs, ACR, ACI, and Storage Accounts.
- **Databricks Workspace**: Unity Catalog enabled.

### 2. Infrastructure Setup
**Azure Config:**
- Create an Event Hub Namespace and Event Hub (`coinbase-raw-trades`).
- Note user: configured with **1 TU** and **1 Partition** for cost-efficiency.

**Security:**
- Secrets are managed via **Databricks Secret Scopes** (non-Key Vault).
- Create scope: `cryptopulse-scope`.
- Add secret: `eventhub-conn-string`.

### 3. Deploy Producer (Cloud Shell & ACR)
We utilized **Azure Cloud Shell** for a streamlined, ephemeral deployment process, ensuring a clean and consistent build environment.

**Steps followed:**
1.  **Environment Prep**: Opened Azure Cloud Shell and switched to the Visual Studio Enterprise subscription.
2.  **Code Access**: Cloned this repository into the ephemeral Cloud Shell session to retrieve the latest producer code.
    ```bash
    git clone https://github.com/AthulBiju11/CryptoPulse-Streaming-Pipeline.git
    cd CryptoPulse-Streaming-Pipeline
    ```
3.  **Build to Registry**: Used the `az acr build` command to build the Docker image directly in the Azure Container Registry (ACR), eliminating the need for a local Docker daemon.
    ```bash
    az acr build --registry <acr-name> --image cryptopulse-producer:v1 ./producer
    ```
4.  **Resilient Deployment (OnFailure Policy)**: Deployed the image to Azure Container Instances (ACI) with a **Restart Policy** of `OnFailure`. This ensures 24/7 reliability; if the producer crashes or encounters network issues, ACI automatically restarts the container to maintain the continuous data stream.
    ```bash
    az container create \
      --resource-group <rg-name> \
      --name cryptopulse-producer \
      --image <acr-name>.azurecr.io/cryptopulse-producer:v1 \
      --restart-policy OnFailure \
      --environment-variables EVENT_HUB_CONNECTION_STRING="<secret>"
    ```

### 4. Deploy Databricks Pipeline
**1. Initialize Catalog & Tables:**
Run the notebooks in `etl_config/` to create the managed catalog `cryptopulse_catalog` and the Medallion schemas (`bronze`, `silver`, `gold`).

**2. Launch Workflows:**
Create a Databricks Job with the following dependencies:
1.  **Task 1**: `bronze/coinbase_raw_trades_load` (Ingest)
2.  **Task 2**: `silver/fact_crypto_trades_load` (Depends on Task 1)
3.  **Task 3 & 4**: `gold/dm_crypto_price_stats_load` & `dm_market_alerts_load` (Depend on Task 2)

### 5. Visualization (Databricks SQL)
Use the queries in `databricks/dashboard_queries.sql` to build the **Real-Time Monitor**:
- **Price Trends**: 1-hour rolling window of Avg Price.
- **Volume Analysis**: Trading volume per asset.
- **Live Alerts**: Table showing detected `FLASH_CRASH` or `PRICE_SURGE` events.

