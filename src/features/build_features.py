from pathlib import Path
import re

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lower, trim, lit


def to_snake_case(name: str) -> str:
    name = name.strip()
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    name = re.sub(r"[^0-9a-zA-Z]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_").lower()


def main():
    project_root = Path(__file__).resolve().parents[2]

    input_path = project_root / "data" / "parquet" / "customer_churn"
    output_path = project_root / "data" / "processed" / "customer_churn_features"

    spark = (
        SparkSession.builder
        .appName("BuildCustomerChurnFeatures")
        .master("local[*]")
        .getOrCreate()
    )

    df = spark.read.parquet(str(input_path))

    # Clean column names
    for old_col in df.columns:
        new_col = to_snake_case(old_col)
        if old_col != new_col:
            df = df.withColumnRenamed(old_col, new_col)

    # Fix known dataset naming differences
    if "tenure_months" not in df.columns and "tenure" in df.columns:
        df = df.withColumnRenamed("tenure", "tenure_months")

    if "monthly_charges" not in df.columns and "monthlycharges" in df.columns:
        df = df.withColumnRenamed("monthlycharges", "monthly_charges")

    if "total_charges" not in df.columns and "totalcharges" in df.columns:
        df = df.withColumnRenamed("totalcharges", "total_charges")

    # Clean string columns
    string_cols = [
        field.name
        for field in df.schema.fields
        if field.dataType.simpleString() == "string"
    ]

    for c in string_cols:
        df = df.withColumn(c, lower(trim(col(c))))

    # Cast useful numeric columns
    numeric_cols = [
        "age",
        "annual_income",
        "dependents",
        "tenure_months",
        "monthly_charges",
        "total_charges",
        "num_services",
        "customer_satisfaction",
        "churn",
    ]

    for c in numeric_cols:
        if c in df.columns:
            df = df.withColumn(c, col(c).cast("double"))

    # Target column
    if "churn" in df.columns:
        df = df.withColumn(
            "churn_label",
            when(lower(trim(col("churn").cast("string"))).isin("yes", "true", "1", "1.0"), 1)
            .when(lower(trim(col("churn").cast("string"))).isin("no", "false", "0", "0.0"), 0)
            .otherwise(col("churn").cast("int"))
        )

    # Feature engineering
    if "tenure_months" in df.columns:
        df = df.withColumn("tenure_years", col("tenure_months") / lit(12))

    if "monthly_charges" in df.columns and "tenure_months" in df.columns:
        df = df.withColumn(
            "monthly_charge_per_tenure",
            col("monthly_charges") / when(col("tenure_months") == 0, lit(1)).otherwise(col("tenure_months"))
        )

    if "monthly_charges" in df.columns:
        df = df.withColumn(
            "is_high_monthly_charge",
            when(col("monthly_charges") >= 80, 1).otherwise(0)
        )

    if "tenure_months" in df.columns:
        df = df.withColumn(
            "is_new_customer",
            when(col("tenure_months") <= 6, 1).otherwise(0)
        )

    if "customer_satisfaction" in df.columns:
        df = df.withColumn(
            "is_low_satisfaction",
            when(col("customer_satisfaction") <= 3, 1).otherwise(0)
        )

    if "num_services" in df.columns:
        df = df.withColumn(
            "is_multi_service_customer",
            when(col("num_services") >= 3, 1).otherwise(0)
        )

    if "contract" in df.columns:
        df = df.withColumn(
            "is_month_to_month",
            when(col("contract").contains("month"), 1).otherwise(0)
        )

    print("Final columns:")
    print(df.columns)

    print("Processed rows:", df.count())
    print("Processed columns:", len(df.columns))
    df.printSchema()

    (
        
        df.coalesce(1)
        .write
        .mode("overwrite")
        .parquet(str(output_path))

    )

    print(f"Saved processed data to: {output_path}")

    spark.stop()


if __name__ == "__main__":
    main()