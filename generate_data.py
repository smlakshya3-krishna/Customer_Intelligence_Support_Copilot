
# ==========================================
# INSTAMART CUSTOMER INTELLIGENCE COPILOT
# STEP 3 - GENERATE RAW DATASETS
# ==========================================

from pathlib import Path
import pandas as pd
import numpy as np

# Project folder location
BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"

# Create raw folder if it does not exist
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Random data generation
np.random.seed(42)

# ==========================================
# 1. CUSTOMER DATA
# ==========================================

customers = pd.DataFrame({
    "customer_id": range(1001, 1101),

    "name": [
        f"Customer_{i}" for i in range(1, 101)
    ],

    "age": np.random.randint(18, 60, 100),

    "gender": np.random.choice(
        ["Male", "Female"], 100
    ),

    "city": np.random.choice(
        ["Chennai", "Coimbatore", "Madurai",
         "Sivakasi", "Trichy"], 100
    )
})

# Add a few missing values for cleaning practice
customers.loc[5, "age"] = np.nan
customers.loc[12, "city"] = np.nan

customers.to_csv(
    RAW_DIR / "customers.csv",
    index=False
)


# ==========================================
# 2. PRODUCT DATA
# ==========================================

products = pd.DataFrame({
    "product_id": range(201, 221),

    "product_name": [
        f"Product_{i}" for i in range(1, 21)
    ],

    "category": np.random.choice(
        ["Fruits", "Vegetables", "Dairy",
         "Snacks", "Beverages"], 20
    ),

    "price_inr": np.random.randint(
        20, 500, 20
    )
})

products.to_csv(
    RAW_DIR / "products.csv",
    index=False
)


# ==========================================
# 3. ORDER DATA
# ==========================================

number_of_orders = 300

order_customer_ids = np.random.choice(
    customers["customer_id"],
    number_of_orders
)

order_product_ids = np.random.choice(
    products["product_id"],
    number_of_orders
)

order_quantities = np.random.randint(
    1, 6, number_of_orders
)

order_discounts = np.random.choice(
    [0, 5, 10, 15, 20],
    number_of_orders
)

order_status = np.random.choice(
    ["Completed", "Cancelled", "Pending"],
    number_of_orders,
    p=[0.75, 0.15, 0.10]
)

# Get product prices for each order
price_lookup = products.set_index(
    "product_id"
)["price_inr"]

order_prices = [
    price_lookup[product_id]
    for product_id in order_product_ids
]

order_amounts = (
    np.array(order_prices)
    * order_quantities
    * (1 - order_discounts / 100)
)

orders = pd.DataFrame({
    "order_id": range(5001, 5001 + number_of_orders),

    "customer_id": order_customer_ids,

    "product_id": order_product_ids,

    "order_ts": pd.date_range(
        start="2026-01-01",
        periods=number_of_orders,
        freq="D"
    ),

    "status": order_status,

    "quantity": order_quantities,

    "discount_pct": order_discounts,

    "order_amount": order_amounts.round(2),

    "delivery_minutes": np.random.randint(
        10, 90, number_of_orders
    )
})

orders.to_csv(
    RAW_DIR / "orders.csv",
    index=False
)


# ==========================================
# 4. DISPLAY GENERATION SUMMARY
# ==========================================

print("\nCUSTOMER INTELLIGENCE COPILOT")
print("--------------------------------")

print("Customer dataset:", len(customers), "records")
print("Product dataset:", len(products), "records")
print("Order dataset:", len(orders), "records")

print("\nAll datasets generated successfully!")

print("\nSaved files in:", RAW_DIR)
