from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import Usuario

auth_bp = Blueprint('auth', __name__)


def destino_pos_login(usuario):
    if usuario.perfil == 'admin':
        return url_for('admin.dashboard')
    if usuario.perfil == 'empresa':
        return url_for('portfolio.index')
    return url_for('projetos.painel')


@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(destino_pos_login(current_user))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(destino_pos_login(current_user))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            flash(f'Bem-vindo(a), {usuario.nome}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or destino_pos_login(usuario))
        else:
            flash('E-mail ou senha inválidos.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    from flask import session
    # Limpa flashes pendentes que não foram exibidos (ex: perfil empresa que nunca vê base.html)
    session.pop('_flashes', None)
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))
