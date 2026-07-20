# Feature Engineering

## Overview

This project uses a reusable PySpark feature-engineering pipeline to transform the raw customer churn dataset into a consistent, model-ready Parquet dataset.

The pipeline:

1. Loads the source Parquet data.
2. Standardizes column names.
3. resolves known schema differences.
4. Cleans categorical fields.
5. Casts analytical columns to appropriate data types.
6. Creates the binary churn target.
7. Engineers business-relevant churn features.
8. Validates the processed output.
9. Writes the results to compressed Parquet storage.

The feature pipeline is located at:

```text
src/features/build_features.py