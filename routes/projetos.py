from flask import send_from_directory
import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Projeto, Usuario
from datetime import datetime

projetos_bp = Blueprint('projetos', __name__)

def allowed_file(filename):
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'pdf', 'zip', 'rar', 'png', 'jpg', 'jpeg', 'docx'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


#  PAINEL PRINCIPAL 

@projetos_bp.route('/painel')
@login_required
def painel():
    if current_user.perfil == 'aluno':
        projetos = Projeto.query.filter_by(aluno_id=current_user.id)\
                                .order_by(Projeto.criado_em.desc()).all()
    elif current_user.perfil == 'professor':
        projetos = Projeto.query.order_by(Projeto.criado_em.desc()).all()
    else:  # admin
        projetos = Projeto.query.order_by(Projeto.criado_em.desc()).all()

    return render_template('painel.html', projetos=projetos)


#  CREATE 

@projetos_bp.route('/projetos/novo', methods=['GET', 'POST'])
@login_required
def novo_projeto():
    if current_user.perfil != 'aluno':
        flash('Apenas alunos podem submeter projetos.', 'warning')
        return redirect(url_for('projetos.painel'))

    if request.method == 'POST':
        titulo      = request.form.get('titulo', '').strip()
        descricao   = request.form.get('descricao', '').strip()
        tecnologias = request.form.get('tecnologias', '').strip()
        link_github = request.form.get('link_github', '').strip()

        if not titulo or not descricao:
            flash('Título e descrição são obrigatórios.', 'danger')
            return render_template('projeto_form.html', acao='Novo')

        # Upload de arquivo
        arquivo_nome = None
        if 'arquivo' in request.files:
            arquivo = request.files['arquivo']
            if arquivo and arquivo.filename and allowed_file(arquivo.filename):
                arquivo_nome = secure_filename(f"{datetime.utcnow().timestamp()}_{arquivo.filename}")
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'])
                os.makedirs(upload_path, exist_ok=True)
                arquivo.save(os.path.join(upload_path, arquivo_nome))

        projeto = Projeto(
            titulo=titulo,
            descricao=descricao,
            tecnologias=tecnologias,
            link_github=link_github,
            arquivo=arquivo_nome,
            aluno_id=current_user.id
        )
        db.session.add(projeto)
        db.session.commit()
        flash('Projeto submetido com sucesso!', 'success')
        return redirect(url_for('projetos.painel'))

    return render_template('projeto_form.html', acao='Novo', projeto=None)


#  READ 

@projetos_bp.route('/projetos/<int:id>')
@login_required
def ver_projeto(id):
    projeto = db.get_or_404(Projeto, id)
    # Aluno só vê os próprios
    if current_user.perfil == 'aluno' and projeto.aluno_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('projetos.painel'))
    return render_template('projeto_detalhe.html', projeto=projeto)


# UPDATE 

@projetos_bp.route('/projetos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_projeto(id):
    projeto = db.get_or_404(Projeto, id)

    if current_user.perfil == 'aluno' and projeto.aluno_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('projetos.painel'))

    # Aluno não pode editar projeto já avaliado
    if current_user.perfil == 'aluno' and projeto.status == 'avaliado':
        flash('Não é possível editar um projeto que já foi avaliado.', 'warning')
        return redirect(url_for('projetos.ver_projeto', id=projeto.id))

    if request.method == 'POST':
        titulo    = request.form.get('titulo', '').strip()
        descricao = request.form.get('descricao', '').strip()

        if not titulo or not descricao:
            flash('Título e descrição são obrigatórios.', 'danger')
            return render_template('projeto_form.html', acao='Editar', projeto=projeto)

        projeto.titulo      = titulo
        projeto.descricao   = descricao
        projeto.tecnologias = request.form.get('tecnologias', '').strip()
        projeto.link_github = request.form.get('link_github', '').strip()
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


# DELETE 
@projetos_bp.route('/projetos/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_projeto(id):
    projeto = db.get_or_404(Projeto, id)

    if current_user.perfil == 'aluno' and projeto.aluno_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('projetos.painel'))

    db.session.delete(projeto)
    db.session.commit()
    flash('Projeto excluído com sucesso.', 'info')
    return redirect(url_for('projetos.painel'))



#  AVALIAÇÃO (professor)

@projetos_bp.route('/projetos/<int:id>/avaliar', methods=['GET', 'POST'])
@login_required
def avaliar_projeto(id):
    if current_user.perfil not in ('professor', 'admin'):
        flash('Acesso negado.', 'danger')
        return redirect(url_for('projetos.painel'))

    projeto = db.get_or_404(Projeto, id)

    # Marca projeto como "em avaliação" quando professor abre pela primeira vez
    if request.method == 'GET' and projeto.status == 'enviado':
        projeto.status = 'em_avaliacao'
        db.session.commit()

    if request.method == 'POST':
        from models import Avaliacao
        try:
            nota = float(request.form.get('nota', ''))
            if nota < 0 or nota > 10:
                raise ValueError
        except ValueError:
            flash('Nota inválida. Informe um valor entre 0 e 10.', 'danger')
            return render_template('avaliar.html', projeto=projeto)

        comentario = request.form.get('comentario', '').strip()

        if projeto.avaliacao:
            projeto.avaliacao.nota       = nota
            projeto.avaliacao.comentario = comentario
            projeto.avaliacao.professor_id = current_user.id
        else:
            av = Avaliacao(nota=nota, comentario=comentario,
                           projeto_id=projeto.id, professor_id=current_user.id)
            db.session.add(av)

        projeto.status = 'avaliado'
        db.session.commit()
        flash('Avaliação registrada!', 'success')
        return redirect(url_for('projetos.painel'))

    return render_template('avaliar.html', projeto=projeto)

# DOWNLOAD 

@projetos_bp.route('/projetos/download/<filename>')
@login_required
def download_arquivo(filename):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename, as_attachment=True)
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory