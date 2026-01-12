import os
import tensorflow as tf
from pathlib import Path
from cnnClassifier.entity.config_entity import TrainingConfig
from cnnClassifier import logger
import mlflow
import mlflow.keras
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.setup_mlflow()

    def setup_mlflow(self):
        """Setup MLflow tracking"""
        mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
        mlflow_tracking_username = os.getenv("MLFLOW_TRACKING_USERNAME")
        mlflow_tracking_password = os.getenv("MLFLOW_TRACKING_PASSWORD")

        if mlflow_tracking_uri:
            mlflow.set_tracking_uri(mlflow_tracking_uri)
            if mlflow_tracking_username and mlflow_tracking_password:
                os.environ["MLFLOW_TRACKING_USERNAME"] = mlflow_tracking_username
                os.environ["MLFLOW_TRACKING_PASSWORD"] = mlflow_tracking_password
            logger.info(f"MLflow tracking URI set to: {mlflow_tracking_uri}")
        else:
            logger.warning("MLFLOW_TRACKING_URI not found in environment variables. Using local tracking.")

    def get_base_model(self):
        self.model = tf.keras.models.load_model(
            self.config.updated_base_model_path
        )

    def train_valid_generator(self):

        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split=0.30
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )

        if self.config.params_is_augmentation:
            train_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range=40,
                horizontal_flip=True,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                **datagenerator_kwargs
            )
        else:
            train_datagenerator = valid_datagenerator

        self.train_generator = train_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="training",
            shuffle=True,
            **dataflow_kwargs
        )

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)

    def train(self):
        self.steps_per_epoch = self.train_generator.samples // self.train_generator.batch_size
        self.validation_steps = self.valid_generator.samples // self.valid_generator.batch_size

        # Create MLflow callback for logging metrics
        mlflow_callback = tf.keras.callbacks.LambdaCallback(
            on_epoch_end=lambda epoch, logs: self.log_epoch_metrics(epoch, logs)
        )

        # Start MLflow run
        with mlflow.start_run():
            # Log parameters
            mlflow.log_param("epochs", self.config.params_epochs)
            mlflow.log_param("batch_size", self.config.params_batch_size)
            mlflow.log_param("image_size", self.config.params_image_size)
            mlflow.log_param("is_augmentation", self.config.params_is_augmentation)
            mlflow.log_param("learning_rate", getattr(self.config, 'params_learning_rate', 'default'))

            # Train the model
            history = self.model.fit(
                self.train_generator,
                epochs=self.config.params_epochs,
                steps_per_epoch=self.steps_per_epoch,
                validation_steps=self.validation_steps,
                validation_data=self.valid_generator,
                callbacks=[mlflow_callback]
            )

            # Log final metrics
            final_loss = history.history['loss'][-1]
            final_accuracy = history.history['accuracy'][-1]
            final_val_loss = history.history['val_loss'][-1]
            final_val_accuracy = history.history['val_accuracy'][-1]

            mlflow.log_metric("final_loss", final_loss)
            mlflow.log_metric("final_accuracy", final_accuracy)
            mlflow.log_metric("final_val_loss", final_val_loss)
            mlflow.log_metric("final_val_accuracy", final_val_accuracy)

            # Log the trained model
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
            if tracking_url_type_store != "file":
                mlflow.keras.log_model(self.model, "model", registered_model_name="KidneyDiseaseModel")
            else:
                mlflow.keras.log_model(self.model, "model")

            logger.info("Model training completed and logged to MLflow")

        self.save_model(
            path=self.config.trained_model_path,
            model=self.model
        )

    def log_epoch_metrics(self, epoch, logs):
        """Log metrics for each epoch to MLflow"""
        mlflow.log_metric("train_loss", logs.get('loss'), step=epoch)
        mlflow.log_metric("train_accuracy", logs.get('accuracy'), step=epoch)
        if 'val_loss' in logs:
            mlflow.log_metric("val_loss", logs.get('val_loss'), step=epoch)
        if 'val_accuracy' in logs:
            mlflow.log_metric("val_accuracy", logs.get('val_accuracy'), step=epoch)