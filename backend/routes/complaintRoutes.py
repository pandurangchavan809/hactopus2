from flask import Blueprint, request, jsonify
from utils.db import get_db

complaint_bp = Blueprint('complaint_bp', __name__)

@complaint_bp.route('/submit', methods=['POST'])
def submit_complaint():
    data = request.json
    firebase_uid = data.get('firebase_uid')
    email = data.get('email')
    ctype = data.get('type')
    subject = data.get('subject')
    description = data.get('description')
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO complaints (firebase_uid, email, type, subject, description)
        VALUES (?, ?, ?, ?, ?)
    """, (firebase_uid, email, ctype, subject, description))
    db.commit()
    complaint_id = cur.lastrowid
    cur.close()
    return jsonify({'message': 'Complaint submitted successfully', 'id': complaint_id, 'status': 'pending'}), 201

@complaint_bp.route('/my', methods=['GET'])
def get_user_complaints():
    firebase_uid = request.args.get('firebase_uid')
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM complaints WHERE firebase_uid = ? ORDER BY created_at DESC", (firebase_uid,))
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    complaints = [dict(zip(columns, row)) for row in rows]
    cur.close()
    return jsonify(complaints)

@complaint_bp.route('/all', methods=['GET'])
def get_all_complaints():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM complaints ORDER BY created_at DESC")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    complaints = [dict(zip(columns, row)) for row in rows]
    cur.close()
    return jsonify(complaints)

@complaint_bp.route('/<int:complaint_id>/respond', methods=['POST'])
def respond_to_complaint(complaint_id):
    data = request.json
    ai_response = data.get('ai_response')
    status = data.get('status', 'resolved')
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE complaints SET ai_response = ?, status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
    """, (ai_response, status, complaint_id))
    db.commit()
    cur.close()
    return jsonify({'message': 'Response saved'})
