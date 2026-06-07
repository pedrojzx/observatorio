from app import app, aplicar_migrations
from models import db, Usuario
from werkzeug.security import generate_password_hash

aplicar_migrations(app)

with app.app_context():
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
