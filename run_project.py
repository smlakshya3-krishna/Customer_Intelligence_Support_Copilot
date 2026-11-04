
from pathlib import Path
import subprocess
import sys

# ==========================================
# CUSTOMER INTELLIGENCE SUPPORT COPILOT
# MAIN PROJECT RUNNER
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

PROJECT_STEPS = [
    ("DATA GENERATION", "generate_data.py"),
    ("DATA CLEANING", "src/data_pipeline.py"),
    ("CUSTOMER INTELLIGENCE", "src/customer_intelligence.py"),
    ("SUPPORT TICKET INTELLIGENCE", "src/triage.py"),
    ("POLICY RAG SYSTEM", "src/policy_rag.py"),
    ("REFUND SUPPORT AGENT", "src/refund_agent.py")
]


def run_project():

    print("\n" + "=" * 55)
    print(" CUSTOMER INTELLIGENCE SUPPORT COPILOT")
    print("=" * 55)

    for step_name, file_name in PROJECT_STEPS:

        print(f"\n\nSTARTING: {step_name}")
        print("-" * 55)

        file_path = BASE_DIR / file_name

        if not file_path.exists():
            print(f"ERROR: {file_name} not found!")
            return

        try:
            subprocess.run(
                [sys.executable, str(file_path)],
                cwd=BASE_DIR,
                check=True
            )

            print(f"\n{step_name} completed successfully!")

        except subprocess.CalledProcessError:
            print(f"\nERROR: {step_name} failed!")
            return

    print("\n" + "=" * 55)
    print("ALL PROJECT MODULES COMPLETED SUCCESSFULLY!")
    print("=" * 55)


if __name__ == "__main__":
    run_project()
