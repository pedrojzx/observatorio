# 🎓 Observatório de Projetos Integradores

> Plataforma web centralizada para submissão, avaliação e consulta de Projetos Integradores do curso de Análise e Desenvolvimento de Sistemas — Senac.

---

## 📋 Descrição do Sistema

O **Observatório de Projetos Integradores** é um sistema web desenvolvido como Projeto Integrador do 2º Módulo do curso de ADS no Senac. O sistema centraliza o processo de envio, avaliação e consulta dos projetos, substituindo o método descentralizado por e-mail/Teams.

## 🎯 Objetivo

Criar uma plataforma única onde:
- **Alunos** submetem e gerenciam seus projetos
- **Professores** avaliam os projetos dentro da plataforma
- **Coordenadores/Admin** têm visão estratégica e geram relatórios
- **Empresas parceiras** consultam projetos e identificam talentos

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função |
|---|---|
| Python 3.x | Linguagem principal |
| Flask 3.x | Framework web |
| Flask-SQLAlchemy | ORM para banco de dados |
| Flask-Login | Autenticação e sessões |
| MySQL | Banco de dados relacional |
| PyMySQL | Conector Python ↔ MySQL |
| HTML5 + CSS3 | Interface do usuário |
| Google Fonts (Sora) | Tipografia |
| Git + GitHub | Versionamento de código |
| Trello | Gerenciamento de tarefas |

## 📁 Estrutura do Projeto

```
observatorio/
├── app.py              # Ponto de entrada da aplicação
├── config.py           # Configurações (DB, uploads, chave secreta)
├── models.py           # Modelos do banco de dados (ORM)
├── requirements.txt    # Dependências Python
├── .gitignore
├── routes/
│   ├── auth.py         # Login e logout
│   ├── projetos.py     # CRUD de projetos + avaliação
│   └── admin.py        # Gerenciamento de usuários
├── templates/
│   ├── base.html       # Template base com navbar
│   ├── login.html      # Tela de autenticação
│   ├── painel.html     # Painel principal
│   ├── projeto_form.html    # Formulário criar/editar projeto
│   ├── projeto_detalhe.html # Visualização do projeto
│   ├── avaliar.html    # Formulário de avaliação
│   └── admin/
│       ├── dashboard.html   # Painel admin
│       └── usuario_form.html # Criar/editar usuário
└── uploads/            # Arquivos enviados (gerado automaticamente)
```

## 📐 Regras de Negócio

-  Apenas **Administrador/Coordenador** pode cadastrar usuários
-  **Alunos** só visualizam e gerenciam seus próprios projetos
-  **Professores** visualizam e avaliam todos os projetos
-  Um projeto pode ser avaliado apenas por um professor (mas pode ser atualizado)
-  Status do projeto: `enviado` → `em_avaliacao` → `avaliado`
-  Upload de arquivos: PDF, ZIP, RAR, DOCX, PNG, JPG (máx. 16MB)
-  Link do repositório GitHub obrigatoriamente visível por todos os perfis

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.10+
- MySQL rodando localmente
- Git

### Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/observatorio-pi.git
cd observatorio-pi

# 2. Crie e ative o ambiente virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Crie o banco de dados no MySQL
mysql -u root -p
CREATE DATABASE observatorio_pi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# 5. Configure a conexão no config.py
# Edite a linha:
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:SUA_SENHA@localhost/observatorio_pi'

# 6. Execute o sistema
python app.py 
ou 
python -m flask run
```

### Acesso padrão
- URL: http://localhost:5000
- **Admin**: admin@senac.br / admin123

---

---

# 🎓 Integrative Projects Observatory *(English)*

> Centralized web platform for submission, evaluation and consultation of Integrative Projects from the Systems Analysis and Development program — Senac.

## 📋 System Description

The **Integrative Projects Observatory** is a web system developed as the Integrative Project for Module 2 of the ADS program at Senac. The system centralizes project submission, evaluation and consultation, replacing the decentralized email/Teams-based method.

## 🎯 Objective

Create a single platform where:
- **Students** submit and manage their projects
- **Teachers** evaluate projects within the platform
- **Coordinators/Admins** have a strategic overview and generate reports
- **Partner companies** browse projects and identify talent

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.x | Main language |
| Flask 3.x | Web framework |
| Flask-SQLAlchemy | ORM for database |
| Flask-Login | Authentication and sessions |
| MySQL | Relational database |
| PyMySQL | Python ↔ MySQL connector |
| HTML5 + CSS3 | User interface |
| Google Fonts (Sora) | Typography |
| Git + GitHub | Source control |
| Trello | Task management |

## 🚀 How to Run the Project

```bash
# 1. Clone the repository
git clone https://github.com/your-username/observatorio-pi.git
cd observatorio-pi

# 2. Create and activate virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the MySQL database
mysql -u root -p
CREATE DATABASE observatorio_pi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# 5. Edit config.py with your MySQL credentials

# 6. Run the application
python app.py
```

### Default credentials
- URL: http://localhost:5000
- **Admin**: admin@senac.br / admin123

## 📖 Documentation Link

> 📎 [Link da Documentação / Documentation Link] — *(adicionar após entrega / add after submission)*

---

**Senac Fecomércio · ADS 2º Módulo · 2025**
