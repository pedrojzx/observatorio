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
from routes.lgpd import lgpd_bp
from routes.portfolio import portfolio_bp

app.register_blueprint(auth_bp)
app.register_blueprint(projetos_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(lgpd_bp)
app.register_blueprint(portfolio_bp)


def aplicar_migrations(app):
    """Adiciona colunas faltantes sem apagar dados existentes."""
    with app.app_context():
        db.create_all()

        migrations = [
            # tabela, coluna, definição SQL
            ("usuarios",   "turno",               "ENUM('manha','tarde','noite') NULL"),
            ("usuarios",   "turma",               "VARCHAR(50) NULL"),
            ("usuarios",   "criado_em",            "DATETIME DEFAULT CURRENT_TIMESTAMP"),
            # Colunas da rubrica de avaliação
            ("avaliacoes", "nota_funcionalidade",  "FLOAT NULL"),
            ("avaliacoes", "nota_codigo",          "FLOAT NULL"),
            ("avaliacoes", "nota_documentacao",    "FLOAT NULL"),
            ("avaliacoes", "nota_interface",       "FLOAT NULL"),
            ("avaliacoes", "nota_apresentacao",    "FLOAT NULL"),
            ("projetos",   "participantes",           "TEXT NULL"),
        ]

        # Garantir que o ENUM de perfil inclui 'empresa'
        with db.engine.connect() as conn_enum:
            try:
                conn_enum.execute(db.text(
                    "ALTER TABLE usuarios MODIFY COLUMN perfil "
                    "ENUM('aluno','professor','admin','empresa') NOT NULL DEFAULT 'aluno'"
                ))
                conn_enum.commit()
            except Exception:
                pass  # Já existe ou banco não suporta

        with db.engine.connect() as conn:
            for tabela, coluna, definicao in migrations:
                resultado = conn.execute(
                    db.text(
                        "SELECT COUNT(*) FROM information_schema.columns "
                        "WHERE table_schema = DATABASE() "
                        "AND table_name = :t AND column_name = :c"
                    ),
                    {"t": tabela, "c": coluna}
                ).scalar()

                if resultado == 0:
                    conn.execute(db.text(
                        f"ALTER TABLE {tabela} ADD COLUMN {coluna} {definicao}"
                    ))
                    conn.commit()
                    print(f"[migration] Coluna '{coluna}' adicionada em '{tabela}'.")
                else:
                    print(f"[migration] '{tabela}.{coluna}' já existe, pulando.")


if __name__ == '__main__':
    aplicar_migrations(app)

    with app.app_context():
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
