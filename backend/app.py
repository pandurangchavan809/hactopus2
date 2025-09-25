from flask import Flask
from utils.db import create_app

from routes.complaintRoutes import complaint_bp
from routes.adminRoutes import admin_bp
from routes.aiRoutes import ai_bp

app = create_app()

# Register blueprints

app.register_blueprint(complaint_bp, url_prefix='/api/complaints')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(ai_bp, url_prefix='/api/ai')

@app.route('/')
def home():
    return {'message': 'Flask backend with MySQL is running!'}

if __name__ == '__main__':
    app.run(debug=True)
