
# =====================================================
# CUSTOMER INTELLIGENCE SUPPORT COPILOT
# PART A - DATA PIPELINE
# =====================================================

# STEP 1: IMPORT LIBRARIES

from pathlib import Path
import sqlite3
import logging
import pandas as pd
import numpy as np


# =====================================================
# STEP 2: PROJECT PATHS AND LOGGING
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = BASE_DIR / "data" / "raw"
CLEAN_DIR = BASE_DIR / "data" / "clean"

DB_PATH = BASE_DIR / "data" / "instamart.db"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger("Instamart")

logger.info("Customer Intelligence Copilot initialized")
logger.info("Raw folder: %s", RAW_DIR)
logger.info("Clean folder: %s", CLEAN_DIR)


# =====================================================
# STEP 3: READ RAW DATASETS
# =====================================================

def read_dataset(name):

    file_path = RAW_DIR / f"{name}.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    logger.info("%s dataset loaded successfully", name)

    return df


# =====================================================
# STEP 4: DATA QUALITY AUDIT
# =====================================================

def audit():

    dataset_names = [
        "customers",
        "products",
        "orders"
    ]

    print("\n========== DATA QUALITY AUDIT ==========")

    for name in dataset_names:

        df = read_dataset(name)

        print("\n========================================")
        print("DATASET:", name.upper())
        print("========================================")

        print("\n1. Dataset Shape:")
        print("Rows:", df.shape[0])
        print("Columns:", df.shape[1])

        print("\n2. Column Names:")
        print(df.columns.tolist())

        print("\n3. Data Types:")
        print(df.dtypes)

        print("\n4. Missing Values:")
        print(df.isnull().sum())

        print("\n5. Duplicate Records:")
        print(df.duplicated().sum())


# =====================================================
# STEP 5: CLEAN CUSTOMER DATA
# =====================================================

def clean_customers(df):

    print("\nCleaning customer dataset...")

    df = df.copy()

    # Fill missing age with median
    df["age"] = df["age"].fillna(
        df["age"].median()
    )

    # Fill missing city with most common city
    df["city"] = df["city"].fillna(
        df["city"].mode()[0]
    )

    # Remove duplicate customer IDs
    df = df.drop_duplicates(
        subset=["customer_id"]
    )

    # Convert age into integer
    df["age"] = df["age"].astype(int)

    return df


# =====================================================
# STEP 6: CLEAN PRODUCT DATA
# =====================================================

def clean_products(df):

    print("\nCleaning product dataset...")

    df = df.copy()

    # Remove duplicate product IDs
    df = df.drop_duplicates(
        subset=["product_id"]
    )

    # Remove invalid prices
    df = df[df["price_inr"] > 0].copy()

    return df


# =====================================================
# STEP 7: CLEAN ORDER DATA
# =====================================================

def clean_orders(df):

    print("\nCleaning order dataset...")

    df = df.copy()

    # Remove duplicate order IDs
    df = df.drop_duplicates(
        subset=["order_id"]
    )

    # Convert order date into datetime
    df["order_ts"] = pd.to_datetime(
        df["order_ts"],
        errors="coerce"
    )

    # Remove invalid dates
    df = df.dropna(
        subset=["order_ts"]
    )

    # Remove invalid quantities
    df = df[df["quantity"] > 0].copy()

    return df


# =====================================================
# STEP 8: SAVE CLEANED DATASETS
# =====================================================

def save_clean_data(customers, products, orders):

    customers.to_csv(
        CLEAN_DIR / "customers_clean.csv",
        index=False
    )

    products.to_csv(
        CLEAN_DIR / "products_clean.csv",
        index=False
    )

    orders.to_csv(
        CLEAN_DIR / "orders_clean.csv",
        index=False
    )

    logger.info("Clean CSV files saved successfully")


# =====================================================
# STEP 9: CREATE SQLITE DATABASE
# =====================================================

def create_database(customers, products, orders):

    connection = sqlite3.connect(DB_PATH)

    try:

        customers.to_sql(
            "customers",
            connection,
            if_exists="replace",
            index=False
        )

        products.to_sql(
            "products",
            connection,
            if_exists="replace",
            index=False
        )

        orders.to_sql(
            "orders",
            connection,
            if_exists="replace",
            index=False
        )

        print("\nSQLite database created successfully!")

    finally:
        connection.close()


# =====================================================
# STEP 10: RUN COMPLETE DATA PIPELINE
# =====================================================

def clean_data():

    print("\n========== DATA CLEANING STARTED ==========")

    # Read raw datasets
    customers = read_dataset("customers")
    products = read_dataset("products")
    orders = read_dataset("orders")

    # Clean datasets
    customers_clean = clean_customers(customers)

    products_clean = clean_products(products)

    orders_clean = clean_orders(orders)

    # Save cleaned CSV files
    save_clean_data(
        customers_clean,
        products_clean,
        orders_clean
    )

    # Create SQLite database
    create_database(
        customers_clean,
        products_clean,
        orders_clean
    )

    print("\n========== CLEANING SUMMARY ==========")

    print("Customers:", len(customers_clean))
    print("Products:", len(products_clean))
    print("Orders:", len(orders_clean))

    print("\nAll datasets cleaned successfully!")


# =====================================================
# STEP 11: VALIDATE CLEANED DATA
# =====================================================

def validate():

    print("\n========== DATA VALIDATION ==========")

    dataset_names = [
        "customers",
        "products",
        "orders"
    ]

    for name in dataset_names:

        file_path = CLEAN_DIR / f"{name}_clean.csv"

        df = pd.read_csv(file_path)

        print("\nDataset:", name.upper())

        print("Rows:", len(df))

        print("Missing values:", df.isnull().sum().sum())

        print("Duplicate records:", df.duplicated().sum())

    print("\nValidation completed successfully!")


# =====================================================
# MAIN PROGRAM
# =====================================================

if __name__ == "__main__":

    audit()

    clean_data()

    validate()
