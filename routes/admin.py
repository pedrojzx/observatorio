from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, Usuario, Projeto
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.perfil != 'admin':
            flash('Acesso restrito ao administrador.', 'danger')
            return redirect(url_for('projetos.painel'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    total_usuarios = Usuario.query.count()
    total_projetos = Projeto.query.count()
    projetos_avaliados = Projeto.query.filter_by(status='avaliado').count()
    usuarios = Usuario.query.order_by(Usuario.criado_em.desc()).all()
    return render_template('admin/dashboard.html',
                           total_usuarios=total_usuarios,
                           total_projetos=total_projetos,
                           projetos_avaliados=projetos_avaliados,
                           usuarios=usuarios)


@admin_bp.route('/usuarios/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_usuario():
    if request.method == 'POST':
        nome   = request.form.get('nome', '').strip()
        email  = request.form.get('email', '').strip()
        senha  = request.form.get('senha', '')
        perfil = request.form.get('perfil', 'aluno')
        turma  = request.form.get('turma', '').strip()

        if not nome or not email or not senha:
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'danger')
            return render_template('admin/usuario_form.html', acao='Novo', usuario=None)

        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'danger')
            return render_template('admin/usuario_form.html', acao='Novo', usuario=None)

        usuario = Usuario(
            nome=nome,
            email=email,
            senha=generate_password_hash(senha),
            perfil=perfil,
            turma=turma
        )
        db.session.add(usuario)
        db.session.commit()
        flash(f'Usuário {nome} cadastrado com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/usuario_form.html', acao='Novo', usuario=None)


@admin_bp.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_usuario(id):
    usuario = db.get_or_404(Usuario, id)

    if request.method == 'POST':
        usuario.nome   = request.form.get('nome', '').strip()
        usuario.email  = request.form.get('email', '').strip()
        usuario.perfil = request.form.get('perfil', 'aluno')
        usuario.turma  = request.form.get('turma', '').strip()

        nova_senha = request.form.get('senha', '').strip()
        if nova_senha:
            usuario.senha = generate_password_hash(nova_senha)

        db.session.commit()
        flash('Usuário atualizado!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/usuario_form.html', acao='Editar', usuario=usuario)


@admin_bp.route('/usuarios/<int:id>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir_usuario(id):
    usuario = db.get_or_404(Usuario, id)
    if usuario.id == current_user.id:
        flash('Você não pode excluir sua própria conta.', 'danger')
        return redirect(url_for('admin.dashboard'))
    if usuario.projetos:
        flash(f'Não é possível excluir "{usuario.nome}": possui {len(usuario.projetos)} projeto(s) vinculado(s). Exclua os projetos antes.', 'danger')
        return redirect(url_for('admin.dashboard'))
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário removido.', 'info')
    return redirect(url_for('admin.dashboard'))
