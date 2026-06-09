# ─────────────────────────────────────────────────────────────────────────────
# Desenvolvedor: Timóteo Batista
# Módulo: Painel Administrativo — dashboard, CRUD de usuários e exportação CSV
# Projeto Integrador — ADS 2º Módulo · Senac Fecomércio Pernambuco · 2025/2026
# ─────────────────────────────────────────────────────────────────────────────

import csv
import io
from flask import Blueprint, render_template, redirect, url_for, flash, request, Response, make_response
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, Usuario, Projeto, Avaliacao
from functools import wraps
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.perfil != 'admin':
            flash('Acesso restrito ao administrador.', 'danger')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated


def admin_ou_professor_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.perfil not in ('admin', 'professor'):
            flash('Acesso restrito.', 'danger')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated


# ── DASHBOARD ─────────────────────────────────────────────────────────────────

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    from flask import request as req

    # Filtros de projetos
    filtro_turma  = req.args.get('turma', '')
    filtro_turno  = req.args.get('turno', '')
    filtro_status = req.args.get('status', '')
    filtro_busca  = req.args.get('q', '').strip()

    total_usuarios      = Usuario.query.count()
    total_projetos      = Projeto.query.count()
    projetos_avaliados  = Projeto.query.filter_by(status='avaliado').count()
    projetos_em_aval    = Projeto.query.filter_by(status='em_avaliacao').count()
    projetos_enviados   = Projeto.query.filter_by(status='enviado').count()
    usuarios            = Usuario.query.order_by(Usuario.criado_em.desc()).all()
    turmas              = sorted(set(u.turma for u in usuarios if u.turma))

    # Projetos com filtros
    query_proj = Projeto.query.join(Usuario, Projeto.aluno_id == Usuario.id)
    if filtro_turma:
        query_proj = query_proj.filter(Usuario.turma == filtro_turma)
    if filtro_turno:
        query_proj = query_proj.filter(Usuario.turno == filtro_turno)
    if filtro_status:
        query_proj = query_proj.filter(Projeto.status == filtro_status)
    if filtro_busca:
        query_proj = query_proj.filter(
            db.or_(
                Projeto.titulo.ilike(f'%{filtro_busca}%'),
                Projeto.descricao.ilike(f'%{filtro_busca}%'),
                Projeto.tecnologias.ilike(f'%{filtro_busca}%'),
                Usuario.nome.ilike(f'%{filtro_busca}%'),
            )
        )
    projetos = query_proj.order_by(Projeto.criado_em.desc()).all()

    # Métricas por turma
    stats_turma = []
    for turma in turmas:
        alunos_turma = Usuario.query.filter_by(perfil='aluno', turma=turma).all()
        ids_alunos   = [a.id for a in alunos_turma]
        total_t      = Projeto.query.filter(Projeto.aluno_id.in_(ids_alunos)).count()
        aval_t       = Projeto.query.filter(Projeto.aluno_id.in_(ids_alunos), Projeto.status=='avaliado').count()
        projetos_t   = Projeto.query.filter(Projeto.aluno_id.in_(ids_alunos), Projeto.status=='avaliado').all()
        notas        = [p.avaliacao.nota for p in projetos_t if p.avaliacao]
        media_t      = round(sum(notas)/len(notas), 1) if notas else None
        stats_turma.append({
            'turma': turma,
            'alunos': len(alunos_turma),
            'projetos': total_t,
            'avaliados': aval_t,
            'media': media_t,
            'pct': round(aval_t/total_t*100) if total_t else 0
        })

    # Métricas por turno
    stats_turno = []
    for turno in ['manha', 'tarde', 'noite']:
        alunos_t  = Usuario.query.filter_by(perfil='aluno', turno=turno).all()
        ids       = [a.id for a in alunos_t]
        total_t   = Projeto.query.filter(Projeto.aluno_id.in_(ids)).count() if ids else 0
        aval_t    = Projeto.query.filter(Projeto.aluno_id.in_(ids), Projeto.status=='avaliado').count() if ids else 0
        stats_turno.append({'turno': turno, 'total': total_t, 'avaliados': aval_t})

    # Últimas avaliações
    ultimas_avaliacoes = Avaliacao.query.order_by(Avaliacao.criado_em.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                           total_usuarios=total_usuarios,
                           total_projetos=total_projetos,
                           projetos_avaliados=projetos_avaliados,
                           projetos_em_aval=projetos_em_aval,
                           projetos_enviados=projetos_enviados,
                           usuarios=usuarios,
                           turmas=turmas,
                           stats_turma=stats_turma,
                           stats_turno=stats_turno,
                           ultimas_avaliacoes=ultimas_avaliacoes,
                           projetos=projetos,
                           filtro_turma=filtro_turma,
                           filtro_turno=filtro_turno,
                           filtro_status=filtro_status,
                           filtro_busca=filtro_busca)


