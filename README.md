# Customer Churn Analytics

An end-to-end customer churn analytics project that processes 1,000,000 synthetic telecom customer records, identifies major churn drivers, compares multiple machine-learning models, and produces a prioritized customer retention action queue.

## Project Overview

Customer churn creates lost recurring revenue and increased customer-acquisition costs. This project demonstrates how customer data can be transformed into actionable retention recommendations.

The project answers four business questions:

1. Which customers are most likely to churn?
2. What factors are associated with higher churn risk?
3. Which model provides the best balance of performance and interpretability?
4. What action should the retention team take for each high-risk customer?

## Business Deliverables

- Interactive Power BI churn dashboard
- Comparison of Logistic Regression, Random Forest, and XGBoost
- Identification of major churn drivers
- Ranked retention queue for the top 20,000 high-risk customers
- Recommended retention action for each selected customer
- Customer-level CSV preview for operational use

## Key Results

- Processed and analyzed **1,000,000 customer records**
- Compared three classification models using **5-fold stratified cross-validation**
- Selected Logistic Regression because it performed comparably to more complex models while providing stronger interpretability
- Achieved approximately **64% churn recall**
- Generated a retention queue containing the **top 10% highest-risk customers**
- Translated model findings into customer-specific retention recommendations

## Model Comparison

| Model | Accuracy | Balanced Accuracy | Precision | Recall | F1 | F2 | ROC-AUC | PR-AUC | MCC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.6280 | 0.6320 | 0.1583 | 0.6369 | 0.2536 | 0.3969 | 0.6846 | 0.2035 | 0.1611 |
| Random Forest | 0.6133 | 0.6302 | 0.1551 | **0.6513** | 0.2505 | 0.3972 | 0.6812 | 0.1998 | 0.1579 |
| XGBoost | **0.6335** | **0.6339** | **0.1601** | 0.6344 | **0.2557** | **0.3984** | **0.6858** | **0.2047** | **0.1639** |

All results above are validation averages from 5-fold cross-validation.

### Final Model Selection

Logistic Regression was selected as the final model because its performance was nearly identical to tuned Random Forest and XGBoost models while providing:

- Easier interpretation
- Lower deployment complexity
- Faster scoring
- Transparent coefficients and odds ratios
- Clearer explanations for business stakeholders

The model is intended to prioritize retention outreach rather than make definitive predictions about whether an individual customer will churn.

## Major Churn Drivers

The strongest relationships identified by the Logistic Regression model included:

### Factors associated with increased churn risk

- Month-to-month contracts
- More customer complaints
- More service calls
- Late payments
- Lack of technical support
- Lack of online security
- Low customer satisfaction
- High monthly charges

### Factors associated with decreased churn risk

- Two-year contracts
- Higher customer satisfaction
- Technical-support enrollment
- More subscribed services
- Online-security enrollment
- Longer customer tenure

Because the dataset is synthetic, these findings describe relationships within this project dataset and should not be treated as universal telecom-industry conclusions.

## Recommended Retention Actions

| Primary Risk Indicator | Recommended Action |
|---|---|
| Poor customer experience | Service-recovery call and issue resolution |
| Month-to-month contract | Offer an annual-contract incentive |
| Late payment activity | Offer payment reminders or flexible billing |
| No technical support | Offer proactive technical-support enrollment |
| No online security | Offer an online-security trial or bundle |
| High monthly charge | Review the customer plan and recommend a lower-cost option |
| Combined elevated risk | General retention outreach |

The predicted churn probability determines **which customers should be prioritized**. Customer attributes determine **which action should be recommended**.

## Retention Priority Queue

The final model scored the holdout customer population and selected the top 10% highest-risk customers.

Each record contains:

| Column | Description |
|---|---|
| `customer_id` | Synthetic customer identifier |
| `churn_probability` | Predicted probability of churn |
| `risk_tier` | High, medium, or low risk classification |
| `primary_risk_reason` | Main reason selected for outreach |
| `recommended_action` | Suggested retention intervention |

A 100-row demonstration preview is available here:

[`reports/customer_retention_action_preview.csv`](reports/customer_retention_action_preview.csv)

The full customer-level dataset contains synthetic records and is intended only to demonstrate how a retention team could operationalize model output.

## Analytics Workflow

```text
Raw Customer Data
        |
        v
PySpark ETL and Data Cleaning
        |
        v
Feature Engineering
        |
        v
Exploratory Data Analysis
        |
        v
Logistic Regression / Random Forest / XGBoost
        |
        v
Cross-Validation and Model Evaluation
        |
        v
Churn Probability Scoring
        |
        v
Retention Priority Queue
        |
        v
Power BI Dashboard and Business Recommendations
