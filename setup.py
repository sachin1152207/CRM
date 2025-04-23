import sqlite3
import json
import os
def get_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print(" This field cannot be empty. Please enter a valid value.\n")
import sqlite3

def create_database(db_name):
    sql_script = """
        CREATE TABLE "amount_report" (
        "id"	INTEGER,
        "current_balance"	INTEGER,
        "total_collection"	INTEGER,
        "total_expense"	INTEGER,
        "total_paid"	INTEGER,
        "total_unpaid"	INTEGER,
        "last_updated"	INTEGER,
        PRIMARY KEY("id" AUTOINCREMENT)
    );
    INSERT INTO "amount_report" VALUES (1,0,0,0,0,0,0);
    CREATE TABLE "expense" (
        "id"	INTEGER,
        "bill_purpose"	TEXT,
        "spent_by"	TEXT,
        "bill_issued_date"	TEXT,
        "bill_image_filename"	TEXT,
        "spent_amount"	INTEGER,
        "remarks"	TEXT,
        "timestamp"	INTEGER,
        PRIMARY KEY("id" AUTOINCREMENT)
    );

    CREATE TABLE "expense_items" (
        "id"	INTEGER,
        "expense_id"	INTEGER,
        "itemName"	TEXT,
        "itemQty"	TEXT,
        "itemPrice"	INTEGER,
        PRIMARY KEY("id" AUTOINCREMENT)
    );

    CREATE TABLE "records" (
        "id"	INTEGER,
        "name"	TEXT,
        "amount"	INTEGER,
        "created_at"	INTEGER,
        "status"	TEXT,
        "paid_at"	INTEGER,
        "payment_mode"	TEXT,
        "remarks"	TEXT,
        "is_editable"	TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)
    );
    """
    try:
        # Connect to SQLite (creates the database file if it doesn't exist)
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        # Execute the provided SQL code
        cursor.executescript(sql_script)

        # Commit changes and close the connection
        connection.commit()
        connection.close()
        print(f"SQL code executed successfully on '{db_name}'.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")



def setup():
    print("-" * 70)
    print("           Welcome to CRM081 Record Management Setup")
    print("-" * 70)
    print(" This script will collect your database and company information.\n")

    database_name = get_input(" Enter the name of the database file (e.g., crm.db): ")
    username = get_input(" Enter the username for the login: ")
    password = get_input(" Enter the password for the login: ")
    fiscal_year = get_input(" Enter the fiscal year (e.g., 2080): ")
    company_name = get_input(" Enter the company name: ")
    company_address = get_input(" Enter the company address: ")
    company_phone = get_input(" Enter the company phone number: ")
    company_email = get_input(" Enter the company email: ")

    data = {
        'database': database_name,
        'username': username,
        'password': password,
        'fiscal_year': fiscal_year,
        'company_name': company_name,
        'company_address': company_address,
        'company_phone': company_phone,
        'company_email': company_email
    }
    # Writing Config file
    with open("config.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    print("\n Configuration file 'config.json' created successfully.")
    # Creating uploads directory
    if not os.path.exists('./static/uploads/expense_bil_image'):
        os.makedirs('./static/uploads/expense_bil_image')

    # Create the database and tables
    create_database(database_name)
    print("Database and tables created successfully. named:", database_name)
    print("Your username is :", username)
    print("Your password is :", password)
    print("Uploads directory created successfully.")


# Run the setup and print the result
user_data = setup()
print("Setup completed successfully.")
print("Now, start the server")