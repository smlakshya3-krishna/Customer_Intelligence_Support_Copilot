
def clean_customers(df):

    print("\nCleaning customer dataset...")

    # Create a copy of the original dataset
    df = df.copy()

    # Check required columns
    required_columns = [
        "customer_id",
        "name",
        "age",
        "gender",
        "city"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    # Remove duplicate customer records
    df = df.drop_duplicates(subset=["customer_id"])

    # Convert age into numeric format
    df["age"] = pd.to_numeric(df["age"], errors="coerce")

    # Replace invalid ages with missing values
    df.loc[~df["age"].between(18, 100), "age"] = np.nan

    # Fill missing age with median age
    median_age = df["age"].median()

    if pd.isna(median_age):
        median_age = 25

    df["age"] = df["age"].fillna(median_age)

    # Clean customer names
    df["name"] = df["name"].fillna("Unknown")
    df["name"] = df["name"].astype(str).str.strip()

    # Clean gender values
    df["gender"] = df["gender"].fillna("Unknown")
    df["gender"] = df["gender"].astype(str).str.strip().str.title()

    # Clean city values
    df["city"] = df["city"].fillna("Unknown")
    df["city"] = df["city"].astype(str).str.strip().str.title()

    # Reset index
    df = df.reset_index(drop=True)

    print("Customer data cleaning completed!")
    print("Total customers:", len(df))
    print("Missing values:", df.isnull().sum().sum())
    print("Duplicate records:", df.duplicated().sum())

    return df
