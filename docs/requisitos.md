# 📐 Documento de Requisitos de Software
**Sistema:** Observatório de Projetos Integradores  
**Curso:** Análise e Desenvolvimento de Sistemas — Senac Fecomércio  
**Módulo:** 2º Módulo  
**Versão:** 1.0  
**Data:** 2025  

---

## 1. Introdução

### 1.1 Propósito
Este documento descreve os requisitos funcionais e não funcionais do sistema **Observatório de Projetos Integradores**, desenvolvido como Projeto Integrador do 2º Módulo do curso de ADS. Seu objetivo é orientar o desenvolvimento, servir como base para testes e documentar as decisões de projeto.

### 1.2 Escopo
O sistema é uma plataforma web centralizada que substituirá o processo manual (e-mail/Teams) de submissão e avaliação dos Projetos Integradores do Senac. O sistema gerencia três perfis de usuário: aluno, professor e administrador.

### 1.3 Definições e Siglas

| Termo | Definição |
|---|---|
| PI | Projeto Integrador |
| ADS | Análise e Desenvolvimento de Sistemas |
| CRUD | Create, Read, Update, Delete |
| ORM | Object-Relational Mapping |
| LGPD | Lei Geral de Proteção de Dados (Lei nº 13.709/2018) |
| Admin | Perfil de administrador/coordenador do sistema |

---

## 2. Partes Interessadas (Stakeholders)

| Parte Interessada | Papel | Interesse |
|---|---|---|
| Alunos | Usuário final | Submeter e acompanhar projetos |
| Professores | Avaliador | Avaliar projetos e cadastrar alunos |
| Coordenadores / Admin | Gestor | Visão estratégica, relatórios, gestão de usuários |
| Empresas parceiras | Consultor externo | Consultar projetos e identificar talentos |
| Senac | Instituição | Centralizar e modernizar o processo de PI |

---

## 3. Requisitos Funcionais

> **Convenção de ID:** RF-XXX  
> **Prioridade:** Alta / Média / Baixa

### 3.1 Módulo de Autenticação
**Responsável:** Pedro Roberto

| ID | Descrição | Prioridade |
|---|---|---|
| RF-001 | O sistema deve permitir login com e-mail e senha | Alta |
| RF-002 | O sistema deve manter sessão autenticada por cookie seguro | Alta |
| RF-003 | O sistema deve redirecionar usuário não autenticado para a tela de login | Alta |
| RF-004 | O sistema deve permitir logout com encerramento de sessão | Alta |
| RF-005 | O sistema deve exibir mensagem de erro para credenciais inválidas | Média |

### 3.2 Módulo de Usuários
**Responsável:** Timóteo Batista

| ID | Descrição | Prioridade |
|---|---|---|
| RF-006 | O administrador deve poder criar usuários com qualquer perfil (aluno, professor, admin) | Alta |
| RF-007 | O professor deve poder criar e editar somente usuários com perfil aluno | Alta |
| RF-008 | Cada usuário deve ter: nome, e-mail único, senha (hash), perfil, turma e turno | Alta |
| RF-009 | O administrador deve poder editar e excluir usuários | Alta |
| RF-010 | Não deve ser possível excluir usuário que possui projetos vinculados | Média |
| RF-011 | Não deve ser possível excluir a própria conta do administrador logado | Alta |
| RF-012 | O e-mail deve ser único no sistema | Alta |

### 3.3 Módulo de Projetos
**Responsável:** Guilherme Gonçalves

| ID | Descrição | Prioridade |
|---|---|---|
| RF-013 | O aluno deve poder submeter projetos com: título, descrição, tecnologias, link do GitHub e arquivo | Alta |
| RF-014 | O aluno deve poder editar seus projetos enquanto não estiverem com status "avaliado" | Alta |
| RF-015 | O aluno deve poder excluir seus próprios projetos | Alta |
| RF-016 | O aluno deve visualizar somente seus próprios projetos | Alta |
| RF-017 | O professor e o admin devem visualizar todos os projetos com filtros | Alta |
| RF-018 | O sistema deve suportar upload de arquivos nos formatos: PDF, ZIP, RAR, DOCX, PNG, JPG | Média |
| RF-019 | O tamanho máximo de arquivo permitido é 100 MB | Média |
| RF-020 | O link do repositório GitHub deve ser visível para todos os perfis | Alta |
| RF-021 | O sistema deve permitir download dos arquivos enviados | Média |

