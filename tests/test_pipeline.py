
import pandas as pd

from src.validation import validate_customers
from src.validation import validate_orders
from src.transformation import transform_customers
from src.transformation import transform_orders


def test_validate_customers():
    customers = pd.DataFrame({
        "customer_id": ["C001", "C002", "C002"],
        "customer_name": ["Rahul", "Priya", "Anita"],
        "email": ["rahul@gmail.com", "priya@gmail.com", "anita@gmail.com"],
        "city": ["Hyderabad", "Warangal", "Karimnagar"],
        "signup_date": ["2026-01-15"] * 3
    })

    valid, rejected = validate_customers(customers)

    assert len(valid) == 2
    assert len(rejected) == 1


def test_validate_orders():
    customers = pd.DataFrame({
        "customer_id": ["C001"]
    })

    orders = pd.DataFrame({
        "order_id": ["O001", "O002"],
        "customer_id": ["C001", "C999"],
        "order_date": ["2026-02-10", "2026-02-10"],
        "amount": [500, 1000],
        "status": ["Completed", "Pending"]
    })

    valid, rejected = validate_orders(orders, customers)

    assert len(valid) == 1
    assert len(rejected) == 1


def test_transform_customers():
    customers = pd.DataFrame({
        "customer_name": [" Rahul "],
        "email": ["RAHUL@GMAIL.COM"],
        "city": ["hyderabad"],
        "signup_date": ["2026-01-15"]
    })

    result = transform_customers(customers)

    assert result.iloc[0]["email"] == "rahul@gmail.com"
    assert result.iloc[0]["city"] == "Hyderabad"


def test_transform_orders():
    orders = pd.DataFrame({
        "order_date": ["2026-02-10"],
        "amount": [500],
        "status": ["Completed"]
    })

    result = transform_orders(orders)

    assert result.iloc[0]["status"] == "COMPLETED"
    assert result.iloc[0]["order_month"] == "2026-02"
    assert result.iloc[0]["amount_category"] == "Low"
