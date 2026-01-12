import mlflow

with mlflow.start_run():
    mlflow.log_param("check", "dagshub")
    mlflow.log_metric("accuracy", 0.95)

print("MLflow test run logged")
