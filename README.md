# Customer Intelligence Support Copilot

## 1. Project Overview

The **Customer Intelligence Support Copilot** is a Python-based project designed to analyse customer behaviour and improve customer support operations for an online grocery delivery platform like Instamart.

This project combines data cleaning, customer segmentation, machine learning, support ticket classification, and policy-based refund assistance in one system.

## 2. Project Objectives

- To generate and analyse customer, product, and order datasets.
- To clean and validate customer data.
- To perform RFM analysis for understanding customer purchasing behaviour.
- To segment customers based on their activities.
- To apply K-Means clustering.
- To identify inactive and at-risk customers.
- To classify customer support tickets.
- To assign priority levels and support teams.
- To retrieve relevant refund policies.
- To provide automated refund support responses.

## 3. Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- SQLite
- Joblib
- Jupyter Notebook

## 4. Project Structure

## 4. Project Structure

```text
Customer_Intelligence_Support_Copilot/
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── orders.csv
│   │   ├── products.csv
│   │   └── tickets.csv
│   │
│   ├── clean/
│   │   ├── customers_clean.csv
│   │   ├── orders_clean.csv
│   │   └── products_clean.csv
│   │
│   ├── policies/
│   │   └── refund_policy.txt
│   │
│   └── instamart.db
│
├── outputs/
│   ├── customer_rfm.csv
│   ├── customer_segments.csv
│   ├── customer_clusters.csv
│   ├── customer_lapse_prediction.csv
│   ├── processed_tickets.csv
│   └── refund_agent_results.csv
│
├── src/
│   ├── __init__.py
│   ├── data_pipeline.py
│   ├── customer_intelligence.py
│   ├── triage.py
│   ├── policy_rag.py
│   └── refund_agent.py
│
├── state/
│
├── Customer_Intelligence_Support_Copilot.ipynb
├── generate_data.py
├── run_project.py
├── Requirements.txt
└── README.md
```

## 5. Project Modules

### Part A – Data Generation and Data Cleaning

- Generates customer, product, and order datasets.
- Performs data quality auditing.
- Identifies missing values and duplicate records.
- Cleans and validates datasets.
- Stores cleaned data in SQLite.

### Part B – Customer Intelligence

- Performs RFM analysis.
- Calculates Recency, Frequency, and Monetary values.
- Segments customers into different groups.
- Uses K-Means clustering.
- Identifies inactive and at-risk customers.

### Part C – Support Ticket Intelligence

- Processes customer support messages.
- Redacts sensitive information from messages.
- Classifies tickets into categories.
- Assigns priority levels.
- Routes tickets to appropriate support teams.

### Part D – Policy RAG and Refund Support Agent

- Loads refund policy documents.
- Retrieves relevant policy information.
- Calculates refund eligibility status for review.
- Generates customer support responses.
- Provides refund assistance based on policy information.

## 6. Installation

Install the required Python packages using:

```bash
python -m pip install -r Requirements.txt
```

## 7. How to Run the Project

Open the project folder in VS Code.

Run the following command in the terminal:

```bash
python run_project.py
```

The main runner executes the project modules in sequence:

1. Data Generation
2. Data Cleaning
3. Customer Intelligence
4. Support Ticket Intelligence
5. Policy RAG System
6. Refund Support Agent

## 8. Expected Outputs

The project generates:

- Raw customer, product, and order datasets.
- Cleaned CSV datasets.
- SQLite database.
- Customer RFM analysis.
- Customer segmentation results.
- K-Means clustering results.
- Customer lapse prediction results.
- Processed support ticket records.
- Relevant refund policy information.
- Refund support agent responses.

## 9. Learning Outcomes

Through this project, we learn:

- Python programming and file handling.
- Data cleaning and preprocessing.
- Data analysis using Pandas and NumPy.
- Customer segmentation techniques.
- Machine learning using K-Means clustering.
- SQLite database operations.
- Text classification and ticket routing.
- Retrieval-Augmented Generation (RAG) concepts.
- Building an automated customer support workflow.

## 10. Conclusion

The Customer Intelligence Support Copilot demonstrates how Python, data analysis, machine learning, and policy-based information retrieval can work together to improve customer intelligence and support operations.

It helps understand customer behaviour, organise support tickets, and provide policy-based refund assistance through an automated workflow.

---

**Project Name:** Customer Intelligence Support Copilot  
**Domain:** Data Science and Customer Support  
**Programming Language:** Python