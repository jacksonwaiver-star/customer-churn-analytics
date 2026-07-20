# Model Evaluation and Selection

## Evaluation Strategy

The models were compared using 5-fold stratified cross-validation because
the churn target was heavily imbalanced.

Primary metrics:

- PR-AUC
- Recall
- Precision
- F2 score
- ROC-AUC
- Matthews correlation coefficient

## Model Comparison

| Model | Precision | Recall | F2 | ROC-AUC | PR-AUC | MCC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.1583 | 0.6369 | 0.3969 | 0.6846 | 0.2035 | 0.1611 |
| Random Forest | 0.1551 | 0.6513 | 0.3972 | 0.6812 | 0.1998 | 0.1579 |
| XGBoost | 0.1601 | 0.6344 | 0.3984 | 0.6858 | 0.2047 | 0.1639 |

## Final Model

Logistic Regression was selected because it performed comparably to the
tuned Random Forest and XGBoost models while providing greater
interpretability and lower deployment complexity.

## Holdout Performance

- Recall: 63.69%
- Precision: 15.83%
- PR-AUC: 0.2035
- ROC-AUC: 0.6846
- F2 score: 0.3969
- Lift at the selected threshold: approximately 1.6x
- True positives: 12,639
- False negatives: 7,206

The model is intended to rank customers for retention outreach rather
than make definitive churn classifications.