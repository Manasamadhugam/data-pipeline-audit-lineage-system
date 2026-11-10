
import pandas as pd
import sqlite3
import os

# Get project folder paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


# 1. Create Audit Report
def create_audit_report():

    # Create reports folder
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Define file paths
    audit_file = os.path.join(LOGS_DIR, "audit_log.csv")
    database_file = os.path.join(REPORTS_DIR, "audit.db")
    summary_file = os.path.join(REPORTS_DIR, "audit_summary.csv")

    # Check whether audit log exists
    if not os.path.exists(audit_file):
        raise FileNotFoundError(
            f"Audit log not found: {audit_file}"
        )

    # Read audit log
    audit_df = pd.read_csv(audit_file)

    if audit_df.empty:
        raise ValueError("Audit log is empty. No report can be created.")

    # Connect to SQLite database
    connection = sqlite3.connect(database_file)

    try:
        # Store audit records in SQLite
        audit_df.to_sql(
            "pipeline_audit",
            connection,
            if_exists="replace",
            index=False
        )

        # Query pipeline execution details
        query = """
        SELECT
            run_id,
            MIN(timestamp) AS execution_time,
            GROUP_CONCAT(DISTINCT NULLIF(source_file, ''))
                AS input_files,
            SUM(input_records) AS total_input_records,
            GROUP_CONCAT(DISTINCT NULLIF(output_file, ''))
                AS output_files,
            SUM(output_records) AS total_output_records,
            MAX(rejected_records) AS rejected_records,
            MIN(status) AS status
        FROM pipeline_audit
        GROUP BY run_id
        ORDER BY execution_time DESC
        """

        # Execute SQL query
        report = pd.read_sql_query(query, connection)

        # Save summary report
        report.to_csv(summary_file, index=False)

        print("\nAudit Report Created Successfully!")

        print("\nPipeline Audit Summary:")
        print(report.to_string(index=False))

        print("\nSaved Files:")
        print(database_file)
        print(summary_file)

    finally:
        # Close database connection
        connection.close()


# 2. Execute Audit Report
if __name__ == "__main__":

    create_audit_report()
