from flask import Blueprint, request, jsonify
from utils.db import get_db
import openai
import os

ai_bp = Blueprint('ai_bp', __name__)

# Set your OpenAI API key in .env as OPENAI_API_KEY
openai.api_key = os.getenv('OPENAI_API_KEY')

@ai_bp.route('/analyze', methods=['POST'])
def analyze_complaint():
    data = request.json
    complaint_text = data.get('description')
    if not complaint_text:
        return jsonify({'error': 'No complaint description provided'}), 400
    try:
        # Example prompt for GPT-3/4
        prompt = f"Analyze the following complaint and summarize the main problem and possible solutions:\n{complaint_text}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        analysis = response.choices[0].text.strip()
        return jsonify({'analysis': analysis})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
