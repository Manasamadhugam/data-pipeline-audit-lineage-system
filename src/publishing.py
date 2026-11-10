

import os
import sys

# Get project folder paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
SRC_DIR = os.path.join(BASE_DIR, "src")


# 1. Publish cleaned datasets
def publish_data(customers, orders):

    # Create output folder
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Define output file paths
    customers_path = os.path.join(
        OUTPUT_DIR, "cleaned_customers.csv"
    )

    orders_path = os.path.join(
        OUTPUT_DIR, "cleaned_orders.csv"
    )

    # Save cleaned customer data
    customers.to_csv(
        customers_path,
        index=False
    )

    # Save cleaned order data
    orders.to_csv(
        orders_path,
        index=False
    )

    print("\nData Publishing Completed!")

    print("\nPublished Files:")
    print(customers_path)
    print(orders_path)

    print("\nPublished Customer Records:", len(customers))
    print("Published Order Records:", len(orders))

    return {
        "customers_output": customers_path,
        "orders_output": orders_path,
        "customers_count": len(customers),
        "orders_count": len(orders)
    }


# 2. Execute publishing independently
if __name__ == "__main__":

    # Add src folder to Python import path
    sys.path.insert(0, SRC_DIR)

    from ingestion import load_all_data
    from validation import validate_data
    from transformation import transform_data

    # Load datasets
    customers, orders, _ = load_all_data()

    # Validate datasets
    valid_customers, valid_orders, rejected = validate_data(
        customers, orders
    )

    # Transform valid datasets
    transformed_customers, transformed_orders = transform_data(
        valid_customers, valid_orders
    )

    # Publish cleaned datasets
    publish_data(
        transformed_customers,
        transformed_orders
    )
