
import pandas as pd
import numpy as np
import random
import os

# Fixed seed for reproducible data
random.seed(42)
np.random.seed(42)

# Create data folder
os.makedirs("data", exist_ok=True)

# --------------------------------
# 1. Generate Customers Dataset
# --------------------------------

customers = []

names = [
    "Rahul", "Priya", "Anita", "Kiran", "Vijay",
    "Sneha", "Arjun", "Meena", "Ravi", "Divya"
]

cities = [
    "Hyderabad", "Warangal", "Karimnagar",
    "Khammam", "Wanaparthy"
]

for i in range(1, 1001):
    customers.append({
        "customer_id": f"C{i:04d}",
        "customer_name": random.choice(names),
        "email": f"customer{i}@gmail.com",
        "city": random.choice(cities),
        "signup_date": "2026-01-15"
    })

customers_df = pd.DataFrame(customers)

# Introduce data quality issues
customers_df.loc[5, "email"] = None
customers_df.loc[10, "city"] = None
customers_df.loc[999, "customer_id"] = "C0001"

# Save customers dataset
customers_df.to_csv("data/customers.csv", index=False)


# --------------------------------
# 2. Generate Orders Dataset
# --------------------------------

orders = []

statuses = ["Completed", "Pending", "Cancelled"]

for i in range(1, 2001):
    orders.append({
        "order_id": f"O{i:05d}",
        "customer_id": f"C{random.randint(1, 1000):04d}",
        "order_date": "2026-02-10",
        "amount": round(random.uniform(100, 10000), 2),
        "status": random.choice(statuses)
    })

orders_df = pd.DataFrame(orders)

# Introduce data quality issues
orders_df.loc[1999, "order_id"] = "O00001"
orders_df.loc[1998, "customer_id"] = "C9999"
orders_df.loc[1997, "amount"] = -500
orders_df.loc[1996, "amount"] = None
orders_df.loc[1995, "order_date"] = "invalid_date"

# Save orders dataset
orders_df.to_csv("data/orders.csv", index=False)


# --------------------------------
# 3. Print Generation Summary
# --------------------------------

print("Sample datasets generated successfully!")

print("\nCustomers Dataset:")
print("Total Records:", len(customers_df))
print("Unique Customer IDs:", customers_df["customer_id"].nunique())

print("\nOrders Dataset:")
print("Total Records:", len(orders_df))
print("Unique Order IDs:", orders_df["order_id"].nunique())

print("\nFiles saved:")
print("data/customers.csv")
print("data/orders.csv")
