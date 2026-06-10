import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import joblib
import os


def train_pipeline():

    csv_path = "data/predictive_maintenance.csv"

    if not os.path.exists(csv_path):
        print("Dataset not found!")
        return

    df = pd.read_csv(csv_path)

    X = df[
        [
            "Air temperature [K]",
            "Process temperature [K]",
            "Rotational speed [rpm]",
            "Torque [Nm]",
            "Tool wear [min]"
        ]
    ].copy()

    X.columns = [
        "air_temp",
        "process_temp",
        "rotational_speed",
        "torque",
        "tool_wear"
    ]

    y = df["Machine failure"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = XGBClassifier(
        n_estimators=100,
        random_state=42,
        eval_metric="logloss"
    )

    model.fit(X_train, y_train)

    joblib.dump(model, "model.pkl")

    print("✅ model.pkl created successfully!")


if __name__ == "__main__":
    train_pipeline()