# ── RELATÓRIO CSV ──────────────────────────────────────────────────────────────

@admin_bp.route('/relatorio/csv')
@login_required
@admin_required
def relatorio_csv():
    projetos = Projeto.query.join(Usuario, Projeto.aluno_id == Usuario.id)\
                            .order_by(Usuario.turma, Projeto.criado_em).all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'ID', 'Título do Projeto', 'Aluno', 'E-mail', 'Turma', 'Turno', 'Status',
        'Nota Final', 'Funcionalidade (30%)', 'Código (25%)', 'Documentação (20%)',
        'Interface (15%)', 'Apresentação (10%)', 'Avaliado por', 'Data Avaliação',
        'GitHub', 'Enviado em'
    ])

    for p in projetos:
        av = p.avaliacao
        writer.writerow([
            p.id,
            p.titulo,
            p.aluno.nome,
            p.aluno.email,
            p.aluno.turma or '—',
            p.aluno.turno_display if p.aluno.turno else '—',
            p.status.replace('_', ' '),
            f'{av.nota:.1f}'.replace('.', ',') if av else '—',
            f'{av.nota_funcionalidade:.1f}'.replace('.', ',') if av and av.nota_funcionalidade is not None else '—',
            f'{av.nota_codigo:.1f}'.replace('.', ',')        if av and av.nota_codigo is not None else '—',
            f'{av.nota_documentacao:.1f}'.replace('.', ',')  if av and av.nota_documentacao is not None else '—',
            f'{av.nota_interface:.1f}'.replace('.', ',')     if av and av.nota_interface is not None else '—',
            f'{av.nota_apresentacao:.1f}'.replace('.', ',')  if av and av.nota_apresentacao is not None else '—',
            av.professor.nome if av else '—',
            av.criado_em.strftime('%d/%m/%Y') if av else '—',
            p.link_github or '—',
            p.criado_em.strftime('%d/%m/%Y')
        ])

    response = make_response(output.getvalue().encode('utf-8-sig'))
    response.headers['Content-Type']        = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename=relatorio_pi_{datetime.now().strftime("%Y%m%d")}.csv'
    return response


# ── RELATÓRIO PDF (gerado via HTML → PDF sem dependências externas) ───────────

