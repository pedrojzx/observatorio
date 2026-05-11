from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id       = db.Column(db.Integer, primary_key=True)
    nome     = db.Column(db.String(150), nullable=False)
    email    = db.Column(db.String(150), unique=True, nullable=False)
    senha    = db.Column(db.String(256), nullable=False)
    perfil   = db.Column(db.Enum('aluno', 'professor', 'admin'), default='aluno', nullable=False)
    turma    = db.Column(db.String(50))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    projetos    = db.relationship('Projeto', backref='aluno', lazy=True, foreign_keys='Projeto.aluno_id')
    avaliacoes  = db.relationship('Avaliacao', backref='professor', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.email}>'


class Projeto(db.Model):
    __tablename__ = 'projetos'

    id           = db.Column(db.Integer, primary_key=True)
    titulo       = db.Column(db.String(200), nullable=False)
    descricao    = db.Column(db.Text, nullable=False)
    tecnologias  = db.Column(db.String(300))
    link_github  = db.Column(db.String(300))
    arquivo      = db.Column(db.String(300))  # nome do arquivo enviado
    status       = db.Column(db.Enum('enviado', 'em_avaliacao', 'avaliado'), default='enviado')
    criado_em    = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    aluno_id     = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    avaliacao    = db.relationship('Avaliacao', backref='projeto', uselist=False, lazy=True)

    def __repr__(self):
        return f'<Projeto {self.titulo}>'


class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'

    id             = db.Column(db.Integer, primary_key=True)
    nota           = db.Column(db.Float, nullable=False)
    comentario     = db.Column(db.Text)
    criado_em      = db.Column(db.DateTime, default=datetime.utcnow)

    projeto_id     = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)
    professor_id   = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def __repr__(self):
        return f'<Avaliacao projeto={self.projeto_id} nota={self.nota}>'
