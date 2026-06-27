# Job Market Analytics Platform

An end-to-end **Data Engineering** project that collects job postings, processes and enriches the data, stores it in a PostgreSQL warehouse, and provides analytical insights into hiring trends and in-demand technical skills.

## Project Overview

The goal of this project is to simulate a production-style data engineering pipeline that ingests job posting data, performs ETL processing, extracts technical skills from job descriptions, and stores normalized data in PostgreSQL for analytics.

The project is designed to demonstrate practical data engineering concepts including:

* Data ingestion
* ETL pipelines
* Data cleaning
* Data normalization
* Relational database design
* Incremental loading
* SQL analytics
* Dockerized PostgreSQL

---

## Architecture

```text
Job Source (RemoteOK API)
            │
            ▼
     Raw JSON Storage
            │
            ▼
     Data Cleaning Layer
            │
            ▼
    Skill Extraction Layer
            │
            ▼
      PostgreSQL Warehouse
       ├── jobs
       ├── skills
       └── job_skills
            │
            ▼
      SQL Analytics Layer
            │
            ▼
   Streamlit Dashboard (Upcoming)
```

---

## Tech Stack

| Category               | Technology           |
| ---------------------- | -------------------- |
| Language               | Python 3.12          |
| Data Processing        | Pandas               |
| Database               | PostgreSQL           |
| ORM                    | SQLAlchemy           |
| Containerization       | Docker               |
| Version Control        | Git & GitHub         |
| Dashboard              | Streamlit (Upcoming) |
| Workflow Orchestration | Airflow (Planned)    |
| Testing                | Pytest (Planned)     |

---

## Project Structure

```text
job-market-analytics/
│
├── analytics/
├── database/
├── data/
│   ├── raw/
│   └── processed/
├── extract/
├── load/
├── transform/
├── tests/
│
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Features Implemented

* Fetch job postings from RemoteOK API
* Store raw API responses
* Clean and transform job data
* Extract technical skills from job descriptions
* Load data into PostgreSQL
* Normalize skills using a many-to-many relationship
* Incremental loading to prevent duplicate records

---

## Planned Features

* Data quality validation
* Logging
* Configuration management
* Airflow DAG for pipeline orchestration
* Streamlit analytics dashboard
* Dockerized application services
* AWS deployment
* CI/CD with GitHub Actions
* dbt transformation layer

---

## Database Schema

### jobs

Stores job-related information.

### skills

Stores unique technical skills.

### job_skills

Bridge table representing the many-to-many relationship between jobs and skills.

---

## Getting Started

Clone the repository:

```bash
git clone <repository-url>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start PostgreSQL:

```bash
docker compose up -d
```

Run the pipeline:

```bash
python extract/remoteok_fetch.py
python transform/clean_jobs.py
python transform/extract_skills.py
python -m load.load_jobs
```

---

## Future Enhancements

* Support multiple job sources
* Incremental API ingestion
* Data quality reporting
* Salary extraction from job descriptions
* Dashboard visualizations
* Cloud deployment
* Automated scheduling with Airflow

---

## 👨‍💻 Author

Built as a portfolio project to demonstrate practical Data Engineering skills including ETL, data warehousing, SQL, Docker, and analytics.
