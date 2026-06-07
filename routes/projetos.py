from flask import send_from_directory
import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Projeto, Usuario
from datetime import datetime

projetos_bp = Blueprint('projetos', __name__)


def destino_voltar():
    """Redireciona cada perfil para seu destino correto."""
    if current_user.perfil == 'admin':
        return redirect(url_for('admin.dashboard'))
    if current_user.perfil == 'empresa':
        return redirect(url_for('portfolio.index'))
    return redirect(url_for('projetos.painel'))


def allowed_file(filename):
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'pdf', 'zip', 'rar', 'png', 'jpg', 'jpeg', 'docx'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


@projetos_bp.route('/painel')
@login_required
def painel():
    if current_user.perfil == 'empresa':
        return redirect(url_for('portfolio.index'))
    filtro_turma  = request.args.get('turma', '')
    filtro_turno  = request.args.get('turno', '')
    filtro_status = request.args.get('status', '')

    if current_user.perfil == 'aluno':
        projetos = Projeto.query.filter_by(aluno_id=current_user.id)\
                                .order_by(Projeto.criado_em.desc()).all()
        turmas_disponiveis = []
    else:
        query = Projeto.query.join(Usuario, Projeto.aluno_id == Usuario.id)
        if filtro_turma:
            query = query.filter(Usuario.turma == filtro_turma)
        if filtro_turno:
            query = query.filter(Usuario.turno == filtro_turno)
        if filtro_status:
            query = query.filter(Projeto.status == filtro_status)
        projetos = query.order_by(Projeto.criado_em.desc()).all()
        alunos_com_turma = Usuario.query.filter(
            Usuario.perfil == 'aluno', Usuario.turma != None, Usuario.turma != ''
        ).all()
        turmas_disponiveis = sorted(set(a.turma for a in alunos_com_turma))

    return render_template('painel.html',
                           projetos=projetos,
                           turmas_disponiveis=turmas_disponiveis,
                           filtro_turma=filtro_turma,
                           filtro_turno=filtro_turno,
                           filtro_status=filtro_status)


@projetos_bp.route('/projetos/novo', methods=['GET', 'POST'])
@login_required
def novo_projeto():
    if current_user.perfil != 'aluno':
        flash('Apenas alunos podem submeter projetos.', 'warning')
        return destino_voltar()

    if request.method == 'POST':
        titulo        = request.form.get('titulo', '').strip()
        descricao     = request.form.get('descricao', '').strip()
        tecnologias   = request.form.get('tecnologias', '').strip()
        link_github   = request.form.get('link_github', '').strip()
        participantes = request.form.get('participantes', '').strip()

        if not titulo or not descricao:
            flash('Título e descrição são obrigatórios.', 'danger')
            return render_template('projeto_form.html', acao='Novo')

        arquivo_nome = None
        if 'arquivo' in request.files:
            arquivo = request.files['arquivo']
            if arquivo and arquivo.filename and allowed_file(arquivo.filename):
                arquivo_nome = secure_filename(f"{datetime.utcnow().timestamp()}_{arquivo.filename}")
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'])
                os.makedirs(upload_path, exist_ok=True)
                arquivo.save(os.path.join(upload_path, arquivo_nome))

        projeto = Projeto(
            titulo=titulo, descricao=descricao, tecnologias=tecnologias,
            link_github=link_github, arquivo=arquivo_nome, aluno_id=current_user.id,
            participantes=participantes
        )
        db.session.add(projeto)
        db.session.commit()
        flash('Projeto submetido com sucesso!', 'success')
        return destino_voltar()

    return render_template('projeto_form.html', acao='Novo', projeto=None)


@projetos_bp.route('/projetos/<int:id>')
@login_required
def ver_projeto(id):
    projeto = db.get_or_404(Projeto, id)
    if current_user.perfil == 'aluno' and projeto.aluno_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return destino_voltar()
    return render_template('projeto_detalhe.html', projeto=projeto)


