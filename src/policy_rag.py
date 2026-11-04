
# ==========================================================
# CUSTOMER INTELLIGENCE SUPPORT COPILOT
# PART D - POLICY RAG SYSTEM
# ==========================================================

from pathlib import Path
import logging
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# STEP 1: PROJECT SETUP

BASE_DIR = Path(__file__).resolve().parents[1]

POLICY_FILE = (
    BASE_DIR / "data" / "policies" / "refund_policy.txt"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger("PolicyRAG")


# STEP 2: LOAD POLICY DOCUMENT

def load_policy():

    if not POLICY_FILE.exists():
        raise FileNotFoundError(
            f"Policy file not found: {POLICY_FILE}"
        )

    with open(
        POLICY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        policy_text = file.read()

    if not policy_text.strip():
        raise ValueError("Policy document is empty")

    logger.info("Refund policy loaded successfully")

    return policy_text


# STEP 3: SPLIT POLICY INTO SECTIONS

def split_policy(policy_text):

    sections = re.split(
        r'\n(?=\d+\.\s)',
        policy_text.strip()
    )

    chunks = [
        section.strip()
        for section in sections
        if section.strip()
    ]

    logger.info(
        "%s policy sections created",
        len(chunks)
    )

    return chunks


# STEP 4: BUILD SEARCH MODEL

def build_retriever():

    policy_text = load_policy()

    policy_chunks = split_policy(policy_text)

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2)
    )

    policy_vectors = vectorizer.fit_transform(
        policy_chunks
    )

    logger.info(
        "Policy search model created successfully"
    )

    return vectorizer, policy_vectors, policy_chunks


# STEP 5: RETRIEVE RELEVANT POLICY

def retrieve_policy(question, top_k=2):

    if not str(question).strip():
        raise ValueError("Please enter a customer question")

    vectorizer, policy_vectors, policy_chunks = (
        build_retriever()
    )

    question_vector = vectorizer.transform(
        [question]
    )

    similarity_scores = cosine_similarity(
        question_vector,
        policy_vectors
    ).flatten()

    ranked_indices = similarity_scores.argsort()[::-1]

    results = []

    for index in ranked_indices[:top_k]:

        score = float(similarity_scores[index])

        if score > 0:

            results.append({
                "policy": policy_chunks[index],
                "similarity": round(score, 3)
            })

    logger.info("Policy retrieval completed")

    return results


# STEP 6: DISPLAY POLICY RESULTS

def answer_question(question):

    print("\n========== POLICY RAG SYSTEM ==========")

    print("\nCustomer Question:")
    print(question)

    results = retrieve_policy(question)

    if not results:

        print("\nNo matching policy information found.")

        return []

    print("\nRelevant Policy Information:")

    for number, result in enumerate(results, start=1):

        print(f"\n{number}. {result['policy']}")

        print(
            "Similarity Score:",
            result["similarity"]
        )

    print("\nPolicy retrieval completed successfully!")

    return results


# STEP 7: TEST POLICY RAG

if __name__ == "__main__":

    sample_question = (
        "I received a damaged product. "
        "Can I request a refund?"
    )

    answer_question(sample_question)
