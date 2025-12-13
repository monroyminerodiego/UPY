# VMI Project 3: Event-Driven Architecture with Airflow & Kafka

**Technical Implementation Report**

| **Context** | **Details** |
| :--- | :--- |
| **Institution** | Universidad Politécnica de Yucatán |
| **Course** | Visual Modeling for Information (9th Quarter) |
| **Developer** | Diego Monroy |
| **Focus** | Real-time ETL, Streaming, and Visualization |

-----

## 1\. Executive Summary

This project establishes a robust **Event-Driven Data Engineering Platform** designed to ingest, process, and visualize real-time data streams. By integrating **Apache Kafka** for high-throughput messaging and **Apache Airflow** for workflow orchestration, the system simulates and analyzes complex scenarios such as urban environmental monitoring and e-commerce user behavior. The architecture is fully containerized using Docker, ensuring reproducibility, and culminates in a Flask-based web interface for interactive data exploration.

### Core Capabilities

  * **Streaming Backbone:** Implementation of Confluent Kafka for scalable event ingestion.
  * **Orchestration Engine:** Utilization of Apache Airflow (v3.1.3) to schedule and monitor ELT/ETL tasks.
  * **Multi-Domain Processing:** Simultaneous handling of distinct data domains (Urban Sensors, Retail, Transportation).
  * **Visual Analytics:** Custom web application using Bokeh for dynamic, interactive plotting.
  * **Infrastructure as Code:** Full service orchestration via Docker Compose.
  * **Data Governance:** Enforcement of data contracts via Confluent Schema Registry.

-----

## 2\. Technology Stack

The system relies on a modern Python-centric stack, orchestrated within a Docker environment.

### Infrastructure & Backend

  * **Runtime:** Python 3.11
  * **Containerization:** Docker & Docker Compose
  * **Streaming:** Confluent Kafka (Kraft mode), Kafka Connect, Schema Registry
  * **Orchestration:** Apache Airflow 3.1.3 (Scheduler, Triggerer, DAG Processor)
  * **Persistence:** PostgreSQL 16 (Metadata), Local Volume Storage (Data Lake)

### Application & Analysis Layer

  * **Web Framework:** Flask 3.1.2
  * **Visualization:** Bokeh 3.8.1, Matplotlib 3.10.7
  * **Data Manipulation:** Pandas 2.3.3, NumPy 2.3.5
  * **Task Queue:** Celery 5.5.3 (Airflow Executor support)

-----

## 3\. System Architecture

The architecture is divided into four logical tiers: the **Network Layer**, **Streaming Layer**, **Orchestration Layer**, and **Presentation Layer**.

```mermaid
graph TD
    subgraph "Docker Network (airflow-net)"
        direction TB
        
        subgraph "Streaming Ecosystem"
            K[Kafka Broker :9092]
            SR[Schema Registry :8081]
            KC[Kafka Connect :8083]
            K --> SR
            K --> KC
        end

        subgraph "Orchestration (Airflow)"
            AS[API Server]
            SCH[Scheduler]
            DP[DAG Processor]
            TR[Triggerer]
            DB[(Postgres)]
            
            SCH --> DB
            AS --> DB
            DP --> DB
        end

        subgraph "ETL Workflows"
            DAG1(Urban Sensors ELT)
            DAG2(Product Events ETL)
            DAG3(Transport ETL)
        end

        subgraph "Data Persistence"
            VOL[/Shared Volume /data/]
            RAW[Raw Data]
            PROC[Processed Data]
            ANL[Analytics]
            VOL --- RAW
            VOL --- PROC
            VOL --- ANL
        end

        subgraph "Frontend"
            WEB[Flask Dashboard :5200]
        end

        K --> DAG1
        K --> DAG2
        K --> DAG3
        DAG1 --> VOL
        DAG2 --> VOL
        DAG3 --> VOL
        VOL --> WEB
    end
```

-----

## 4\. Service Catalog

The infrastructure is composed of the following microservices defined in `docker-compose.yml`:

### The Streaming Ecosystem

  * **Kafka Broker (`kafka`):** The central nervous system. Listens on internal port `9092` and external `29092`. It manages topics like `urban-sensors` and `product-events` with a single-partition configuration for this deployment.
  * **Schema Registry (`schema-registry`):** Listens on `8081`. It acts as the guardian of data structure, managing Avro schemas to ensure producers and consumers speak the same language.
  * **Kafka Connect (`kafka-connect`):** Listens on `8083`. Prepared for integration with external sinks/sources.

### The Orchestration Ecosystem (Airflow)

  * **Scheduler:** The heartbeat of the system. Triggers tasks and manages dependencies.
  * **API Server (`:8080`):** Exposes the REST interface for the Airflow UI and external triggers.
  * **DAG Processor:** Parses Python files in `dags/` to serialize workflow definitions into the metadata database.
  * **Triggerer:** Optimizes resource usage by handling asynchronous, deferrable tasks.
  * **PostgreSQL (`postgres`):** The metadata store for Airflow, tracking the state of every task instance.

### The Presentation Ecosystem

  * **Web Dashboard (`web-dashboard`):** A custom Flask application running on port `5200`. It mounts the shared `/data` volume to visualize processed CSVs using Bokeh.

-----

## 5\. Deployment Guide

### System Preparation

Ensure your environment meets these baselines:

  * **OS:** Linux, macOS, or Windows (WSL2 recommended).
  * **Resources:** Minimum 4GB RAM, 10GB Disk.
  * **Tools:** Docker Engine and Docker Compose installed.

