import os
import uuid
from database import get_db
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, jsonify, send_file
from utils import login_required
expense = Blueprint('expense',__name__, template_folder="templates")


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@expense.route('/')
@login_required
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM amount_report")
    amount_report = cursor.fetchone()
    cursor.execute("SELECT * FROM expense ORDER BY timestamp DESC")
    expense_list = cursor.fetchall()
    return render_template("expense.html", datetime=datetime, amount_report=amount_report, expense_list=expense_list)


@expense.route('/getbilldetails')
@login_required
def get_bill_details():
    db = get_db()
    cursor = db.cursor()
    expense_id = request.args.get('expense_id')

    cursor.execute("SELECT * FROM expense_items WHERE expense_id = ?", (expense_id,))
    expense_items = cursor.fetchall()
    cursor.execute("SELECT * FROM expense WHERE id = ?", (expense_id,))
    expense = cursor.fetchone()
    if not expense_items:
        return jsonify({"status":False,"message": "No items found for this expense."}), 404
    return jsonify({"status":True,"expense_items": [dict(item) for item in expense_items], "expense_details": dict(expense)})


@expense.route('/add_bill', methods=['POST'])
@login_required
def add_bill():
    db = get_db()
    cursor = db.cursor()
    addBillPurpose = request.form.get('addBillPurpose')
    addBillSpentby = request.form.get('addBillSpentby')
    addBillIssuedDate = request.form.get('addBillIssuedDate')
    addBillTotalAmount = int(request.form.get('addBillTotalAmount'))
    addBillImage = request.files['addBillImage']
    addBillRemark = request.form.get('addBillRemark')

    # handling bill image
    if addBillImage.filename != '':
        if allowed_file(addBillImage.filename):
            addBillImage.filename = f"{uuid.uuid4()}.{addBillImage.filename.rsplit('.', 1)[1].lower()}"
            addBillImage.save(os.path.join('static/uploads/expense_bill_image/', secure_filename(addBillImage.filename)))
        else:
            return jsonify({"status": False, "message": "Invalid file type. Only PNG, JPG, and JPEG are allowed."}), 400
    else:
        addBillImage.filename = None
    
    # Grabbing all items from the form
    items = []
    index = 1

    while True:
        name = request.form.get(f"itemName{index}")
        qty = request.form.get(f"itemQuantity{index}") or '-'
        price = request.form.get(f"itemPrice{index}")

        if name is None and price is None:
            break  # No more items

        if name and price:  # Skip if any field is empty
            items.append({
                "name": name.strip(),
                "quantity": qty,
                "price": int(price)
            })

        index += 1
    cursor.execute("INSERT INTO expense (bill_purpose, spent_by, bill_issued_date, spent_amount, bill_image_filename, remarks, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",(addBillPurpose, addBillSpentby, addBillIssuedDate, addBillTotalAmount, addBillImage.filename, addBillRemark, int(datetime.now().timestamp())))
    expense_id = cursor.lastrowid  # Get the last inserted ID
    for item in items:
        cursor.execute("INSERT INTO expense_items (expense_id, itemName, itemQty, itemPrice) VALUES (?, ?, ?, ?)", (expense_id, item["name"], item["quantity"], item["price"]))
    db.commit()

    return jsonify({"status": True, "message": "Bill added successfully.", "addBillpurpose": addBillPurpose, "addBillSpentby": addBillSpentby, "addBillIssuedDate": addBillIssuedDate, "addBillRemark": addBillRemark, "addBillImage":addBillImage.filename,"addBillTotalAmount": addBillTotalAmount, "items": items})

@expense.route('/download_bill', methods=['GET'])
@login_required
def download_bill():
    filename = request.args.get('filename')
    path = f"static/uploads/expense_bill_image/{filename}"
    return send_file(path, as_attachment=True)
