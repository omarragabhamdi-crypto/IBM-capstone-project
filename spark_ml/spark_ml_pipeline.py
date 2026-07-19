from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
import os

def main():
    print("🚀 Starting Spark ML Pipeline...")
    
    # 1. Initialize Spark Session
    spark = SparkSession.builder \
        .appName("IBM-Capstone-SparkML") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    # 2. Setup Data Path
    data_path = "spark_ml/sample_data.csv"
    if not os.path.exists(data_path):
        print("Creating sample dataset for the project...")
        df_sample = spark.createDataFrame([
            (1, 20.0, 30.0, 100.0),
            (2, 25.0, 35.0, 120.0),
            (3, 30.0, 40.0, 140.0),
            (4, 35.0, 45.0, 160.0),
            (5, 40.0, 50.0, 180.0)
        ], ["id", "feature1", "feature2", "label"])
        df_sample.write.csv(data_path, header=True, mode="overwrite")

    # Load data
    df = spark.read.csv(data_path, header=True, inferSchema=True)
    print("Data loaded successfully.")


    # 3. Feature Engineering
    assembler = VectorAssembler(inputCols=["feature1", "feature2"], outputCol="features")
    output = assembler.transform(df)

    # 4. Feature Scaling
    scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures", withStd=True, withMean=False)
    scaler_model = scaler.fit(output)
    final_data = scaler_model.transform(output)

    # Split Data
    train_data, test_data = final_data.randomSplit([0.8, 0.2], seed=42)

    # 5. Model Training
    print("Training Linear Regression Model...")
    lr = LinearRegression(featuresCol="scaledFeatures", labelCol="label")
    lr_model = lr.fit(train_data)

    # 6. Evaluation
    predictions = lr_model.transform(test_data)
    evaluator_rmse = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="rmse")
    evaluator_r2 = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="r2")
    
    print(f"📉 RMSE = {evaluator_rmse.evaluate(predictions)}")
    print(f"📊 R2 = {evaluator_r2.evaluate(predictions)}")

    # 7. Save the Model
    model_save_path = "spark_ml/linear_regression_model"
    lr_model.write().overwrite().save(model_save_path)
    print(f"💾 Model saved to {model_save_path}")

    spark.stop()

if __name__ == "__main__":
    main()
