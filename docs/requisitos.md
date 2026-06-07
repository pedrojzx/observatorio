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

| ID | Descrição | Prioridade |
|---|---|---|
| RF-001 | O sistema deve permitir login com e-mail e senha | Alta |
| RF-002 | O sistema deve manter sessão autenticada por cookie seguro | Alta |
| RF-003 | O sistema deve redirecionar usuário não autenticado para a tela de login | Alta |
| RF-004 | O sistema deve permitir logout com encerramento de sessão | Alta |
| RF-005 | O sistema deve exibir mensagem de erro para credenciais inválidas | Média |

### 3.2 Módulo de Usuários

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

| ID | Descrição | Prioridade |
|---|---|---|
| RF-022 | O professor e o admin devem poder avaliar projetos com nota (0 a 10) e comentário | Alta |
| RF-023 | Ao abrir um projeto para avaliação, o status deve mudar automaticamente para "em_avaliacao" | Alta |
| RF-024 | Após avaliação, o status deve mudar para "avaliado" | Alta |
| RF-025 | A avaliação de um projeto pode ser atualizada pelo avaliador | Média |
| RF-026 | O aluno não deve poder avaliar projetos | Alta |

### 3.5 Módulo Administrativo

| ID | Descrição | Prioridade |
|---|---|---|
| RF-027 | O admin deve visualizar painel com totais: usuários, projetos e projetos avaliados | Alta |
| RF-028 | O painel deve exibir lista completa de usuários com filtros por turma | Média |
| RF-029 | O sistema deve criar automaticamente um usuário admin padrão na primeira execução | Alta |

### 3.6 Módulo de Privacidade

| ID | Descrição | Prioridade |
|---|---|---|
| RF-030 | O sistema deve exibir página de Política de Privacidade acessível sem login | Alta |
| RF-031 | A página de login deve ter link para a Política de Privacidade | Alta |
| RF-032 | O sistema deve permitir acesso à política de privacidade pelo menu do usuário logado | Média |

---

## 4. Requisitos Não Funcionais

### 4.1 Segurança

| ID | Descrição |
|---|---|
| RNF-001 | Senhas devem ser armazenadas com hash seguro (Werkzeug/bcrypt) |
| RNF-002 | Todas as rotas protegidas devem exigir autenticação ativa |
| RNF-003 | Controle de acesso por perfil deve ser validado no servidor (não apenas na interface) |
| RNF-004 | Nomes de arquivos enviados devem ser sanitizados (secure_filename) |
| RNF-005 | A chave secreta da aplicação deve ser configurada via variável de ambiente |
| RNF-006 | O sistema deve estar em conformidade com a LGPD (Lei nº 13.709/2018) |

### 4.2 Usabilidade

| ID | Descrição |
|---|---|
| RNF-007 | A interface deve ser responsiva para dispositivos móveis e desktop |
| RNF-008 | Mensagens de feedback devem ser exibidas após toda ação do usuário (flash messages) |
| RNF-009 | Ações destrutivas (excluir) devem solicitar confirmação do usuário |
| RNF-010 | O sistema deve utilizar tipografia e identidade visual consistente (fonte Sora) |

### 4.3 Desempenho

| ID | Descrição |
|---|---|
| RNF-011 | O sistema deve responder a requisições em menos de 3 segundos em ambiente local |
| RNF-012 | O banco de dados deve suportar múltiplas conexões simultâneas via pool do SQLAlchemy |

### 4.4 Manutenibilidade

| ID | Descrição |
|---|---|
| RNF-013 | O código deve seguir a arquitetura MVC com Blueprints do Flask |
| RNF-014 | Migrações de banco de dados devem ser aplicadas automaticamente no startup |
| RNF-015 | O projeto deve ser versionado com Git e hospedado no GitHub |
| RNF-016 | O repositório deve conter README bilíngue (pt-BR e en) |

### 4.5 Portabilidade

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
│ turno: Enum          │        │ status: Enum          │
│ criado_em: DateTime  │        │ aluno_id: FK          │
└──────────────────────┘        │ criado_em: DateTime   │
                                └──────────┬───────────┘
                                           │ 1..1
                                ┌──────────▼───────────┐
                                │       Avaliacao       │
                                ├──────────────────────┤
                                │ id: Integer (PK)      │
                                │ nota: Float           │
                                │ comentario: Text      │
                                │ projeto_id: FK        │
                                │ professor_id: FK      │
                                │ criado_em: DateTime   │
                                └──────────────────────┘

Status do Projeto: enviado → em_avaliacao → avaliado
Perfis de Usuário: aluno | professor | admin
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

## 8. Rastreabilidade

| Requisito | Arquivo de Implementação |
|---|---|
| RF-001 a RF-005 | `routes/auth.py` |
| RF-006 a RF-012 | `routes/admin.py` |
| RF-013 a RF-021 | `routes/projetos.py` |
| RF-022 a RF-026 | `routes/projetos.py` (avaliar_projeto) |
| RF-027 a RF-029 | `routes/admin.py` (dashboard) |
| RF-030 a RF-032 | `routes/lgpd.py` |
| RNF-001 a RNF-006 | `models.py`, `config.py`, `routes/` |
| Modelo de Dados | `models.py` |

---

*Documento gerado para fins acadêmicos — ADS 2º Módulo Senac · 2025*
