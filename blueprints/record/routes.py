from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from database import get_db
record = Blueprint('record',__name__, template_folder="templates")
from utils import login_required


@record.route('/')
@login_required
def index():
    db = get_db()
    cursor = db.cursor()
    
    sort_by = request.args.get('sort_by', 'newest')
    query = "SELECT * FROM records"
    params = []

    if sort_by == 'today':
        today = datetime.now().strftime('%Y-%m-%d')
        query += " WHERE date(created_at, 'unixepoch') = ?"
        params.append(today)
    elif sort_by == 'paid':
        query += " WHERE status = ?"
        params.append('PAID')
    elif sort_by == 'unpaid':
        query += " WHERE status = ?"
        params.append('UNPAID')
    elif sort_by == 'cash':
        query += " WHERE payment_mode = ?"
        params.append('CASH')
    elif sort_by == 'online':
        query += " WHERE payment_mode = ?"
        params.append('ONLINE')

    query += " ORDER BY id DESC"  # Sort newest first

    cursor.execute("SELECT * FROM amount_report")
    amount_report = cursor.fetchone()

    cursor.execute(query, params)
    records = cursor.fetchall()

    return render_template("record.html", record=records, datetime=datetime, amount_report=amount_report)


@record.route('/getbyid', methods=['GET'])
@login_required
def get_by_id():
    db = get_db()
    cursor = db.cursor()
    record_id = request.args.get('id')
    cursor.execute("SELECT * FROM records WHERE id=?", (record_id,))
    record = cursor.fetchone()
    if record is None:
        return jsonify({"error": "Record not found"}), 404
    return jsonify({
        "id": record[0],
        "name": record[1],
        "amount": record[2],
        "created_at": record[3],
        "paid_at": record[5],
        "status": record[4],
        "payment_mode": record[6],
        "remarks": record[7],
        "is_editable": record[8],
    })
    
@record.route('/add', methods=['POST'])
@login_required
def add_record():
    db = get_db()
    cursor = db.cursor()
    name = request.form.get('donorName')
    amount = int(request.form.get('donorAmount'))
    created_at = int(datetime.now().timestamp())  #get current timestamp
    status = request.form.get('donorPaymentStatus')
    if status == 'PAID':
        paid_at = created_at  #get current timestamp
    paid_at = None if status == 'UNPAID' else created_at
    payment_mode = "UNPAID" if status == 'UNPAID' else request.form.get('donorPaymentMode')
    remarks = "Jay mata di" if request.form.get('donorRemarks') == "" else request.form.get('donorRemarks')
    is_editable = "TRUE" if status == 'UNPAID' else "FALSE"
    cursor.execute("INSERT INTO records (name, amount, created_at, paid_at, status, payment_mode, remarks, is_editable) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(name, amount, created_at, paid_at, status, payment_mode, remarks, is_editable))
    db.commit()
    return jsonify({"status": True})


@record.route('/update', methods=['POST'])
@login_required
def update_record():
    db = get_db()
    cursor = db.cursor()
    record_id = request.form.get('donorId')
    name = request.form.get('donorName')
    amount = int(request.form.get('donorAmount'))
    paid_at = int(datetime.now().timestamp())
    remarks = request.form.get('donorRemarks')
    status = request.form.get('donorPaymentStatus')
    payment_mode = "UNPAID" if status == 'UNPAID' else request.form.get('donorPaymentMode')
    is_editable = "TRUE" if status == 'UNPAID' else "FALSE"

    cursor.execute("UPDATE records SET name=?, amount=?, paid_at=?, status=?, payment_mode=?, remarks=?, is_editable=? WHERE id=?", (name, amount, paid_at, status, payment_mode, remarks, is_editable, record_id))
    db.commit()

    return jsonify({"status": True, "name": name, "amount": amount, "paid_at": paid_at, "payment_mode": payment_mode, "remarks": remarks, "is_editable": is_editable})


@record.route('/search', methods=['POST'])
@login_required
def search_record():
    db = get_db()
    cursor = db.cursor()
    search_query = request.form.get('searchQuery')
    cursor.execute("SELECT * FROM records WHERE name LIKE ?", ('%' + search_query + '%',))
    records = cursor.fetchall()
    result = [dict(row) for row in records]
    if not records:
        return jsonify({"status": False, "error": {"message": "No records found"}}), 404
        return jsonify({"status": False, "error": {"message": "No records found"}}), 404
    return jsonify({"status": True, "data": result})
