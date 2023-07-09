
import mysql.connector
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
sql_username = os.getenv("SQL_USERNAME")
sql_password = os.getenv("SQL_PASSWORD")
sql_hostname = os.getenv("SQL_HOSTNAME")
sql_port = os.getenv("SQL_PORT")
database_name = os.getenv("DATABASE_NAME")


# Establish a connection to the MySQL server
connection = mysql.connector.connect(
    host=sql_hostname,
    user=sql_username,
    password=sql_password,
    database=database_name,
    port=sql_port
)

cursor = connection.cursor()


check_db_query = f"SHOW DATABASES LIKE '{database_name}'"
cursor.execute(check_db_query)
exists = cursor.fetchone()
if not exists:
    create_db_query = f"CREATE DATABASE {database_name}"
    cursor.execute(create_db_query)


check_table_query = "SHOW TABLES LIKE 'Customers'"
cursor.execute(check_table_query)
exists = cursor.fetchone()

if not exists:
    create_table_query = """
CREATE TABLE Customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100),
    address VARCHAR(255),
    phone_number VARCHAR(50)
)
"""
    cursor.execute(create_table_query)


cursor.close()
connection.close()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    connection = mysql.connector.connect(
        host=sql_hostname,
        user=sql_username,
        password=sql_password,
        database=database_name,
        port=sql_port
    )
    cursor = connection.cursor()

    if request.method == "POST":
        if "name" in request.form and "email" in request.form and "address" in request.form and "phone_number" in request.form:
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            phone_number = request.form["phone_number"]

            cursor = connection.cursor()
            insert_query = "INSERT INTO Customers (name, email, address, phone_number) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (name, email, address, phone_number))
            connection.commit()

            select_query = "SELECT * FROM Customers"
            cursor.execute(select_query)
            customers = cursor.fetchall()
            cursor.close()

            message = "Customer inserted successfully!"
            return render_template("index.html", message=message, customers=customers)

        elif "customer_id" in request.form and "new_address" in request.form:
            customer_id = request.form["customer_id"]
            new_address = request.form["new_address"]

            cursor = connection.cursor()
            update_query = "UPDATE Customers SET address = %s WHERE id = %s"
            cursor.execute(update_query, (new_address, customer_id))
            connection.commit()
            cursor.close()

            update_message = "Customer updated successfully!"
            return render_template("index.html", update_message=update_message)

        elif "query" in request.form:
            query = request.form["query"]

            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()

            return render_template("index.html", result=result)

    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
