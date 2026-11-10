
import pandas as pd
import os


def publish_data(customers, orders):

    # Create output folder
    os.makedirs("output", exist_ok=True)

    # Define output file paths
    customers_path = "output/cleaned_customers.csv"
    orders_path = "output/cleaned_orders.csv"

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


if __name__ == "__main__":

    import sys
    sys.path.insert(0, "src")

    from ingestion import load_all_data
    from validation import validate_data
    from transformation import transform_data

    customers, orders, _ = load_all_data()

    valid_customers, valid_orders, rejected = validate_data(
        customers, orders
    )

    transformed_customers, transformed_orders = transform_data(
        valid_customers, valid_orders
    )

    publish_data(transformed_customers, transformed_orders)
