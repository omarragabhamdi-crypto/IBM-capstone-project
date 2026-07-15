# Hybrid E-Commerce Data Engineering Platform
An IBM-Data-Engineering-Capstone.

---

## Project Overview
This project builds a robust, hybrid data engineering platform for a global e-commerce enterprise. It showcases the design and implementation of an OLTP system, data pipelines, warehousing, and analytics dashboard to optimize sales and operational efficiency.

## Business Problem
The company operates on multi-channel sales without a centralized system, making it difficult to analyze daily sales trends, track stock, or run analytics. Data is siloed in dynamic transactional systems and flat files, preventing real-time or analytical reporting.

## Objectives
- Design and populate a production-grade MySQL OLTP database.
- Implement robust automation scripts for backup and data recovery.
- Establish scalable ETL pipelines to clean, transform, and ingest structured and semi-structured data.
- Build a centralized Data Warehouse for analytical querying.
- Develop an interactive dashboard to visualize KPIs.

## Dataset
- **Name:** `oltpdata.csv` (E-commerce transactional dataset)
- **Features:** Timestamps, transaction IDs, product categories, quantities, store locations, and pricing metrics.

## Technologies
- **OS/Shell:** Linux (Ubuntu), Bash Scripting
- **Database (OLTP):** MySQL
- **Languages & Frameworks:** Python, Pandas, SQL
- **Orchestration & ETL:** Apache Airflow
- **Visualization:** BI Tools / Dashboards
- **Version Control:** Git, GitHub

---

## Architecture

```mermaid
graph TD
    A["oltpdata.csv"] -->|Bash Script / Ingestion| B["(MySQL OLTP)"]
    B -->|Backup: datadump.sh| C["sales_data.sql"]
    C -->|Python / ETL Pipeline| D["Data Cleaning & Transformation"]
    D -->|Loading| E["(PostgreSQL Data Warehouse)"]
    E -->|Analytics Querying| F["BI Dashboards / Visualization"]
