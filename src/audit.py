
import pandas as pd
import os
import uuid
from datetime import datetime, timezone

def log_pipeline_run(input_details, output_details, rejected_count):
    os.makedirs("logs", exist_ok=True)

    audit_file = "logs/audit_log.csv"

    run_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    records = []

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

    audit_df = pd.DataFrame(records)

    audit_df.to_csv(
        audit_file,
        mode="a",
        header=not os.path.exists(audit_file),
        index=False
    )

    print("\nAudit Logging Completed!")
    print("Pipeline Run ID:", run_id)
    print("Audit File:", audit_file)
