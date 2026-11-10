
import pandas as pd
import os

def reconcile_data(customers, orders, valid_customers,
                   valid_orders, rejected):

    customer_rejected = len(
        rejected[rejected["entity"] == "customer"]
    )

    order_rejected = len(
        rejected[rejected["entity"] == "order"]
    )

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

    report = pd.DataFrame(results)
    report["status"] = report["check"].map({
        True: "PASS",
        False: "FAIL"
    })

    os.makedirs("reports", exist_ok=True)
    report.to_csv("reports/reconciliation_report.csv", index=False)

    print("\nData Reconciliation Report:")
    print(report.to_string(index=False))

    if not report["check"].all():
        raise ValueError("Data reconciliation failed!")

    print("\nData Reconciliation Successful!")
    return report
