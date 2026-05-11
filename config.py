import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'observatorio-senac-secret-2026'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:teste1-@localhost/observatorio_pi'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf', 'zip', 'rar', 'png', 'jpg', 'jpeg', 'docx'}