### 3.4 Módulo de Avaliação
**Responsável:** Guilherme Gonçalves

| ID | Descrição | Prioridade |
|---|---|---|
| RF-022 | O professor e o admin devem poder avaliar projetos com nota (0 a 10) e comentário | Alta |
| RF-023 | Ao abrir um projeto para avaliação, o status deve mudar automaticamente para "em_avaliacao" | Alta |
| RF-024 | Após avaliação, o status deve mudar para "avaliado" | Alta |
| RF-025 | A avaliação de um projeto pode ser atualizada pelo avaliador | Média |
| RF-026 | O aluno não deve poder avaliar projetos | Alta |

### 3.5 Módulo Administrativo
**Responsável:** Timóteo Batista

| ID | Descrição | Prioridade |
|---|---|---|
| RF-027 | O admin deve visualizar painel com totais: usuários, projetos e projetos avaliados | Alta |
| RF-028 | O painel deve exibir lista completa de usuários com filtros por turma | Média |
| RF-029 | O sistema deve criar automaticamente um usuário admin padrão na primeira execução | Alta |

### 3.6 Módulo de Portfólio Público
**Responsável:** Taywan Francisco

| ID | Descrição | Prioridade |
|---|---|---|
| RF-033 | O sistema deve exibir portfólio público com todos os projetos avaliados | Alta |
| RF-034 | O portfólio deve ter filtros por busca textual, turma e turno | Média |
| RF-035 | A página de detalhe do portfólio deve exibir nota, avaliador, tecnologias e GitHub dos integrantes | Alta |
| RF-036 | O portfólio deve exibir estatísticas gerais (total de projetos, turmas, média geral) | Média |

### 3.7 Módulo de Privacidade
**Responsável:** Taywan Francisco

| ID | Descrição | Prioridade |
|---|---|---|
| RF-030 | O sistema deve exibir página de Política de Privacidade acessível sem login | Alta |
| RF-031 | A página de login deve ter link para a Política de Privacidade | Alta |
| RF-032 | O sistema deve permitir acesso à política de privacidade pelo menu do usuário logado | Média |

---

## 4. Requisitos Não Funcionais

### 4.1 Segurança
**Responsável:** Pedro Roberto / Ivan Roberto

| ID | Descrição |
|---|---|
| RNF-001 | Senhas devem ser armazenadas com hash seguro (Werkzeug/bcrypt) |
| RNF-002 | Todas as rotas protegidas devem exigir autenticação ativa |
| RNF-003 | Controle de acesso por perfil deve ser validado no servidor (não apenas na interface) |
| RNF-004 | Nomes de arquivos enviados devem ser sanitizados (secure_filename) |
| RNF-005 | A chave secreta da aplicação deve ser configurada via variável de ambiente |
| RNF-006 | O sistema deve estar em conformidade com a LGPD (Lei nº 13.709/2018) |

### 4.2 Usabilidade
**Responsável:** Filipe José

| ID | Descrição |
|---|---|
| RNF-007 | A interface deve ser responsiva para dispositivos móveis e desktop |
| RNF-008 | Mensagens de feedback devem ser exibidas após toda ação do usuário (flash messages) |
| RNF-009 | Ações destrutivas (excluir) devem solicitar confirmação do usuário |
| RNF-010 | O sistema deve utilizar tipografia e identidade visual consistente (fonte Sora) |

### 4.3 Desempenho
**Responsável:** Ivan Roberto

| ID | Descrição |
|---|---|
| RNF-011 | O sistema deve responder a requisições em menos de 3 segundos em ambiente local |
| RNF-012 | O banco de dados deve suportar múltiplas conexões simultâneas via pool do SQLAlchemy |

### 4.4 Manutenibilidade
**Responsável:** Ivan Roberto / Pedro Roberto

| ID | Descrição |
|---|---|
| RNF-013 | O código deve seguir a arquitetura MVC com Blueprints do Flask |
| RNF-014 | Migrações de banco de dados devem ser aplicadas automaticamente no startup |
| RNF-015 | O projeto deve ser versionado com Git e hospedado no GitHub |
| RNF-016 | O repositório deve conter README bilíngue (pt-BR e en) |

### 4.5 Portabilidade
**Responsável:** Ivan Roberto

| ID | Descrição |
|---|---|
| RNF-017 | O sistema deve funcionar em Windows, Linux e macOS |
| RNF-018 | Todas as dependências devem estar listadas no arquivo `requirements.txt` |

