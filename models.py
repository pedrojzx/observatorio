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
    perfil   = db.Column(db.Enum('aluno', 'professor', 'admin', 'empresa'), default='aluno', nullable=False)
    turma    = db.Column(db.String(50))
    turno    = db.Column(db.Enum('manha', 'tarde', 'noite'), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    projetos    = db.relationship('Projeto', backref='aluno', lazy=True, foreign_keys='Projeto.aluno_id')
    avaliacoes  = db.relationship('Avaliacao', backref='professor', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.email}>'

    @property
    def turno_display(self):
        mapa = {'manha': 'Manhã', 'tarde': 'Tarde', 'noite': 'Noite'}
        return mapa.get(self.turno, '—')


class Projeto(db.Model):
    __tablename__ = 'projetos'

    id           = db.Column(db.Integer, primary_key=True)
    titulo       = db.Column(db.String(200), nullable=False)
    descricao    = db.Column(db.Text, nullable=False)
    tecnologias  = db.Column(db.String(300))
    link_github  = db.Column(db.String(300))
    arquivo      = db.Column(db.String(300))
    participantes = db.Column(db.Text)
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

    # Rubrica — critérios com pesos
    nota_funcionalidade = db.Column(db.Float, nullable=True)  # 30%
    nota_codigo         = db.Column(db.Float, nullable=True)  # 25%
    nota_documentacao   = db.Column(db.Float, nullable=True)  # 20%
    nota_interface      = db.Column(db.Float, nullable=True)  # 15%
    nota_apresentacao   = db.Column(db.Float, nullable=True)  # 10%

    projeto_id     = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)
    professor_id   = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def nota_calculada(self):
        campos = [
            (self.nota_funcionalidade, 0.30),
            (self.nota_codigo,         0.25),
            (self.nota_documentacao,   0.20),
            (self.nota_interface,      0.15),
            (self.nota_apresentacao,   0.10),
        ]
        if all(v is not None for v, _ in campos):
            return round(sum(v * p for v, p in campos), 1)
        return None

    def __repr__(self):
        return f'<Avaliacao projeto={self.projeto_id} nota={self.nota}>'
