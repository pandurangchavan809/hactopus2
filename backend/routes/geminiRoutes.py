from utils.db import get_db
from flask import Blueprint, request, jsonify
import requests
import os

gemini_bp = Blueprint('gemini_bp', __name__)

from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

@gemini_bp.route('/suggest', methods=['POST'])
def get_gemini_suggestions():
    data = request.json
    complaint_type = data.get('complaintType')
    user_id = data.get('user_id', 'default')
    session_id = data.get('session_id', 'default')
    if not complaint_type:
        return jsonify({'error': 'No complaint type provided'}), 400
    db = get_db()
    cur = db.cursor()
    # Store user message with user/session
    cur.execute("INSERT INTO chat_history (user_id, session_id, sender, message) VALUES (?, ?, ?, ?)", (user_id, session_id, 'user', complaint_type))
    db.commit()
    # Retrieve last 5 messages for memory
    cur.execute("SELECT sender, message FROM chat_history WHERE user_id=? AND session_id=? ORDER BY created_at DESC LIMIT 5", (user_id, session_id))
    history = cur.fetchall()
    history_text = ''
    for row in reversed(history):
        history_text += f"{row['sender']}: {row['message']}\n"
    prompt = f"This is your previous chat:\n{history_text}\nNow, suggest 4 clear actions a user can take for a '{complaint_type}' complaint. Format as a numbered list."
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(
            f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        result = response.json()
        ai_text = ''
        if 'candidates' in result and result['candidates']:
            candidate = result['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content'] and candidate['content']['parts']:
                ai_text = candidate['content']['parts'][0].get('text', '')
        if not ai_text:
            cur.execute("INSERT INTO chat_history (sender, message) VALUES (?, ?)", ('ai', 'AI could not generate suggestions. Try again.'))
            db.commit()
            return jsonify({'suggestions': [], 'error': 'AI could not generate suggestions. Try again.'})
        suggestions = []
        for line in ai_text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                suggestions.append(line.lstrip('0123456789.-) ').strip())
            elif line:
                suggestions.append(line)
        if not suggestions:
            suggestions = [ai_text]
        cur.execute("INSERT INTO chat_history (user_id, session_id, sender, message) VALUES (?, ?, ?, ?)", (user_id, session_id, 'ai', ' '.join(suggestions)))
        db.commit()
        return jsonify({'suggestions': suggestions})
    except Exception as e:
        cur.execute("INSERT INTO chat_history (user_id, session_id, sender, message) VALUES (?, ?, ?, ?)", (user_id, session_id, 'ai', str(e)))
        db.commit()
        return jsonify({'error': str(e)}), 500
