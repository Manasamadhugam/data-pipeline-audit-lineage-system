
import pandas as pd
import os


def validate_customers(customers):

    df = customers.copy()

    # Add source tracking details
    df["source_file"] = "customers.csv"
    df["source_row"] = range(2, len(df) + 2)

    reasons = pd.Series("", index=df.index, dtype="object")

    # Check missing required fields
    for column in ["customer_id", "customer_name", "email", "city"]:
        invalid = df[column].isna() | (
            df[column].astype(str).str.strip() == ""
        )
        reasons.loc[invalid] += f"Missing {column}; "

    # Check duplicate customer IDs
    duplicate = df["customer_id"].duplicated(keep="first")
    reasons.loc[duplicate] += "Duplicate customer_id; "

    # Separate valid and rejected records
    rejected_mask = reasons != ""

    valid = df.loc[~rejected_mask].copy()
    rejected = df.loc[rejected_mask].copy()

    rejected["reject_reason"] = reasons.loc[rejected_mask]

    return valid, rejected


def validate_orders(orders, valid_customers):

    df = orders.copy()

    # Add source tracking details
    df["source_file"] = "orders.csv"
    df["source_row"] = range(2, len(df) + 2)

    reasons = pd.Series("", index=df.index, dtype="object")

    # Check missing required fields
    for column in ["order_id", "customer_id", "order_date",
                   "amount", "status"]:
        invalid = df[column].isna() | (
            df[column].astype(str).str.strip() == ""
        )
        reasons.loc[invalid] += f"Missing {column}; "

    # Check duplicate order IDs
    duplicate = df["order_id"].duplicated(keep="first")
    reasons.loc[duplicate] += "Duplicate order_id; "

    # Check invalid dates
    parsed_dates = pd.to_datetime(df["order_date"], errors="coerce")
    invalid_dates = parsed_dates.isna()
    reasons.loc[invalid_dates] += "Invalid order_date; "

    # Check negative or invalid amounts
    amounts = pd.to_numeric(df["amount"], errors="coerce")
    invalid_amounts = amounts.isna() | (amounts < 0)
    reasons.loc[invalid_amounts] += "Invalid amount; "

    # Check customer reference
    customer_ids = set(valid_customers["customer_id"].dropna())
    invalid_reference = ~df["customer_id"].isin(customer_ids)
    reasons.loc[invalid_reference] += "Invalid customer reference; "

    # Check valid order status
    allowed_statuses = ["Completed", "Pending", "Cancelled"]
    invalid_status = ~df["status"].isin(allowed_statuses)
    reasons.loc[invalid_status] += "Invalid order status; "

    # Separate valid and rejected records
    rejected_mask = reasons != ""

    valid = df.loc[~rejected_mask].copy()
    rejected = df.loc[rejected_mask].copy()

    rejected["reject_reason"] = reasons.loc[rejected_mask]

    return valid, rejected


def validate_data(customers, orders):

    print("\nStarting Data Validation...")

    valid_customers, rejected_customers = validate_customers(
        customers
    )

    valid_orders, rejected_orders = validate_orders(
        orders, valid_customers
    )

    # Combine rejected records
    rejected_customers["entity"] = "customer"
    rejected_orders["entity"] = "order"

    rejected_records = pd.concat(
        [rejected_customers, rejected_orders],
        ignore_index=True,
        sort=False
    )

    # Save rejected records
    os.makedirs("rejected", exist_ok=True)

    rejected_records.to_csv(
        "rejected/rejected_records.csv",
        index=False
    )

    print("\nData Validation Completed!")

    print("\nCustomers:")
    print("Input Records:", len(customers))
    print("Valid Records:", len(valid_customers))
    print("Rejected Records:", len(rejected_customers))

    print("\nOrders:")
    print("Input Records:", len(orders))
    print("Valid Records:", len(valid_orders))
    print("Rejected Records:", len(rejected_orders))

    print("\nTotal Rejected Records:", len(rejected_records))

    print("\nRejected records saved to:")
    print("rejected/rejected_records.csv")

    return (
        valid_customers,
        valid_orders,
        rejected_records
    )


if __name__ == "__main__":

    from ingestion import load_all_data

    customers, orders, details = load_all_data()

    valid_customers, valid_orders, rejected = validate_data(
        customers, orders
    )
