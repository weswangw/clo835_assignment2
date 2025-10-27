from flask import Flask, render_template, request
import os
import pymysql
from pymysql import connections

app = Flask(__name__)

# Environment variables
DBHOST = os.environ.get("DBHOST", "localhost")
DBPORT = int(os.environ.get("DBPORT", 3306))
DBUSER = os.environ.get("DBUSER", "root")
DBPWD = os.environ.get("DBPWD", "password")
DATABASE = os.environ.get("DATABASE", "employees")
APP_COLOR = os.environ.get("APP_COLOR", "blue")

# Function to create a DB connection safely when needed
def get_db_conn():
    try:
        conn = connections.Connection(
            host=DBHOST,
            port=DBPORT,
            user=DBUSER,
            password=DBPWD,
            db=DATABASE
        )
        return conn
    except Exception as e:
        print(f"⚠️ Database connection failed: {e}")
        return None


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('addemp.html', color=APP_COLOR)


@app.route("/about", methods=["GET"])
def about():
    return render_template('about.html', color=APP_COLOR)


@app.route("/addemp", methods=["POST"])
def add_employee():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']

    conn = get_db_conn()
    if conn is None:
        return render_template("error.html", message="Database connection failed. Please try again later.", color=APP_COLOR)

    insert_sql = "INSERT INTO employee (name, email, phone, address) VALUES (%s, %s, %s, %s)"
    cursor = conn.cursor()
    try:
        cursor.execute(insert_sql, (name, email, phone, address))
        conn.commit()
    except Exception as e:
        print(f"Error inserting employee: {e}")
        return render_template("error.html", message=str(e), color=APP_COLOR)
    finally:
        cursor.close()
        conn.close()

    return render_template('addemp.html', color=APP_COLOR)


@app.route("/getemp", methods=["GET"])
def get_employee():
    conn = get_db_conn()
    if conn is None:
        return render_template("error.html", message="Database connection failed. Please try again later.", color=APP_COLOR)

    select_sql = "SELECT * FROM employee"
    cursor = conn.cursor()
    try:
        cursor.execute(select_sql)
        employees = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching employees: {e}")
        employees = []
    finally:
        cursor.close()
        conn.close()

    return render_template("getemp.html", color=APP_COLOR, employees=employees)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
