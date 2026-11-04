
# =====================================================
# CUSTOMER INTELLIGENCE SUPPORT COPILOT
# PART B - CUSTOMER INTELLIGENCE
# STEP 1 - RFM ANALYSIS
# =====================================================

from pathlib import Path
import pandas as pd
import numpy as np

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]

CLEAN_DIR = BASE_DIR / "data" / "clean"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================
# STEP 1: LOAD CLEANED DATA
# =====================================================

orders = pd.read_csv(
    CLEAN_DIR / "orders_clean.csv"
)

print("Cleaned order data loaded successfully!")

# Convert order date into datetime
orders["order_ts"] = pd.to_datetime(
    orders["order_ts"]
)


# =====================================================
# STEP 2: FILTER COMPLETED ORDERS
# =====================================================

completed_orders = orders[
    orders["status"].str.lower() == "completed"
].copy()

print("Completed orders:", len(completed_orders))


# =====================================================
# STEP 3: CALCULATE RFM VALUES
# =====================================================

# Reference date = day after the latest order date
reference_date = (
    completed_orders["order_ts"].max()
    + pd.Timedelta(days=1)
)

rfm = completed_orders.groupby(
    "customer_id"
).agg(

    # Recency: Days since last order
    Recency=(
        "order_ts",
        lambda x: (
            reference_date - x.max()
        ).days
    ),

    # Frequency: Total number of orders
    Frequency=(
        "order_id",
        "nunique"
    ),

    # Monetary: Total money spent
    Monetary=(
        "order_amount",
        "sum"
    )

).reset_index()


# =====================================================
# STEP 4: DISPLAY RFM RESULTS
# =====================================================

rfm["Monetary"] = rfm["Monetary"].round(2)

print("\n========== RFM ANALYSIS ==========")

print(rfm.head(10))

print("\nTotal customers analysed:", len(rfm))


# =====================================================
# STEP 5: SAVE RFM RESULTS
# =====================================================

rfm.to_csv(
    OUTPUT_DIR / "customer_rfm.csv",
    index=False
)

print("\nRFM analysis completed successfully!")

print("RFM file saved in:", OUTPUT_DIR)


# =====================================================
# STEP 2 - CUSTOMER SEGMENTATION
# =====================================================

def customer_segmentation(rfm):

    rfm = rfm.copy()

    # Assign customer groups based on RFM values
    def assign_segment(row):

        if row["Recency"] <= 30 and row["Monetary"] >= 1500:
            return "High Value Customer"

        elif row["Frequency"] >= 3:
            return "Regular Customer"

        elif row["Recency"] > 90:
            return "At Risk Customer"

        else:
            return "New / Occasional Customer"

    # Apply segmentation
    rfm["Segment"] = rfm.apply(
        assign_segment,
        axis=1
    )

    print("\n========== CUSTOMER SEGMENTATION ==========")

    print(
        rfm[
            ["customer_id", "Recency", "Frequency",
             "Monetary", "Segment"]
        ].head(10)
    )

    # Count customers in each segment
    print("\nCustomer Segment Summary:")

    print(rfm["Segment"].value_counts())

    # Save segmentation results
    rfm.to_csv(
        OUTPUT_DIR / "customer_segments.csv",
        index=False
    )

    print("\nCustomer segmentation completed!")

    return rfm


# =====================================================
# RUN CUSTOMER SEGMENTATION
# =====================================================

if __name__ == "__main__":

    segmented_customers = customer_segmentation(rfm)


# =====================================================
# STEP 3 - K-MEANS CLUSTERING
# =====================================================

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def perform_kmeans(rfm):

    print("\n========== K-MEANS CLUSTERING ==========")

    # Select RFM columns
    features = rfm[
        ["Recency", "Frequency", "Monetary"]
    ].copy()

    # Convert values into a common scale
    scaler = StandardScaler()

    scaled_data = scaler.fit_transform(features)

    # Create K-Means model
    kmeans = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    # Assign cluster numbers
    rfm["Cluster"] = kmeans.fit_predict(
        scaled_data
    )

    # Display cluster results
    print("\nCustomer Cluster Results:")

    print(
        rfm[
            ["customer_id", "Recency",
             "Frequency", "Monetary", "Cluster"]
        ].head(10)
    )

    # Count customers in each cluster
    print("\nCluster Summary:")

    print(
        rfm["Cluster"].value_counts().sort_index()
    )

    # Save results
    rfm.to_csv(
        OUTPUT_DIR / "customer_clusters.csv",
        index=False
    )

    print("\nK-Means clustering completed successfully!")

    return rfm


# =====================================================
# RUN CUSTOMER SEGMENTATION AND K-MEANS
# =====================================================

if __name__ == "__main__":

    segmented_customers = customer_segmentation(rfm)

    clustered_customers = perform_kmeans(
        segmented_customers
    )


# =====================================================
# STEP 4 - CUSTOMER LAPSE PREDICTION
# =====================================================

def predict_customer_lapse(rfm):

    rfm = rfm.copy()

    print("\n========== CUSTOMER LAPSE PREDICTION ==========")

    # Classify customers based on recency
    def predict_status(days):

        if days <= 30:
            return "Active Customer"

        elif days <= 90:
            return "At Risk Customer"

        else:
            return "Inactive Customer"

    # Apply prediction rules
    rfm["Lapse_Status"] = rfm["Recency"].apply(
        predict_status
    )

    # Display results
    print("\nCustomer Lapse Results:")

    print(
        rfm[
            ["customer_id", "Recency", "Lapse_Status"]
        ].head(10)
    )

    # Summary
    print("\nLapse Prediction Summary:")

    print(
        rfm["Lapse_Status"].value_counts()
    )

    # Save results
    rfm.to_csv(
        OUTPUT_DIR / "customer_lapse_prediction.csv",
        index=False
    )

    print("\nCustomer lapse prediction completed!")

    return rfm


# =====================================================
# RUN COMPLETE CUSTOMER INTELLIGENCE
# =====================================================

if __name__ == "__main__":

    segmented_customers = customer_segmentation(rfm)

    clustered_customers = perform_kmeans(
        segmented_customers
    )

    lapse_results = predict_customer_lapse(
        clustered_customers
    )
