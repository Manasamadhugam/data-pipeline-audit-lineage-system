\# Data Pipeline Audit \& Lineage System



\## Project Overview



The Data Pipeline Audit \& Lineage System is a Python-based data engineering project that ingests raw customer and order datasets, validates data quality, rejects invalid records, transforms valid data, and publishes clean datasets.



It also maintains pipeline execution logs, generates audit reports, and reconciles input, valid, and rejected record counts.



\## Problem Statement



Raw datasets can contain duplicate records, missing values, invalid dates, incorrect amounts, and invalid customer references. These issues can affect the reliability of analytical reports.



This project addresses these problems through automated data validation, transformation, rejection handling, audit logging, and reconciliation.



\## Technologies Used



\- Python 3.11

\- Pandas

\- NumPy

\- SQLite

\- CSV

\- Pytest



\## Pipeline Architecture



1\. Data Generation – Creates synthetic customer and order datasets.

2\. Data Ingestion – Loads CSV files into Pandas DataFrames.

3\. Data Validation – Identifies missing values, duplicates, invalid dates, amounts, and customer references.

4\. Data Reconciliation – Checks input records against valid and rejected records.

5\. Data Transformation – Cleans and standardizes valid records.

6\. Data Publishing – Saves cleaned customer and order datasets.

7\. Audit Logging – Records pipeline run IDs, input counts, output counts, and rejected counts.

8\. Audit Reporting – Stores audit information in SQLite and generates summary reports.



\## Project Results



| Metric | Customers | Orders |

|---|---:|---:|

| Input records | 1000 | 2000 |

| Valid records | 997 | 1989 |

| Rejected records | 3 | 11 |



\- Total input records: 3000

\- Total valid records: 2986

\- Total rejected records: 14

\- Reconciliation status: PASS

\- Automated tests: 4 passed



\## Project Structure



```text

data-pipeline-audit-lineage-system/

│

├── data/

│   ├── customers.csv

│   └── orders.csv

│

├── src/

│   ├── generate\_data.py

│   ├── ingestion.py

│   ├── validation.py

│   ├── transformation.py

│   ├── publishing.py

│   ├── audit.py

│   ├── audit\_report.py

│   └── reconciliation.py

│

├── output/

│   ├── cleaned\_customers.csv

│   └── cleaned\_orders.csv

│

├── rejected/

│   └── rejected\_records.csv

│

├── logs/

│   └── audit\_log.csv

│

├── reports/

│   ├── audit.db

│   ├── audit\_summary.csv

│   └── reconciliation\_report.csv

│

├── tests/

│   └── test\_pipeline.py

│

├── main.py

├── requirements.txt

├── .gitignore

└── README.md

```



\## How to Run the Project



\### 1. Clone the repository



```bash

git clone https://github.com/Manasamadhugam/data-pipeline-audit-lineage-system.git
cd data-pipeline-audit-lineage-system

```



\### 2. Install dependencies



```bash

pip install -r requirements.txt

```



\### 3. Generate synthetic datasets



```bash

python src/generate\_data.py

```



\### 4. Run the complete pipeline



```bash

python main.py

```



\### 5. Run automated tests



```bash

python -m pytest -v

```



\## Output Files



\- `output/cleaned\_customers.csv` – Validated and transformed customer data.

\- `output/cleaned\_orders.csv` – Validated and transformed order data.

\- `rejected/rejected\_records.csv` – Records that failed validation.

\- `logs/audit\_log.csv` – Pipeline execution history.

\- `reports/audit.db` – SQLite audit database.

\- `reports/audit\_summary.csv` – Pipeline run summary.

\- `reports/reconciliation\_report.csv` – Input, valid, and rejected record reconciliation.



\## Future Enhancements



\- Cloud storage integration using AWS S3 or Azure Blob.

\- Apache Airflow scheduling.

\- Real-time pipeline monitoring.

\- Advanced data quality metrics.

\- Configurable validation rules.

\- Failure handling and error logging.

\- Detailed data lineage tracking.



\## Conclusion



This project demonstrates an end-to-end data engineering workflow with data ingestion, validation, transformation, publishing, audit logging, and reconciliation. It improves data reliability and provides traceability across pipeline executions.

