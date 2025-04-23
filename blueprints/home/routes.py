from flask import Blueprint, render_template
from database import get_db
from utils import login_required
home = Blueprint('home',__name__, template_folder="templates")



@home.route('/')
@login_required
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM amount_report")
    amount_report = cursor.fetchone()
    cursor.execute("SELECT * FROM records WHERE status = 'PAID' ORDER BY amount DESC LIMIT 5")
    top_paid = cursor.fetchall()
    cursor.execute("SELECT * FROM expense ORDER BY timestamp DESC LIMIT 5")
    recent_expenses = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM records")
    total_records = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return render_template("index.html", amount_report=amount_report, top_paid=top_paid, recent_expenses=recent_expenses, total_records=total_records)