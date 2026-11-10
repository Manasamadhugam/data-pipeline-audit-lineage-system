
import pandas as pd
import os
import uuid
from datetime import datetime, timezone

# Get project folder path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")


# 1. Log pipeline execution details
def log_pipeline_run(input_details, output_details, rejected_count):

    # Create logs folder
    os.makedirs(LOGS_DIR, exist_ok=True)

    # Define audit log file
    audit_file = os.path.join(LOGS_DIR, "audit_log.csv")

    # Generate unique run ID and timestamp
    run_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    records = []

    # Record input dataset details
    for item in input_details:

        records.append({
            "run_id": run_id,
            "timestamp": timestamp,
            "source_file": item["source_file"],
            "input_records": item["input_records"],
            "output_file": "",
            "output_records": "",
            "rejected_records": rejected_count,
            "status": "SUCCESS"
        })

    # Record output dataset details
    for key in ["customers", "orders"]:

        records.append({
            "run_id": run_id,
            "timestamp": timestamp,
            "source_file": "",
            "input_records": "",
            "output_file": output_details[f"{key}_output"],
            "output_records": output_details[f"{key}_count"],
            "rejected_records": rejected_count,
            "status": "SUCCESS"
        })

    # Convert records into DataFrame
    audit_df = pd.DataFrame(records)

    # Append records to audit CSV
    audit_df.to_csv(
        audit_file,
        mode="a",
        header=not os.path.exists(audit_file),
        index=False
    )

    print("\nAudit Logging Completed!")
    print("Pipeline Run ID:", run_id)
    print("Audit File:", audit_file)

    return run_id
