import io
import csv
from database import get_db
from datetime import datetime
from utils import login_required
from flask import Blueprint, render_template, Response

reports = Blueprint('reports',__name__, template_folder="templates")

@reports.route('/')
@login_required
def index():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM records")
    total_records = cursor.fetchone()[0]

    cursor.execute("""
        SELECT id, name AS title, amount, paid_at AS date, 'Income' AS type FROM records WHERE status = 'PAID' UNION ALL SELECT id, bill_purpose AS title, spent_amount AS amount, timestamp AS date, 'Expense' AS type FROM expense ORDER BY date ASC;
    """)
    transactions = cursor.fetchall()

    balance = 0
    total_income = 0
    total_expense = 0
    all_reports = []
    #Calculate balance and prepare report data 
    for row in transactions:
        amount = row["amount"]
        if row["type"] == 'Expense':
            amount = -amount
            total_expense += abs(amount)  # sum as positive
        else:
            total_income += amount
        balance += amount
        all_reports.append(dict(row) | {"balance": balance})
    final_summary = {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    }
    cursor.close()
    db.close()

    return render_template("reports.html", total_records=total_records, all_reports=all_reports, datetime=datetime, final_summary=final_summary)




@reports.route('/export')
@login_required
def export_csv():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, name AS title, amount, paid_at AS date, 'Income' AS type FROM records WHERE status = 'PAID'
        UNION ALL
        SELECT id, bill_purpose AS title, spent_amount AS amount, timestamp AS date, 'Expense' AS type FROM expense
        ORDER BY date ASC;
    """)
    transactions = cursor.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    # Write Header
    writer.writerow(['S NO', 'Title', 'Date', 'Credit', 'Debit', 'Balance'])

    balance = 0
    serial = 1
    total_income = 0
    total_expense = 0

    # Write Ledger Rows
    for row in transactions:
        amount = row["amount"]
        credit = ''
        debit = ''

        if row["type"] == 'Expense':
            debit = amount
            balance -= amount
            total_expense += amount
        else:
            credit = amount
            balance += amount
            total_income += amount

        writer.writerow([
            serial,
            row["title"],
            datetime.fromtimestamp(row["date"]).strftime('%Y-%m-%d'),
            credit,
            debit,
            balance
        ])
        serial += 1

    # Add Summary
    writer.writerow([])
    writer.writerow(['Total Income', total_income])
    writer.writerow(['Total Expense', total_expense])
    writer.writerow(['Final Balance', balance])

    output.seek(0)
    cursor.close()
    db.close()

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=CRM_Statement.csv"}
    )