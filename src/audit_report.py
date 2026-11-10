
import pandas as pd
import sqlite3
import os

def create_audit_report():
    os.makedirs("reports", exist_ok=True)

    # Read audit log
    audit_df = pd.read_csv("logs/audit_log.csv")

    # Connect to SQLite database
    connection = sqlite3.connect("reports/audit.db")

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
        GROUP_CONCAT(DISTINCT source_file) AS input_files,
        SUM(input_records) AS total_input_records,
        GROUP_CONCAT(DISTINCT output_file) AS output_files,
        SUM(output_records) AS total_output_records,
        MAX(rejected_records) AS rejected_records,
        MIN(status) AS status
    FROM pipeline_audit
    GROUP BY run_id
    """

    report = pd.read_sql_query(query, connection)

    # Save report as CSV
    report.to_csv("reports/audit_summary.csv", index=False)

    print("\nAudit Report Created Successfully!")
    print(report.to_string(index=False))
    print("\nSaved Files:")
    print("reports/audit.db")
    print("reports/audit_summary.csv")

    connection.close()


if __name__ == "__main__":
    create_audit_report()