@projetos_bp.route('/projetos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_projeto(id):
    projeto = db.get_or_404(Projeto, id)

    if current_user.perfil == 'aluno' and projeto.aluno_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return destino_voltar()

    if current_user.perfil == 'aluno' and projeto.status == 'avaliado':
        flash('Não é possível editar um projeto que já foi avaliado.', 'warning')
        return redirect(url_for('projetos.ver_projeto', id=projeto.id))

    if request.method == 'POST':
        titulo    = request.form.get('titulo', '').strip()
        descricao = request.form.get('descricao', '').strip()
        if not titulo or not descricao:
            flash('Título e descrição são obrigatórios.', 'danger')
            return render_template('projeto_form.html', acao='Editar', projeto=projeto)

        projeto.titulo        = titulo
        projeto.descricao     = descricao
        projeto.tecnologias   = request.form.get('tecnologias', '').strip()
        projeto.link_github   = request.form.get('link_github', '').strip()
        projeto.participantes = request.form.get('participantes', '').strip()
        projeto.atualizado_em = datetime.utcnow()

        if 'arquivo' in request.files:
            arquivo = request.files['arquivo']
            if arquivo and arquivo.filename and allowed_file(arquivo.filename):
                arquivo_nome = secure_filename(f"{datetime.utcnow().timestamp()}_{arquivo.filename}")
                upload_path = current_app.config['UPLOAD_FOLDER']
                os.makedirs(upload_path, exist_ok=True)
                arquivo.save(os.path.join(upload_path, arquivo_nome))
                projeto.arquivo = arquivo_nome

        db.session.commit()
        flash('Projeto atualizado com sucesso!', 'success')
        return redirect(url_for('projetos.ver_projeto', id=projeto.id))

    return render_template('projeto_form.html', acao='Editar', projeto=projeto)


@projetos_bp.route('/projetos/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_projeto(id):
    projeto = db.get_or_404(Projeto, id)

    if current_user.perfil == 'aluno' and projeto.aluno_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return destino_voltar()

    # Apenas alunos são bloqueados de excluir projetos avaliados
    if current_user.perfil == 'aluno' and projeto.status == 'avaliado':
        flash('Este projeto já foi avaliado e não pode ser excluído.', 'danger')
        return destino_voltar()    # Excluir avaliação vinculada antes do projeto
    if projeto.avaliacao:
        db.session.delete(projeto.avaliacao)
        db.session.flush()

    db.session.delete(projeto)
    db.session.commit()
    flash('Projeto excluído com sucesso.', 'info')
    return destino_voltar()


@projetos_bp.route('/projetos/<int:id>/avaliar', methods=['GET', 'POST'])
@login_required
def avaliar_projeto(id):
    if current_user.perfil not in ('professor', 'admin'):
        flash('Acesso negado.', 'danger')
        return destino_voltar()

    projeto = db.get_or_404(Projeto, id)

    if request.method == 'GET' and projeto.status == 'enviado':
        projeto.status = 'em_avaliacao'
        db.session.commit()

    if request.method == 'POST':
        from models import Avaliacao

        # Coleta critérios da rubrica
        def get_nota(campo):
            v = request.form.get(campo, '').strip()
            try:
                n = float(v)
                if 0 <= n <= 10:
                    return n
            except (ValueError, TypeError):
                pass
            return None

        n_func  = get_nota('nota_funcionalidade')
        n_cod   = get_nota('nota_codigo')
        n_doc   = get_nota('nota_documentacao')
        n_int   = get_nota('nota_interface')
        n_apr   = get_nota('nota_apresentacao')

        if any(v is None for v in [n_func, n_cod, n_doc, n_int, n_apr]):
            flash('Preencha todos os critérios da rubrica com valores entre 0 e 10.', 'danger')
            return render_template('avaliar.html', projeto=projeto)

        # Calcula nota final ponderada
        nota = round(n_func*0.30 + n_cod*0.25 + n_doc*0.20 + n_int*0.15 + n_apr*0.10, 1)
        comentario = request.form.get('comentario', '').strip()

        if projeto.avaliacao:
            av = projeto.avaliacao
        else:
            av = Avaliacao(projeto_id=projeto.id, professor_id=current_user.id, nota=0)
            db.session.add(av)

        av.nota                = nota
        av.comentario          = comentario
        av.professor_id        = current_user.id
        av.nota_funcionalidade = n_func
        av.nota_codigo         = n_cod
        av.nota_documentacao   = n_doc
        av.nota_interface      = n_int
        av.nota_apresentacao   = n_apr

        projeto.status = 'avaliado'
        db.session.commit()
        flash(f'Avaliação registrada! Nota final: {nota}', 'success')
        return destino_voltar()

    return render_template('avaliar.html', projeto=projeto)


@projetos_bp.route('/projetos/download/<filename>')
@login_required
def download_arquivo(filename):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename, as_attachment=True)
