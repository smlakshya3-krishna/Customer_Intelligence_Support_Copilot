
# ==========================================================
# CUSTOMER INTELLIGENCE SUPPORT COPILOT
# PART C - SUPPORT TICKET INTELLIGENCE
# ==========================================================

from pathlib import Path
import pandas as pd
import re
import logging


# ----------------------------------------------------------
# STEP 1: PROJECT SETUP
# ----------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "outputs"

RAW_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger("SupportCopilot")


# ----------------------------------------------------------
# STEP 2: CREATE SAMPLE SUPPORT TICKETS
# ----------------------------------------------------------

def create_sample_tickets():

    tickets = [
        {
            "ticket_id": 501,
            "customer_id": 1001,
            "message": "My order is delayed. Please help me."
        },
        {
            "ticket_id": 502,
            "customer_id": 1002,
            "message": "I received a damaged product."
        },
        {
            "ticket_id": 503,
            "customer_id": 1005,
            "message": "I want a refund for my cancelled order."
        },
        {
            "ticket_id": 504,
            "customer_id": 1007,
            "message": "My payment was deducted twice. Urgent!"
        },
        {
            "ticket_id": 505,
            "customer_id": 1008,
            "message": "I received the wrong product."
        },
        {
            "ticket_id": 506,
            "customer_id": 1009,
            "message": "I cannot login to my account."
        },
        {
            "ticket_id": 507,
            "customer_id": 1010,
            "message": "My delivery has not arrived."
        },
        {
            "ticket_id": 508,
            "customer_id": 1012,
            "message": "Please cancel my order."
        },
        {
            "ticket_id": 509,
            "customer_id": 1013,
            "message": "I need help with my account."
        },
        {
            "ticket_id": 510,
            "customer_id": 1014,
            "message": "I was charged extra money. Please resolve immediately."
        }
    ]

    df = pd.DataFrame(tickets)

    file_path = RAW_DIR / "tickets.csv"

    df.to_csv(file_path, index=False)

    logger.info("Sample support tickets created successfully")

    return df


# ----------------------------------------------------------
# STEP 3: LOAD SUPPORT TICKETS
# ----------------------------------------------------------

def load_tickets():

    file_path = RAW_DIR / "tickets.csv"

    if not file_path.exists():
        return create_sample_tickets()

    df = pd.read_csv(file_path)

    required_columns = [
        "ticket_id",
        "customer_id",
        "message"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing ticket columns: {missing_columns}"
        )

    logger.info("Support tickets loaded successfully")

    return df


# ----------------------------------------------------------
# STEP 4: PII REDACTION
# ----------------------------------------------------------

def redact_pii(message):

    message = str(message)

    # Hide email addresses
    message = re.sub(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        '[EMAIL HIDDEN]',
        message
    )

    # Hide 10-digit phone numbers
    message = re.sub(
        r'\b\d{10}\b',
        '[PHONE HIDDEN]',
        message
    )

    return message


# ----------------------------------------------------------
# STEP 5: TICKET CLASSIFICATION
# ----------------------------------------------------------

def classify_ticket(message):

    text = str(message).lower()

    # Order cancellation checked before general order
    if any(word in text for word in
           ["cancel my order", "cancel order"]):
        return "Order Cancellation"

    elif any(word in text for word in
             ["refund", "money back", "cancelled"]):
        return "Refund"

    elif any(word in text for word in
             ["payment", "charged", "deducted"]):
        return "Payment"

    elif any(word in text for word in
             ["delivery", "delayed", "arrived", "order"]):
        return "Delivery"

    elif any(word in text for word in
             ["damaged", "wrong product", "defective"]):
        return "Product Issue"

    elif any(word in text for word in
             ["login", "account", "password"]):
        return "Account"

    else:
        return "General Query"


# ----------------------------------------------------------
# STEP 6: PRIORITY ASSIGNMENT
# ----------------------------------------------------------

def assign_priority(message):

    text = str(message).lower()

    urgent_words = [
        "urgent",
        "immediately",
        "emergency",
        "twice",
        "deducted"
    ]

    high_words = [
        "refund",
        "damaged",
        "wrong product",
        "not arrived"
    ]

    if any(word in text for word in urgent_words):
        return "High"

    elif any(word in text for word in high_words):
        return "Medium"

    else:
        return "Low"


# ----------------------------------------------------------
# STEP 7: SUPPORT TEAM ROUTING
# ----------------------------------------------------------

def assign_team(category):

    team_mapping = {
        "Refund": "Refund Team",
        "Payment": "Payment Team",
        "Delivery": "Delivery Team",
        "Product Issue": "Product Support Team",
        "Account": "Account Support Team",
        "Order Cancellation": "Order Support Team",
        "General Query": "General Support Team"
    }

    return team_mapping.get(
        category,
        "General Support Team"
    )


# ----------------------------------------------------------
# STEP 8: PROCESS ALL SUPPORT TICKETS
# ----------------------------------------------------------

def process_tickets():

    print("\n========== SUPPORT TICKET INTELLIGENCE ==========")

    df = load_tickets()

    # Remove duplicate ticket IDs
    df = df.drop_duplicates(
        subset=["ticket_id"]
    ).copy()

    # Remove empty messages
    df = df.dropna(
        subset=["message"]
    ).copy()

    # Hide personal information
    df["Redacted_Message"] = df["message"].apply(
        redact_pii
    )

    # Identify ticket category
    df["Category"] = df["message"].apply(
        classify_ticket
    )

    # Assign priority
    df["Priority"] = df["message"].apply(
        assign_priority
    )

    # Assign support team
    df["Assigned_Team"] = df["Category"].apply(
        assign_team
    )

    # Display ticket results
    print("\nProcessed Support Tickets:\n")

    print(
        df[
            [
                "ticket_id",
                "Redacted_Message",
                "Category",
                "Priority",
                "Assigned_Team"
            ]
        ].to_string(index=False)
    )

    # Category summary
    print("\nTicket Category Summary:")

    print(
        df["Category"].value_counts()
    )

    # Priority summary
    print("\nTicket Priority Summary:")

    print(
        df["Priority"].value_counts()
    )

    # Save processed data
    output_file = OUTPUT_DIR / "processed_tickets.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print("\nProcessed ticket file saved:", output_file)

    print("\nSupport ticket processing completed successfully!")

    return df


# ----------------------------------------------------------
# STEP 9: RUN THE PROGRAM
# ----------------------------------------------------------

if __name__ == "__main__":

    processed_tickets = process_tickets()
