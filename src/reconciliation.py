
import pandas as pd
import os

# Get project folder path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


# Reconcile input, valid and rejected records
def reconcile_data(customers, orders, valid_customers,
                   valid_orders, rejected):

    # Count rejected customer records
    customer_rejected = len(
        rejected[rejected["entity"] == "customer"]
    )

    # Count rejected order records
    order_rejected = len(
        rejected[rejected["entity"] == "order"]
    )

    # Create reconciliation results
    results = [
        {
            "dataset": "customers",
            "input_records": len(customers),
            "valid_records": len(valid_customers),
            "rejected_records": customer_rejected,
            "check": len(customers) == len(valid_customers) + customer_rejected
        },
        {
            "dataset": "orders",
            "input_records": len(orders),
            "valid_records": len(valid_orders),
            "rejected_records": order_rejected,
            "check": len(orders) == len(valid_orders) + order_rejected
        }
    ]

    # Create reconciliation report
    report = pd.DataFrame(results)

    # Assign PASS or FAIL status
    report["status"] = report["check"].map({
        True: "PASS",
        False: "FAIL"
    })

    # Save reconciliation report
    os.makedirs(REPORTS_DIR, exist_ok=True)

    report_path = os.path.join(
        REPORTS_DIR, "reconciliation_report.csv"
    )

    report.to_csv(report_path, index=False)

    # Display report
    print("\nData Reconciliation Report:")
    print(report.to_string(index=False))

    # Stop pipeline if reconciliation fails
    if not report["check"].all():
        raise ValueError("Data reconciliation failed!")

    print("\nData Reconciliation Successful!")
    print("Report saved to:", report_path)

    return report
