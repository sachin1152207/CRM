from flask import Blueprint, render_template
from datetime import datetime
from database import get_db
income = Blueprint('income',__name__, template_folder="templates")
from utils import login_required


@income.route('/')
@login_required
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM amount_report")
    amount_report = cursor.fetchone()

    # Today Collection
    cursor.execute("SELECT * FROM records WHERE date(created_at, 'unixepoch', 'localtime') = date('now', 'localtime')")
    today_collection = cursor.fetchall()
    cursor.execute("SELECT SUM(amount) FROM records WHERE date(created_at, 'unixepoch', 'localtime') = date('now', 'localtime')")
    today_collection_amount = cursor.fetchone()[0] or 0

    # Today unpaid
    cursor.execute("SELECT * FROM records WHERE status = 'UNPAID' AND date(created_at, 'unixepoch', 'localtime') = date('now', 'localtime')")
    today_unpaid = cursor.fetchall()
    cursor.execute("SELECT SUM(amount) FROM records WHERE status = 'UNPAID' AND date(created_at, 'unixepoch', 'localtime') = date('now', 'localtime')")
    today_unpaid_amount = cursor.fetchone()[0] or 0
    # Today Paid
    cursor.execute("SELECT * FROM records WHERE status = 'PAID' AND date(created_at, 'unixepoch', 'localtime') = date('now', 'localtime')")
    today_paid = cursor.fetchall()
    cursor.execute("SELECT SUM(amount) FROM records WHERE status = 'PAID' AND date(created_at, 'unixepoch', 'localtime') = date('now', 'localtime')")
    today_paid_amount = cursor.fetchone()[0] or 0
    cursor.close()
    db.close()
    return render_template("income.html", amount_report=amount_report, today_collection=today_collection, today_collection_amount=today_collection_amount, today_unpaid=today_unpaid, today_unpaid_amount=today_unpaid_amount, today_paid=today_paid, today_paid_amount=today_paid_amount)