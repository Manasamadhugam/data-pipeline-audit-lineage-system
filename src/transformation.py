
import pandas as pd


# 1. Transform Customer Data
def transform_customers(customers):

    df = customers.copy()

    # Clean customer name
    df["customer_name"] = (
        df["customer_name"].astype("string").str.strip()
    )

    # Convert email to lowercase
    df["email"] = (
        df["email"].astype("string").str.strip().str.lower()
    )

    # Standardize city names
    df["city"] = (
        df["city"].astype("string").str.strip().str.title()
    )

    # Standardize signup date
    df["signup_date"] = pd.to_datetime(
        df["signup_date"], errors="raise"
    ).dt.strftime("%Y-%m-%d")

    print("Customer transformation completed!")

    return df


# 2. Transform Order Data
def transform_orders(orders):

    df = orders.copy()

    # Standardize order status
    df["status"] = (
        df["status"].astype("string").str.strip().str.upper()
    )

    # Convert amount to numeric
    df["amount"] = pd.to_numeric(
        df["amount"], errors="raise"
    ).round(2)

    # Standardize order date
    df["order_date"] = pd.to_datetime(
        df["order_date"], errors="raise"
    )

    # Create order month column
    df["order_month"] = df["order_date"].dt.strftime("%Y-%m")

    # Categorize order amounts
    df["amount_category"] = pd.cut(
        df["amount"],
        bins=[-float("inf"), 1000, 5000, float("inf")],
        labels=["Low", "Medium", "High"]
    ).astype("string")

    # Format order date
    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")

    print("Order transformation completed!")

    return df


# 3. Transform Complete Datasets
def transform_data(customers, orders):

    print("\nStarting Data Transformation...")

    transformed_customers = transform_customers(customers)

    transformed_orders = transform_orders(orders)

    print("\nData Transformation Successful!")

    print("Transformed Customers:", len(transformed_customers))
    print("Transformed Orders:", len(transformed_orders))

    return transformed_customers, transformed_orders