---

## 5. Diagrama de Casos de Uso

```
┌─────────────────────────────────────────────────────────────────┐
│                   Observatório de Projetos Integradores          │
│                                                                  │
│  [Aluno]──────────────► (Fazer Login)                           │
│      │                  (Submeter Projeto)                       │
│      │                  (Editar Projeto)                         │
│      │                  (Excluir Projeto)                        │
│      └──────────────► (Visualizar Meus Projetos)                 │
│                                                                  │
│  [Professor]──────────► (Fazer Login)                           │
│      │                  (Visualizar Todos os Projetos)           │
│      │                  (Avaliar Projeto)                        │
│      └──────────────► (Cadastrar/Editar Aluno)                   │
│                                                                  │
│  [Admin]──────────────► (Fazer Login)                           │
│      │                  (Gerenciar Usuários — CRUD)              │
│      │                  (Visualizar Dashboard)                   │
│      └──────────────► (Avaliar Projeto)                          │
│                                                                  │
│  [Qualquer perfil]────► (Ver Política de Privacidade)           │
│  [Público/Empresa]────► (Ver Portfólio de Projetos)             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Modelo de Dados (Diagrama de Classes Simplificado)

```
┌──────────────────────┐        ┌──────────────────────┐
│       Usuario        │        │        Projeto        │
├──────────────────────┤        ├──────────────────────┤
│ id: Integer (PK)     │        │ id: Integer (PK)      │
│ nome: String(150)    │        │ titulo: String(200)   │
│ email: String(150)   │◄───────│ descricao: Text       │
│ senha: String(256)   │  1..n  │ tecnologias: String   │
│ perfil: Enum         │        │ link_github: String   │
│ turma: String(50)    │        │ arquivo: String       │
│ turno: Enum          │        │ participantes: Text   │
│ criado_em: DateTime  │        │ status: Enum          │
└──────────────────────┘        │ aluno_id: FK          │
                                │ criado_em: DateTime   │
                                └──────────┬───────────┘
                                           │ 1..1
                                ┌──────────▼───────────┐
                                │       Avaliacao       │
                                ├──────────────────────┤
                                │ id: Integer (PK)      │
                                │ nota: Float           │
                                │ nota_funcionalidade   │
                                │ nota_codigo           │
                                │ nota_documentacao     │
                                │ nota_interface        │
                                │ nota_apresentacao     │
                                │ comentario: Text      │
                                │ projeto_id: FK        │
                                │ professor_id: FK      │
                                │ criado_em: DateTime   │
                                └──────────────────────┘

