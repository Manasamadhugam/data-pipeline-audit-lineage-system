
import pandas as pd
import os
from datetime import datetime, timezone

# Get project folder path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


# 1. Ingest individual CSV file
def ingest_data(file_path):

    # Check whether input file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")

    # Read CSV file
    df = pd.read_csv(file_path)

    # Capture ingestion details
    ingestion_details = {
        "source_file": file_path,
        "input_records": len(df),
        "columns": list(df.columns),
        "ingestion_timestamp": datetime.now(timezone.utc).isoformat()
    }

    print("\nData Ingestion Successful!")
    print("Source File:", file_path)
    print("Total Records:", len(df))
    print("Columns:", list(df.columns))

    return df, ingestion_details


# 2. Load all datasets
def load_all_data():

    # Read customers data
    customers, customers_info = ingest_data(
        os.path.join(DATA_DIR, "customers.csv")
    )

    # Read orders data
    orders, orders_info = ingest_data(
        os.path.join(DATA_DIR, "orders.csv")
    )

    print("\nCustomers Sample:")
    print(customers.head())

    print("\nOrders Sample:")
    print(orders.head())

    return customers, orders, [customers_info, orders_info]


# 3. Execute ingestion when this file runs directly
if __name__ == "__main__":

    customers, orders, details = load_all_data()

    print("\nTotal Input Records:",
          sum(item["input_records"] for item in details))

    print("\nIngestion Completed Successfully!")