@admin_bp.route('/relatorio/pdf')
@login_required
@admin_required
def relatorio_pdf():
    projetos = Projeto.query.join(Usuario, Projeto.aluno_id == Usuario.id)\
                            .order_by(Usuario.turma, Projeto.criado_em).all()

    total   = len(projetos)
    aval    = sum(1 for p in projetos if p.status == 'avaliado')
    em_aval = sum(1 for p in projetos if p.status == 'em_avaliacao')
    env     = sum(1 for p in projetos if p.status == 'enviado')
    notas   = [p.avaliacao.nota for p in projetos if p.avaliacao]
    media_g = f"{sum(notas)/len(notas):.1f}" if notas else "—"

    def fmt(v):
        return f"{v:.1f}" if v is not None else "—"

    def status_color(s):
        return {"avaliado": "#16a34a", "em_avaliacao": "#d97706", "enviado": "#0369a1"}.get(s, "#6b7280")

    def nota_color(n):
        if n is None: return "#6b7280"
        return "#16a34a" if n >= 7 else ("#d97706" if n >= 5 else "#dc2626")

    rows_html = ""
    for i, p in enumerate(projetos):
        av = p.avaliacao
        bg = "#ffffff" if i % 2 == 0 else "#f3f4f6"
        sc = status_color(p.status)
        status_label = {"enviado": "Enviado", "em_avaliacao": "Em Aval.", "avaliado": "Avaliado"}.get(p.status, p.status)
        nota_val = f"{av.nota:.1f}" if av else "—"
        nc = nota_color(av.nota if av else None)
        avaliador = av.professor.nome[:20] if av else "—"
        rows_html += f"""
        <tr style="background:{bg};">
            <td>{p.id}</td>
            <td style="text-align:left;">{p.titulo[:45]}</td>
            <td style="text-align:left;">{p.aluno.nome[:25]}</td>
            <td>{p.aluno.turma or "—"}</td>
            <td>{p.aluno.turno_display if p.aluno.turno else "—"}</td>
            <td><span style="color:{sc};font-weight:700;">{status_label}</span></td>
            <td>{fmt(av.nota_funcionalidade) if av else "—"}</td>
            <td>{fmt(av.nota_codigo) if av else "—"}</td>
            <td>{fmt(av.nota_documentacao) if av else "—"}</td>
            <td>{fmt(av.nota_interface) if av else "—"}</td>
            <td>{fmt(av.nota_apresentacao) if av else "—"}</td>
            <td style="color:{nc};font-weight:700;">{nota_val}</td>
            <td style="text-align:left;">{avaliador}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: Arial, sans-serif; font-size: 10px; color: #111827; padding: 20px; }}
  h1 {{ font-size: 16px; color: #1a2f6e; text-align:center; margin-bottom:4px; }}
  .sub {{ font-size:9px; color:#6b7280; text-align:center; margin-bottom:12px; }}
  hr {{ border:none; border-top:2px solid #f07621; margin-bottom:14px; }}
  .summary {{ display:flex; gap:10px; margin-bottom:16px; }}
  .scard {{ flex:1; border:1px solid #e5e7eb; border-radius:6px; padding:8px 10px; text-align:center; }}
  .scard .num {{ font-size:18px; font-weight:800; color:#1a2f6e; }}
  .scard .lbl {{ font-size:8px; color:#6b7280; text-transform:uppercase; letter-spacing:.04em; margin-top:2px; }}
  table {{ width:100%; border-collapse:collapse; }}
  thead tr {{ background:#1a2f6e; color:#fff; }}
  th {{ padding:5px 4px; font-size:8px; text-align:center; text-transform:uppercase; letter-spacing:.03em; }}
  td {{ padding:4px; font-size:8px; text-align:center; border-bottom:1px solid #e5e7eb; }}
  .section-title {{ font-size:11px; font-weight:700; color:#1a2f6e; margin:12px 0 6px; }}
  footer {{ margin-top:16px; font-size:7px; color:#9ca3af; text-align:center; border-top:1px solid #e5e7eb; padding-top:6px; }}
  @media print {{
    body {{ padding: 10px; }}
    @page {{ size: A4 landscape; margin: 1cm; }}
  }}
</style>
</head>
<body>
<h1>Observatório de Projetos Integradores</h1>
<p class="sub">Senac Fecomércio — ADS 2º Módulo &nbsp;·&nbsp; Relatório gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}</p>
<hr>
<div class="summary">
  <div class="scard"><div class="num">{total}</div><div class="lbl">Total</div></div>
  <div class="scard"><div class="num" style="color:#16a34a;">{aval}</div><div class="lbl">Avaliados</div></div>
  <div class="scard"><div class="num" style="color:#d97706;">{em_aval}</div><div class="lbl">Em Avaliação</div></div>
  <div class="scard"><div class="num" style="color:#0369a1;">{env}</div><div class="lbl">Aguardando</div></div>
  <div class="scard"><div class="num" style="color:#2a4494;">{media_g}</div><div class="lbl">Média Geral</div></div>
</div>
<p class="section-title">📋 Lista Completa de Projetos</p>
<table>
  <thead>
    <tr>
      <th>#</th><th>Título</th><th>Aluno</th><th>Turma</th><th>Turno</th><th>Status</th>
      <th>Func.</th><th>Cód.</th><th>Doc.</th><th>Interf.</th><th>Apres.</th>
      <th>Nota</th><th>Avaliador</th>
    </tr>
  </thead>
  <tbody>
    {rows_html}
  </tbody>
</table>
<footer>Documento gerado automaticamente pelo Observatório de Projetos Integradores — Senac Fecomércio · ADS 2º Módulo</footer>
<script>window.onload = function(){{ window.print(); }}</script>
</body>
</html>"""

    return Response(html, mimetype='text/html')