Status do Projeto: enviado → em_avaliacao → avaliado
Perfis de Usuário: aluno | professor | admin | empresa
Turnos: manha | tarde | noite
```

---

## 7. Regras de Negócio

| ID | Regra |
|---|---|
| RN-001 | Apenas Admin/Coordenador pode cadastrar professores e administradores |
| RN-002 | Professores podem cadastrar somente alunos |
| RN-003 | Alunos só visualizam e gerenciam seus próprios projetos |
| RN-004 | Professores e admins visualizam e avaliam todos os projetos |
| RN-005 | Um projeto avaliado não pode ser editado pelo aluno |
| RN-006 | A avaliação pode ser atualizada pelo avaliador mesmo após registrada |
| RN-007 | Status segue fluxo unidirecional: enviado → em_avaliacao → avaliado |
| RN-008 | Nota válida: entre 0,0 e 10,0 |
| RN-009 | Usuário com projetos vinculados não pode ser excluído |
| RN-010 | Um administrador não pode excluir a própria conta |
| RN-011 | E-mail deve ser único no sistema |
| RN-012 | Senhas são armazenadas sempre como hash (nunca em texto plano) |

---

## 8. Rastreabilidade por Requisito e Desenvolvedor

| Requisito | Arquivo de Implementação | Desenvolvedor |
|---|---|---|
| RF-001 a RF-005 | `routes/auth.py` | **Pedro Roberto** |
| RF-006 a RF-012 | `routes/admin.py` | **Timóteo Batista** |
| RF-013 a RF-021 | `routes/projetos.py`, `templates/projeto_form.html`, `templates/projeto_detalhe.html` | **Guilherme Gonçalves** |
| RF-022 a RF-026 | `routes/projetos.py` (avaliar_projeto), `templates/avaliar.html` | **Guilherme Gonçalves** |
| RF-027 a RF-029 | `routes/admin.py`, `templates/admin/dashboard.html` | **Timóteo Batista** |
| RF-030 a RF-032 | `routes/lgpd.py`, `templates/privacidade.html` | **Taywan Francisco** |
| RF-033 a RF-036 | `routes/portfolio.py`, `templates/portfolio.html`, `templates/portfolio_detalhe.html` | **Taywan Francisco** |
| RNF-001, RNF-003 | `routes/auth.py`, todos os `routes/*.py` | **Pedro Roberto** |
| RNF-002, RNF-004 | `routes/projetos.py`, `config.py` | **Pedro Roberto** |
| RNF-005 | `config.py` | **Ivan Roberto** |
| RNF-006 | `templates/privacidade.html`, `routes/lgpd.py` | **Taywan Francisco** |
| RNF-007 a RNF-010 | `templates/base.html`, `templates/login.html`, `templates/painel.html` | **Filipe José** |
| RNF-011 a RNF-012 | `models.py`, `config.py` | **Ivan Roberto** |
| RNF-013 a RNF-014 | `app.py`, `models.py` | **Ivan Roberto** / **Pedro Roberto** |
| RNF-015 a RNF-016 | `README.md`, `docs/` | **Filipe José** |
| RNF-017 a RNF-018 | `requirements.txt`, `config.py` | **Ivan Roberto** |
| Modelo de Dados | `models.py` | **Ivan Roberto** |
| Documentação técnica | `docs/requisitos.md`, `README.md` | **Filipe José** |

---

## 9. Distribuição de Responsabilidades por Membro

### 👑 Ivan Roberto — Líder Técnico & Arquiteto do Sistema
Ivan atuou como **líder e cabeça do projeto**, responsável pelas decisões arquiteturais que estruturam todo o sistema. Orientou os demais membros na implementação de suas partes e garantiu a coesão técnica do projeto como um todo.

- `models.py` — modelos `Usuario`, `Projeto`, `Avaliacao`, relacionamentos ORM, design do banco de dados
- `config.py` — configuração de banco, `UPLOAD_FOLDER`, `MAX_CONTENT_LENGTH`, suporte SQLite/MySQL
- `app.py` — função `aplicar_migrations()`, inicialização do SQLAlchemy, estrutura de Blueprints
- `requirements.txt` — gestão de dependências
- Coordenação técnica geral do time

### 🔐 Pedro Roberto — Autenticação & Setup da Aplicação
- `routes/auth.py` — login, logout, proteção de rotas com Flask-Login
- `app.py` — configuração principal, registro de Blueprints, filtro `from_json`, criação do admin padrão

### 📁 Guilherme Gonçalves — Módulo de Projetos & Avaliação
- `routes/projetos.py` — submissão, edição, exclusão, download e avaliação com rubrica
- `templates/projeto_form.html` — formulário de submissão/edição
- `templates/projeto_detalhe.html` — visualização detalhada do projeto
- `templates/avaliar.html` — formulário de avaliação com rubrica ponderada

### 🛠️ Timóteo Batista — Painel Administrativo
- `routes/admin.py` — dashboard, CRUD de usuários, exportação CSV, filtros
- `templates/admin/dashboard.html` — painel com métricas, gráficos e tabelas
- `templates/admin/aluno_form.html` — formulário de cadastro de aluno
- `templates/admin/usuario_form.html` — formulário de cadastro de usuário (admin)

### 🌐 Taywan Francisco — Portfólio Público & LGPD
- `routes/portfolio.py` — listagem pública de projetos avaliados com filtros
- `templates/portfolio.html` — página do portfólio com hero e cards
- `templates/portfolio_detalhe.html` — detalhe público de projeto no portfólio
- `routes/lgpd.py` — rota da política de privacidade
- `templates/privacidade.html` — página de Política de Privacidade (LGPD)

### 🎨 Filipe José — Interface, UX & Documentação
- `templates/base.html` — layout base, navegação, identidade visual, CSS global
- `templates/login.html` — tela de login
- `templates/painel.html` — painel do aluno/professor
- `templates/usuario_form.html` — formulário de perfil de usuário
- `docs/requisitos.md` — este documento
- `README.md` — documentação bilíngue do projeto

---

*Documento gerado para fins acadêmicos — ADS 2º Módulo Senac · 2025*