### Configuration Strategy

1.  **Project Root:** Create a `.env` file for global variables.
    ```env
    AIRFLOW_UID=50000
    MOCKAROO_API=your_api_key  # Optional for data gen
    ```
2.  **Airflow Context:** Create `airflow/.env` for executor settings.
    ```env
    AIRFLOW__CORE__EXECUTOR=LocalExecutor
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
    ```

### Execution

To launch the entire stack in detached mode:

```bash
cd /path/to/project
docker compose up -d
```

### Access Points

Once the stack is healthy (verify with `docker compose ps`), access the services via:

| Interface | Address | Credentials |
| :--- | :--- | :--- |
| **Workflow UI** | `http://localhost:8080` | `airflow` / `airflow` |
| **Dashboards** | `http://localhost:5200` | *Public* |
| **Schema Registry** | `http://localhost:8081` | *Public* |
| **Kafka Broker** | `localhost:29092` | *No Auth* |

-----

## 6\. Data Workflows (ETL)

The system operates three distinct data pipelines designed to demonstrate different facets of data engineering.

### 🏙️ Workflow A: Urban Environmental Monitoring

  * **ID:** `VMI_URBAN_SENSORS_ELT`
  * **Cadence:** Hourly
  * **Process:**
    1.  **Ingest:** Simulates noise, pollution, and traffic data; pushes to Kafka topic `urban-sensors`.
    2.  **Process:** Consumes the stream; aggregates readings by timestamp and city zone.
    3.  **Analytics:** Computes Pollution Index and Noise Levels.
    4.  **Persist:** Updates `data/processed/urban_sensors_processed.csv`.

### 🛒 Workflow B: E-Commerce Funnel Analysis

  * **ID:** `VMI_PRODUCT_EVENTS_ETL`
  * **Cadence:** Hourly
  * **Process:**
    1.  **Ingest:** Generates user events (View, Cart, Purchase) for retail products.
    2.  **Transform:** Classifies sessions and maps user journeys.
    3.  **Analytics:** Calculates Conversion Rates (Funnel) and Category KPIs.
    4.  **Persist:** Generates clean datasets and specific KPI CSV files.

### 🚌 Workflow C: Transport Logistics

  * **ID:** `VMI_001`
  * **Cadence:** Manual / On-Demand
  * **Process:** Connects to Mockaroo to fetch transport logs, streams them through Kafka, and outputs a consolidated CSV.

-----

## 7\. Analytics & Visualization Interface

The web application (`http://localhost:5200`) provides two primary analytical views built with **Flask** and **Bokeh**.

### The Urban Intelligence View (`/urban`)

Focuses on the correlation between traffic and environmental health.

  * **Scatter Analysis:** Plots Vehicle Count vs. Pollution Index, color-coded by city zone.
  * **Noise Heatmap:** Bar chart ranking zones by decibel levels.
  * **Smart Insights:** An AI-simulated text block summarizing critical findings (e.g., "Zone X is the loudest").

### The Transportation View (`/dashboard`)

Focuses on operational metrics and revenue.

  * **Financial KPI:** Real-time display of Total Revenue (MXN).
  * **Trend Analysis:** Interactive time-series line chart showing daily passenger volume.
  * **Operational Hotspots:** Top 5 busiest boarding areas displayed via a spectral-colored bar chart.

-----

## 8\. Operations & Troubleshooting

### Common Resolutions

**1. "Connection Refused" on Airflow UI**

  * *Cause:* The webserver or scheduler is still initializing.
  * *Fix:* Check logs with `docker compose logs airflow-apiserver`. Wait for "Listening" status.

**2. Missing Data in Dashboards**

  * *Cause:* DAGs haven't run yet, or volumes aren't mounted.
  * *Fix:* Log into Airflow (port 8080), unpause the DAGs, and trigger a run manually. Verify file creation with `ls -la data/processed/`.

**3. Kafka Topics Missing**

  * *Cause:* Auto-creation failed or broker timing issues.
  * *Fix:* Force creation:
    ```bash
    docker exec -it kafka kafka-topics --create --bootstrap-server localhost:9092 --topic urban-sensors --partitions 1 --replication-factor 1
    ```

**4. Resetting the Environment**
To perform a complete wipe (destroying database and volumes) and restart:

```bash
docker compose down -v
docker system prune -a
docker compose up -d
```

-----

## 9\. Project Anatomy

The codebase is structured to separate configuration, logic, and data.

```text
U3_preview/
├── airflow/                 # Orchestration Logic
│   ├── dags/                # Workflow Definitions (*.py)
│   ├── plugins/             # Custom Hooks & Kafka Operators
│   └── logs/                # Execution Logs
├── data/                    # The Data Lake (Mounted Volume)
│   ├── raw/                 # Ingestion landing zone
│   ├── processed/           # Transformed datasets for dashboards
│   └── analytics/           # High-level aggregations
├── my_kafka/                # Streaming Logic
│   ├── producer/            # Python Producers
│   └── consumer/            # Python Consumers
├── web/                     # Frontend Application
│   ├── app.py               # Flask Entrypoint
│   └── templates/           # HTML/Bokeh Layouts
├── docker-compose.yml       # Infrastructure Definition
└── requirements.txt         # Python Dependencies
```

-----

*Documentation generated for VMI Project 3. Last updated: December 2025.*