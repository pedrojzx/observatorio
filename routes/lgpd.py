from flask import Blueprint, render_template

lgpd_bp = Blueprint('lgpd', __name__)


@lgpd_bp.route('/privacidade')
def privacidade():
    """Página de Política de Privacidade — acessível sem autenticação."""
    return render_template('privacidade.html')