# ── CRUD USUÁRIOS ──────────────────────────────────────────────────────────────

@admin_bp.route('/alunos/novo', methods=['GET', 'POST'])
@login_required
@admin_ou_professor_required
def novo_aluno():
    if request.method == 'POST':
        nome  = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        turma = request.form.get('turma', '').strip()
        turno = request.form.get('turno', '') or None

        if not nome or not email or not senha:
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'danger')
            return render_template('admin/aluno_form.html', acao='Novo', usuario=None)

        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'danger')
            return render_template('admin/aluno_form.html', acao='Novo', usuario=None)

        usuario = Usuario(nome=nome, email=email, senha=generate_password_hash(senha),
                          perfil='aluno', turma=turma, turno=turno)
        db.session.add(usuario)
        db.session.commit()
        flash(f'Aluno {nome} cadastrado com sucesso!', 'success')
        return redirect(url_for('admin.dashboard') if current_user.perfil == 'admin' else url_for('projetos.painel'))

    return render_template('admin/aluno_form.html', acao='Novo', usuario=None)


@admin_bp.route('/alunos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_ou_professor_required
def editar_aluno(id):
    usuario = db.get_or_404(Usuario, id)
    if current_user.perfil == 'professor' and usuario.perfil != 'aluno':
        flash('Professores só podem editar contas de alunos.', 'danger')
        return redirect(url_for('projetos.painel'))

    if request.method == 'POST':
        usuario.nome  = request.form.get('nome', '').strip()
        usuario.email = request.form.get('email', '').strip()
        usuario.turma = request.form.get('turma', '').strip()
        turno         = request.form.get('turno', '')
        usuario.turno = turno or None
        nova_senha    = request.form.get('senha', '').strip()
        if nova_senha:
            usuario.senha = generate_password_hash(nova_senha)
        db.session.commit()
        flash('Aluno atualizado!', 'success')
        return redirect(url_for('admin.dashboard') if current_user.perfil == 'admin' else url_for('projetos.painel'))

    return render_template('admin/aluno_form.html', acao='Editar', usuario=usuario)


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
        turno  = request.form.get('turno', '') or None

        if not nome or not email or not senha:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('admin/usuario_form.html', acao='Novo', usuario=None)

        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'danger')
            return render_template('admin/usuario_form.html', acao='Novo', usuario=None)

        usuario = Usuario(nome=nome, email=email, senha=generate_password_hash(senha),
                          perfil=perfil, turma=turma, turno=turno)
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
        turno          = request.form.get('turno', '')
        usuario.turno  = turno or None
        nova_senha     = request.form.get('senha', '').strip()
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
        flash(f'Não é possível excluir "{usuario.nome}": possui {len(usuario.projetos)} projeto(s) vinculado(s).', 'danger')
        return redirect(url_for('admin.dashboard'))
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário removido.', 'info')
    return redirect(url_for('admin.dashboard'))
