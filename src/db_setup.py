import mysql.connector

def initialize_database():

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Frooti1145"
    )

    cursor = mydb.cursor()

    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS predictive_maintenance_db"
    )

    cursor.execute("USE predictive_maintenance_db")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS live_sensor_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        air_temp FLOAT,
        process_temp FLOAT,
        rotational_speed INT,
        torque FLOAT,
        tool_wear INT
    )
    """)

    print("✅ Database ready!")

    cursor.close()
    mydb.close()


if __name__ == "__main__":
    initialize_database()