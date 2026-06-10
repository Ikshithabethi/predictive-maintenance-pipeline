import time
import random
import mysql.connector


def run_sensor_simulation():

    print("🚀 Sensor simulator started...")

    while True:

        try:

            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Frooti1145",
                database="predictive_maintenance_db"
            )

            cursor = mydb.cursor()

            air_temp = round(random.uniform(295, 305), 1)
            process_temp = round(air_temp + random.uniform(10, 15), 1)
            rotational_speed = random.randint(1300, 1800)
            torque = round(random.uniform(20, 60), 1)
            tool_wear = random.randint(0, 250)

            sql = """
            INSERT INTO live_sensor_logs
            (air_temp, process_temp, rotational_speed, torque, tool_wear)
            VALUES (%s,%s,%s,%s,%s)
            """

            values = (
                air_temp,
                process_temp,
                rotational_speed,
                torque,
                tool_wear
            )

            cursor.execute(sql, values)

            mydb.commit()

            print(
                f"Inserted -> Temp:{air_temp}, RPM:{rotational_speed}, Torque:{torque}"
            )

            cursor.close()
            mydb.close()

            time.sleep(3)

        except Exception as e:
            print(e)
            break


if __name__ == "__main__":
    run_sensor_simulation()