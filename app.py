from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, Usuario

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

from routes.auth import auth_bp
from routes.projetos import projetos_bp
from routes.admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(projetos_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Cria admin padrão se não existir
        from werkzeug.security import generate_password_hash
        admin = Usuario.query.filter_by(email='admin@senac.br').first()
        if not admin:
            admin = Usuario(
                nome='Administrador',
                email='admin@senac.br',
                senha=generate_password_hash('admin123'),
                perfil='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin criado: admin@senac.br / admin123")
    app.run(debug=True)
