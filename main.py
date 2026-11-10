
from src.ingestion import load_all_data
from src.validation import validate_data
from src.transformation import transform_data
from src.publishing import publish_data
from src.audit import log_pipeline_run
from src.reconciliation import reconcile_data
from src.audit_report import create_audit_report


def run_pipeline():
    print("\n================================")
    print(" DATA PIPELINE AUDIT SYSTEM")
    print("================================")

    # Step 1: Ingestion
    customers, orders, input_details = load_all_data()

    # Step 2: Validation
    valid_customers, valid_orders, rejected = validate_data(
        customers, orders
    )

    # Step 3: Reconciliation
    reconcile_data(
        customers, orders,
        valid_customers, valid_orders, rejected
    )

    # Step 4: Transformation
    transformed_customers, transformed_orders = transform_data(
        valid_customers, valid_orders
    )

    # Step 5: Publishing
    output_details = publish_data(
        transformed_customers, transformed_orders
    )

    # Step 6: Audit Logging
    log_pipeline_run(
        input_details, output_details, len(rejected)
    )

    # Step 7: Audit Report
    create_audit_report()

    print("\n================================")
    print(" PIPELINE COMPLETED SUCCESSFULLY")
    print("================================")


if __name__ == "__main__":
    run_pipeline()
