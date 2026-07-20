from pathlib import Path
from pyspark.sql import SparkSession


def main():
    project_root = Path(__file__).resolve().parents[2]

    raw_path = project_root / "data" / "raw" / "customer_churn_1M.csv"
    parquet_path = project_root / "data" / "parquet" / "customer_churn"

    spark = (
        SparkSession.builder
        .appName("CustomerChurnCSVToParquet")
        .master("local[*]")
        .getOrCreate()
    )

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(raw_path))
    )

    print("Rows:", df.count())
    print("Columns:", len(df.columns))
    df.printSchema()

    (
        df.write
        .mode("overwrite")
        .parquet(str(parquet_path))
    )

    print(f"Saved Parquet files to: {parquet_path}")

    spark.stop()


if __name__ == "__main__":
    main()