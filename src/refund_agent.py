
# ==========================================================
# CUSTOMER INTELLIGENCE SUPPORT COPILOT
# PART D - REFUND SUPPORT AGENT
# ==========================================================

import logging

from policy_rag import retrieve_policy


# STEP 1: LOGGING SETUP

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger("RefundAgent")


# STEP 2: CHECK REFUND ELIGIBILITY

def check_refund_eligibility(question):

    text = question.lower()

    eligible_keywords = [
        "damaged",
        "wrong product",
        "cancelled order",
        "refund",
        "charged twice",
        "deducted twice"
    ]

    if any(
        word in text
        for word in eligible_keywords
    ):

        return "Needs Policy Review"

    return "Not Confirmed"


# STEP 3: GENERATE CUSTOMER RESPONSE

def generate_response(question, policy_results):

    eligibility = check_refund_eligibility(question)

    if not policy_results:

        return (
            "Sorry, we could not find a matching policy. "
            "Please contact customer support."
        )

    relevant_policy = policy_results[0]["policy"]

    if eligibility == "Needs Policy Review":

        response = (
            "Thank you for contacting Instamart Support!\n\n"
            "Your request may qualify for a refund based "
            "on our policy.\n\n"
            "Relevant Policy:\n"
            f"{relevant_policy}\n\n"
            "Please provide your order details for further "
            "verification. Refund approval is subject to "
            "order verification."
        )

    else:

        response = (
            "Thank you for contacting Instamart Support!\n\n"
            "We could not confirm refund eligibility from "
            "your question alone. Please share your order "
            "details so our support team can review your request."
        )

    return response


# STEP 4: RUN REFUND AGENT

def run_refund_agent(question):

    print("\n========== REFUND SUPPORT AGENT ==========")

    print("\nCustomer Question:")
    print(question)

    # Retrieve policy information
    policy_results = retrieve_policy(question)

    # Check refund eligibility
    eligibility = check_refund_eligibility(question)

    print("\nRefund Eligibility:")
    print(eligibility)

    # Generate customer response
    response = generate_response(
        question,
        policy_results
    )

    print("\nAgent Response:")
    print(response)

    logger.info("Refund agent completed successfully")

    return response


# STEP 5: TEST REFUND AGENT

if __name__ == "__main__":

    sample_question = (
        "I received a damaged product. "
        "Can I request a refund?"
    )

    run_refund_agent(sample_question)
