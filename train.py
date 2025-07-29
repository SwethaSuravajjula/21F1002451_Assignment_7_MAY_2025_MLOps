import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
from google.cloud import storage

def upload_to_gcs(local_path: str, bucket_name: str, destination_blob_name: str):
    """
    Uploads a file to Google Cloud Storage.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_path)
    print(f"Model uploaded to gs://{bucket_name}/{destination_blob_name}")


def main():
    # Configuration
    GCS_BUCKET = os.getenv('GCS_BUCKET', 'iris_models_storage')
    MODEL_LOCAL_PATH = 'iris_model.joblib'
    MODEL_GCS_PATH = 'models/iris_model.joblib'

    # Load the Iris dataset
    df = pd.read_csv('iris.csv')
    X = df.drop('species', axis=1)
    y = df['species']

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train the Decision Tree classifier
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)

    # Save the trained model locally
    joblib.dump(clf, MODEL_LOCAL_PATH)
    print(f"Model saved locally to {MODEL_LOCAL_PATH}")

    # Upload the model to Google Cloud Storage
    upload_to_gcs(MODEL_LOCAL_PATH, GCS_BUCKET, MODEL_GCS_PATH)

    # Evaluate on the test set
    y_pred = clf.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))


if __name__ == '__main__':
    main()
