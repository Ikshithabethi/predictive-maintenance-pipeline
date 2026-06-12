import streamlit as st
from streamlit_autorefresh import st_autorefresh
import mysql.connector
import pandas as pd
import joblib
import numpy as np

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "signup_success" not in st.session_state:
    st.session_state.signup_success = False
st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    layout="wide"
)

st_autorefresh(
    interval=5000,
    key="datarefresh"
)

# Sidebar
st.sidebar.title("Predictive Maintenance")



if not st.session_state.logged_in:

    default_page = 0

    if st.session_state.signup_success:
        default_page = 0
        st.session_state.signup_success = False

    page = st.sidebar.radio(
        "Navigation",
        [
            "Login",
            "Sign Up"
        ],
        index=default_page
    )

else:

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Analytics",
            "Retrain Model"
        ]
    )

st.sidebar.markdown("---")
st.sidebar.success(" System Online")
st.sidebar.info(" Model: XGBoost")
st.sidebar.info(" Database: MySQL")
st.sidebar.info(" CI/CD: Jenkins")
if st.session_state.logged_in:

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()

# Header
from datetime import datetime

st.write(
    "Last Refresh:",
    datetime.now().strftime("%H:%M:%S")
)


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


def get_history_data():
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
        LIMIT 20
        """

        df = pd.read_sql(query, mydb)

        mydb.close()

        return df

    except Exception as e:
        st.error(str(e))
        return pd.DataFrame()

def get_retraining_history():

    try:

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Frooti1145",
            database="predictive_maintenance_db"
        )

        query = """
        SELECT *
        FROM retraining_logs
        ORDER BY retrained_at DESC
        """

        df = pd.read_sql(query, mydb)

        mydb.close()

        return df

    except Exception as e:

        st.error(str(e))

        return pd.DataFrame()


data = get_latest_data()
history_df = get_history_data()
retrain_df = get_retraining_history()

if page == "Retrain Model":

    st.title("Model Retraining")

    st.write(
        "Retrain the predictive maintenance model using the latest dataset."
    )

    if st.button(" Retrain Model"):

        import os

        result = os.system(
            "python src/retrain.py"
        )

        if result == 0:

            st.success(
                " Model retrained successfully!"
            )

        else:

            st.error(
                "Retraining failed!"
            )

    st.stop()
if page == "Login":

    st.title("Login")

    with st.form("login_form"):

        email = st.text_input(

            "Email",

            placeholder="Enter your company email"

        )

        password = st.text_input(

            "Password",

            type="password",

            placeholder="Enter your password"

        )

        login_button = st.form_submit_button(
            "Login"
        )

    if login_button:

        try:

            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Frooti1145",
                database="predictive_maintenance_db"
            )

            cursor = mydb.cursor()

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE email=%s
                AND password=%s
                """,
                (email, password)
            )

            user = cursor.fetchone()

            mydb.close()

            if user:

                st.session_state.logged_in = True

                st.success(
                    "Login Successful"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Email or Password"
                )

        except Exception as e:

            st.error(str(e))

    st.stop()
if page == "Sign Up":

    st.title(" Sign Up")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Sign Up"):

        try:
            if not username or not email or not password:

                st.error(

                    "All fields are required."

                )

                st.stop()

            if len(password) < 6:

                st.error(

                    "Password must be at least 6 characters."

                )

            st.stop()

            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Frooti1145",
                database="predictive_maintenance_db"
            )

            cursor = mydb.cursor()

            cursor.execute(
                """
                INSERT INTO users
                (username,email,password)
                VALUES (%s,%s,%s)
                """,
                (username,email,password)
            )
            existing_user = cursor.fetchone()

            if existing_user:

                st.error(

                    "Email already registered."

                )

            else:

                cursor.execute(

                    """

                    INSERT INTO users

                    (username,email,password)

                    VALUES (%s,%s,%s)

                    """,

                    (username,email,password)

                )

            mydb.commit()

            st.success(
                "Account created successfully! Redirecting to Login..."
            )

            st.session_state.signup_success = True
            st.rerun()

            mydb.close()

        except Exception as e:

            st.error(str(e))

    st.stop()

if page == "Analytics":

    st.title(" Analytics Dashboard")

    if not history_df.empty:

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Average Air Temp",
                round(history_df["air_temp"].mean(), 2)
            )

            st.metric(
                "Average RPM",
                round(history_df["rotational_speed"].mean(), 0)
            )

        with col2:
            st.metric(
                "Average Torque",
                round(history_df["torque"].mean(), 2)
            )

            st.metric(
                "Average Tool Wear",
                round(history_df["tool_wear"].mean(), 0)
            )

        st.subheader("Sensor Data Table")

        st.dataframe(
            history_df.sort_values("id", ascending=False)
        )
        history_df = history_df.sort_values("id")

        st.subheader(" Air Temperature Trend")
        st.line_chart(
            history_df.set_index("id")["air_temp"]
        )

        st.subheader(" RPM Trend")
        st.line_chart(
            history_df.set_index("id")["rotational_speed"]
        )

        st.subheader(" Torque Trend")
        st.line_chart(
            history_df.set_index("id")["torque"]
        )

        st.subheader(" Tool Wear Trend")
        st.line_chart(
            history_df.set_index("id")["tool_wear"]
        )
        st.subheader(" Model Retraining History")

        if not retrain_df.empty:

            st.dataframe(
                retrain_df
            )

        else:

            st.info(
                "No retraining history available."
            )

    st.stop()
if page == "Dashboard":

    # Top Metrics
    colA, colB, colC = st.columns(3)

    with colA:
        st.metric(" Model Accuracy", "98.75%")

    with colB:
        st.metric(" Model", "XGBoost")

    with colC:
        st.metric(" Database", "MySQL")
    
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

            st.subheader("⚠️ Failure Risk Score")

            risk_percent = int(probability * 100)

            st.progress(risk_percent)

            st.metric(
                "Failure Risk",
                f"{risk_percent}%"
            )

            if risk_percent < 30:
                st.success(" Low Risk")

            elif risk_percent < 70:
                st.warning(" Medium Risk")

            else:
                st.error(" High Risk")

            st.subheader("Failure Prediction")

            if prediction == 1:
                st.error(
                    f" High Failure Risk ({probability:.2%})"
                )
            else:
                st.success(
                    f"Normal Operation ({1 - probability:.2%} confidence)"
                )

    # Historical Trend Chart
    # Historical Trend Charts
    

else:
    st.warning("No data found in database.")