import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os


def train_pipeline():

    csv_path = "data/predictive_maintenance.csv"

    if not os.path.exists(csv_path):
        print("Dataset not found!")
        return

    # Load dataset
    df = pd.read_csv(csv_path)

    # Features
    X = df[
        [
            "Air temperature [K]",
            "Process temperature [K]",
            "Rotational speed [rpm]",
            "Torque [Nm]",
            "Tool wear [min]"
        ]
    ].copy()

    # Rename columns to match simulator/dashboard
    X.columns = [
        "air_temp",
        "process_temp",
        "rotational_speed",
        "torque",
        "tool_wear"
    ]

    # Target
    y = df["Machine failure"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Create model
    model = XGBClassifier(
        n_estimators=100,
        random_state=42,
        eval_metric="logloss"
    )

    # Train model
    model.fit(X_train, y_train)

    # Evaluate model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")

    # Save model
    joblib.dump(model, "model.pkl")

    print("✅ model.pkl created successfully!")


if __name__ == "__main__":
    train_pipeline()