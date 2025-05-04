# NYC Taxi Data Pipeline with Mage and MongoDB

This project demonstrates a complete end-to-end data pipeline using Mage for orchestration and MongoDB for storage. The pipeline extracts data from `.csv` files, transforms it using pandas DataFrames within Mage blocks, and loads it into MongoDB collections.

## Project Overview

**Objective:** To build a modular, reproducible data pipeline that ingests NYC taxi data and persists it in MongoDB.

### Key Components

* **Data Source:** NYC Taxi `.csv` datasets
* **ETL Orchestration:** Mage (open-source data pipeline tool)
* **Data Transformation:** pandas-based operations inside Mage blocks
* **Data Storage:** MongoDB running in Docker container with persistent storage

## Workflow Steps

1. **Data Ingestion:** Raw `.csv` files are placed in the Mage pipeline's `data_loader` block.
2. **Transformation:** Data is cleaned, filtered, and structured in Mage using pandas DataFrames.
3. **Export to MongoDB:** Each transformed DataFrame is written to its own MongoDB collection under the `nyc_taxi` database.

### MongoDB Collections

Each DataFrame is stored as a separate collection:

* `taxi_fact_table`
* `dim_zone`
* `dim_datetime`

## Setup and Execution

1. Start MongoDB with persistent Docker volume:

```bash
docker volume create mongodb_data
docker run -d --name mongodb \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  --network mage_minio_net \
  mongo
```

2. Run Mage project locally.
3. Use Mage UI to trigger the pipeline and export data to MongoDB.

## Prerequisites

* Docker
* Mage (installed and initialized)
* MongoDB client (for data inspection)

## Output

* Cleaned and structured NYC Taxi data loaded into MongoDB collections.
* Reproducible and modular pipeline managed through Mage.

---

## Architecture Diagram

```
          +------------------+
          |   Uber CSV Files  |
          +------------------+
                    |
                    v
          +------------------+
          |  Mage Pipelines  |
          +------------------+
                    |
          +--------------------------+
          |  Data Cleaning & Mapping |
          +--------------------------+
                    |
                    v
          +------------------+
          |   MongoDB        |
          | (Docker Volume)  |
          +------------------+
```
