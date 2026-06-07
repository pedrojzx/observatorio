# Observatório de Projetos Integradores

Plataforma web centralizada para submissão, avaliação e consulta pública de Projetos Integradores do curso de Análise e Desenvolvimento de Sistemas — Senac Fecomércio Pernambuco.

---

## Descrição

O Observatório substitui o processo descentralizado de e-mail e Teams por uma plataforma única que cobre todo o ciclo de vida dos Projetos Integradores: submissão pelos alunos, avaliação estruturada pelos professores e exposição pública dos trabalhos concluídos para visitantes e empresas parceiras.

---

## Time de Desenvolvimento

Filipe José, Guilherme Gonçalves, Ivan Roberto, Pedro Roberto, Taywan Francisco e Timóteo Batista

Senac Fecomércio Pernambuco — ADS 2º Módulo — 2025/2026

---

## Tecnologias

| Tecnologia | Versão | Função |
|---|---|---|
| Python | 3.10+ | Linguagem principal do backend |
| Flask | 3.0.3 | Framework web — rotas, templates e blueprints |
| Flask-SQLAlchemy | 3.1.1 | ORM para abstração do banco de dados |
| Flask-Login | 0.6.3 | Gerenciamento de sessões e autenticação |
| Werkzeug | 3.0.3 | Hash seguro de senhas (PBKDF2) e utilitários HTTP |
| PyMySQL | 1.1.1 | Driver de conexão com MySQL |
| cryptography | 42.0.8 | Suporte criptográfico para operações seguras |
| SQLite / MySQL | — | SQLite em desenvolvimento, MySQL em produção |
| HTML5 + CSS3 + JS | — | Frontend sem frameworks externos |
| Google Fonts (Sora) | — | Tipografia da interface |

---

## Estrutura do Projeto

```
observatorio/
├── app.py                          # Ponto de entrada e sistema de migrações
├── config.py                       # Configurações (banco, uploads, chave secreta)
├── models.py                       # Modelos ORM: Usuario, Projeto, Avaliacao
├── requirements.txt                # Dependências Python
├── .gitignore
├── docs/
│   ├── requisitos.md               # Requisitos funcionais e não funcionais
│   └── pesquisa_tecnologia_sociedade.md
├── routes/
│   ├── auth.py                     # Login e logout
│   ├── projetos.py                 # CRUD de projetos e avaliação
│   ├── admin.py                    # Dashboard e gestão de usuários
│   ├── portfolio.py                # Portfólio público
│   └── lgpd.py                     # Política de privacidade
├── templates/
│   ├── base.html                   # Template base com navbar e rodapé
│   ├── login.html
│   ├── painel.html
│   ├── projeto_form.html
│   ├── projeto_detalhe.html
│   ├── avaliar.html
│   ├── portfolio.html              # Listagem pública de projetos avaliados
│   ├── portfolio_detalhe.html      # Detalhe público de um projeto
│   ├── privacidade.html            # Política de privacidade (LGPD)
│   └── admin/
│       ├── dashboard.html
│       ├── usuario_form.html
│       └── aluno_form.html
└── uploads/                        # Arquivos enviados (gerado automaticamente)
```

---

## Perfis de Acesso

| Perfil | Acesso |
|---|---|
| Aluno | Submete e gerencia seus próprios projetos; visualiza nota e feedback após avaliação |
| Professor | Visualiza e avalia todos os projetos com a rubrica ponderada; cadastra alunos |
| Administrador | Acesso irrestrito: dashboard, métricas, gestão de usuários, exportação CSV |
| Empresa | Acesso ao portfólio público e detalhe de projetos avaliados, sem acesso ao painel interno |
| Visitante | Acesso à listagem do portfólio público em `/portfolio` sem necessidade de login |

---

## Sistema de Avaliação

A avaliação usa uma rubrica ponderada com cinco critérios obrigatórios:

| Critério | Peso |
|---|---|
| Funcionalidade | 30% |
| Qualidade do Código | 25% |
| Documentação | 20% |
| Interface / UX | 15% |
| Apresentação | 10% |

Fórmula: `nota_final = (func × 0.30) + (codigo × 0.25) + (doc × 0.20) + (ui × 0.15) + (apres × 0.10)`

---

## Segurança e LGPD

- Senhas armazenadas com hash PBKDF2/HMAC-SHA256 via Werkzeug — nunca em texto plano
- Controle de acesso baseado em perfis (RBAC) validado no servidor em todas as rotas
- Sessões autenticadas com cookie assinado pela `SECRET_KEY`
- Sanitização de uploads com `secure_filename()` e validação de extensões permitidas
- Credenciais e chave secreta via variáveis de ambiente — nunca no código
- Política de privacidade acessível em `/privacidade` sem necessidade de login
- Coleta mínima de dados em conformidade com a LGPD (Lei nº 13.709/2018)

---

## Documentação

| Documento | Descrição |
|---|---|
| [docs/requisitos.md](docs/requisitos.md) | Requisitos funcionais, não funcionais, casos de uso e modelo de dados |
| [docs/pesquisa_tecnologia_sociedade.md](docs/pesquisa_tecnologia_sociedade.md) | Definição do problema, metodologia e resultados esperados |
| Política de Privacidade | Acessível na plataforma em `/privacidade` |

---

## Como Executar

### Pré-requisitos

- Python 3.10 ou superior
- MySQL 8+ rodando localmente (ou usar SQLite para desenvolvimento rápido)
- Git

### Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/pedrojzx/observatorio.git
cd observatorio

# 2. Crie e ative o ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Crie o banco de dados no MySQL
mysql -u root -p
CREATE DATABASE observatorio_pi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# 5. Configure as variáveis de ambiente criando um arquivo .env
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=mysql+pymysql://root:SUA_SENHA@localhost/observatorio_pi

# Para rodar com SQLite (sem MySQL), use:
DATABASE_URL=sqlite:///observatorio.db

# 6. Execute o servidor
python app.py
```

Acesse em: http://localhost:5000

### Credenciais padrão do administrador

| Campo | Valor |
|---|---|
| E-mail | admin@senac.br |
| Senha | admin123 |

> Altere as credenciais padrão imediatamente após o primeiro acesso em produção.

---

## Status do Projeto

`enviado` → `em_avaliacao` → `avaliado`

O status é atualizado automaticamente: muda para `em_avaliacao` quando um professor abre o formulário de avaliação, e para `avaliado` após salvar a avaliação.

---

*Senac Fecomércio Pernambuco · ADS 2º Módulo · 2025/2026*
