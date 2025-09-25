from flask import Blueprint, request, jsonify
from utils.db import get_db

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/complaints', methods=['GET'])
def get_all_complaints():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM complaints ORDER BY created_at DESC")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    complaints = [dict(zip(columns, row)) for row in rows]
    cur.close()
    return jsonify(complaints)

@admin_bp.route('/complaints/<int:complaint_id>/respond', methods=['POST'])
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
