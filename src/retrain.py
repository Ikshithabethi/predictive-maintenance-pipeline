import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import mysql.connector

def retrain_model():

    df = pd.read_csv(
        "data/predictive_maintenance.csv"
    )

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

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Frooti1145",
    database="predictive_maintenance_db"
)

    cursor = mydb.cursor()

    cursor.execute(
        """
        INSERT INTO retraining_logs
        (accuracy)
        VALUES (%s)
        """,
        (float(accuracy * 100),)
    )

    mydb.commit()
    mydb.close()

    joblib.dump(
        model,
        "model.pkl"
    )

    print(
        f"Model retrained successfully"
    )

    print(
        f"Accuracy: {accuracy:.4f}"
    )

if __name__ == "__main__":
    retrain_model()