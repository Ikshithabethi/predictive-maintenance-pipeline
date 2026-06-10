import streamlit as st
import mysql.connector
import pandas as pd
import joblib
import numpy as np

st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    layout="wide"
)

st.title("🏭 Predictive Maintenance Dashboard")

# Model Accuracy
st.metric("Model Accuracy", "98.75%")

# Load trained model
model = joblib.load("model.pkl")


def get_latest_data():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Frooti1145",
            database="predictive_maintenance_db"
        )

        query = """
        SELECT *
        FROM live_sensor_logs
        ORDER BY id DESC
        LIMIT 1
        """

        df = pd.read_sql(query, mydb)

        mydb.close()

        return df

    except Exception as e:
        st.error(str(e))
        return pd.DataFrame()


if st.button("🔄 Refresh Data"):
    st.rerun()

data = get_latest_data()

if not data.empty:

    row = data.iloc[0]

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Latest Sensor Values")

        st.metric("Air Temp (K)", row["air_temp"])
        st.metric("Process Temp (K)", row["process_temp"])
        st.metric("RPM", row["rotational_speed"])
        st.metric("Torque (Nm)", row["torque"])
        st.metric("Tool Wear (min)", row["tool_wear"])

    with col2:

        X = np.array([[
            row["air_temp"],
            row["process_temp"],
            row["rotational_speed"],
            row["torque"],
            row["tool_wear"]
        ]])

        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0][1]

        st.subheader("Failure Probability")

        chart_data = pd.DataFrame({
            "Metric": ["Failure Risk"],
            "Probability (%)": [probability * 100]
        })

        st.bar_chart(
            chart_data.set_index("Metric")
        )

        st.subheader("Failure Prediction")

        if prediction == 1:
            st.error(
                f"🚨 High Failure Risk ({probability:.2%})"
            )
        else:
            st.success(
                f"✅ Normal Operation ({1 - probability:.2%} confidence)"
            )

else:
    st.warning("No data found in database.")