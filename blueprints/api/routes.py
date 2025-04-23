from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from database import get_db

api = Blueprint('api', __name__, template_folder="templates")

# Helper function to get the amount_summary_report
def get_amount_summary_report():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT SUM(amount) FROM records WHERE status='PAID'")
    paid_amount = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM records WHERE status='UNPAID'")
    unpaid_amount = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM records")
    total_collection = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(spent_amount) FROM expense")  # Updated to correct column name
    total_expense = cursor.fetchone()[0] or 0  # Fetching total expense from the query
    current_balance = paid_amount - total_expense  # Calculating current balance


    cursor.execute("UPDATE amount_report SET current_balance=?, total_expense=?, total_collection=?, total_paid=?, total_unpaid=?, last_updated=? WHERE id=1", (current_balance, total_expense, total_collection, paid_amount, unpaid_amount, int(datetime.now().timestamp()))) 

    db.commit()
    return {
        "paid_amount": paid_amount,
        "unpaid_amount": unpaid_amount,
        "total_collection": total_collection,
        "current_balance": current_balance,  
        "total_expense": total_expense,
        "last_updated":int(datetime.now().timestamp())
    }


@api.route('/')
def index():
    return jsonify({"status": "API is working!"})

@api.route('/get_balance', methods=['GET'])
def current_balance():
    amount_summary = get_amount_summary_report()
    return jsonify(amount_summary), 200


