# ─────────────────────────────────────────────────────────────────────────────
# Desenvolvedor: Taywan Francisco
# Módulo: Portfólio Público — listagem e detalhe de projetos avaliados
# Projeto Integrador — ADS 2º Módulo · Senac Fecomércio Pernambuco · 2025/2026
# ─────────────────────────────────────────────────────────────────────────────

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from models import Projeto, Usuario, db

portfolio_bp = Blueprint('portfolio', __name__)


@portfolio_bp.route('/portfolio')
def index():
    """Portfólio público — sem necessidade de login."""
    filtro_turma = request.args.get('turma', '')
    filtro_turno = request.args.get('turno', '')
    filtro_aluno = request.args.get('aluno', '').strip()
    busca        = request.args.get('q', '').strip()

    query = Projeto.query.join(Usuario, Projeto.aluno_id == Usuario.id)\
                         .filter(Projeto.status == 'avaliado')

    if filtro_turma:
        query = query.filter(Usuario.turma == filtro_turma)
    if filtro_turno:
        query = query.filter(Usuario.turno == filtro_turno)
    if busca:
        query = query.filter(
            db.or_(
                Projeto.titulo.ilike(f'%{busca}%'),
                Projeto.descricao.ilike(f'%{busca}%'),
                Projeto.tecnologias.ilike(f'%{busca}%')
            )
        )
    if filtro_aluno:
        query = query.filter(
            db.or_(
                Usuario.nome.ilike(f'%{filtro_aluno}%'),
                Projeto.participantes.ilike(f'%{filtro_aluno}%')
            )
        )

    projetos = query.order_by(Projeto.criado_em.desc()).all()

    turmas = sorted(set(
        u.turma for u in Usuario.query.filter(Usuario.perfil == 'aluno',
                                               Usuario.turma != None,
                                               Usuario.turma != '').all()
    ))

    return render_template('portfolio.html',
                           projetos=projetos,
                           turmas=turmas,
                           filtro_turma=filtro_turma,
                           filtro_turno=filtro_turno,
                           filtro_aluno=filtro_aluno,
                           busca=busca)


@portfolio_bp.route('/portfolio/<int:id>')
@login_required
def detalhe_portfolio(id):
    """Detalhe de projeto no portfólio — visível para empresa, admin e professor."""
    if current_user.perfil not in ('empresa', 'admin', 'professor'):
        flash('Acesso restrito.', 'danger')
        return redirect(url_for('portfolio.index'))

    projeto = Projeto.query.filter_by(id=id, status='avaliado').first_or_404()
    return render_template('portfolio_detalhe.html', projeto=projeto)
