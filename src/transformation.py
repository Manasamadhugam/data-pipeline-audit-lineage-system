
import pandas as pd


def transform_customers(customers):

    df = customers.copy()

    df["customer_name"] = df["customer_name"].str.strip()

    df["email"] = df["email"].str.strip().str.lower()

    df["city"] = df["city"].str.strip().str.title()

    df["signup_date"] = pd.to_datetime(
        df["signup_date"]
    ).dt.strftime("%Y-%m-%d")

    print("Customer transformation completed!")

    return df


def transform_orders(orders):

    df = orders.copy()

    df["status"] = df["status"].str.strip().str.upper()

    df["amount"] = pd.to_numeric(
        df["amount"]
    ).round(2)

    df["order_date"] = pd.to_datetime(
        df["order_date"]
    )

    df["order_month"] = df["order_date"].dt.strftime("%Y-%m")

    df["amount_category"] = pd.cut(
        df["amount"],
        bins=[-float("inf"), 1000, 5000, float("inf")],
        labels=["Low", "Medium", "High"]
    ).astype(str)

    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")

    print("Order transformation completed!")

    return df


def transform_data(customers, orders):

    print("\nStarting Data Transformation...")

    transformed_customers = transform_customers(customers)

    transformed_orders = transform_orders(orders)

    print("\nData Transformation Successful!")

    print("Transformed Customers:", len(transformed_customers))
    print("Transformed Orders:", len(transformed_orders))

    return transformed_customers, transformed_orders
