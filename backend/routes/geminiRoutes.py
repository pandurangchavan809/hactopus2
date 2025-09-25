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
    if not complaint_type:
        return jsonify({'error': 'No complaint type provided'}), 400
    prompt = f"Suggest 4 clear actions a user can take for a '{complaint_type}' complaint. Format as a numbered list."
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
        # Defensive parsing for Gemini response
        ai_text = ''
        if 'candidates' in result and result['candidates']:
            candidate = result['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content'] and candidate['content']['parts']:
                ai_text = candidate['content']['parts'][0].get('text', '')
        if not ai_text:
            return jsonify({'suggestions': [], 'error': 'AI could not generate suggestions. Try again.'})
        # Parse numbered list or bullet points
        suggestions = []
        for line in ai_text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove leading number/bullet
                suggestions.append(line.lstrip('0123456789.-) ').strip())
            elif line:
                suggestions.append(line)
        if not suggestions:
            suggestions = [ai_text]
        return jsonify({'suggestions': suggestions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
