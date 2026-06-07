# 🔬 Pesquisa, Tecnologia e Sociedade
**Sistema:** Observatório de Projetos Integradores  
**Curso:** Análise e Desenvolvimento de Sistemas — Senac Fecomércio  
**Módulo:** 2º Módulo  
**Versão:** 1.0  
**Data:** 2026

---

## 1. Definição do Problema

### 1.1 Contexto
O Projeto Integrador (PI) é uma atividade central nos cursos técnicos e de graduação tecnológica do Senac. No 2º Módulo do curso de Análise e Desenvolvimento de Sistemas, os alunos desenvolvem sistemas de software como síntese das competências adquiridas nas Unidades Curriculares (UCs). No entanto, o processo de entrega, avaliação e consulta desses projetos ocorre de forma **descentralizada**, dispersa em diferentes ferramentas como e-mail institucional, Microsoft Teams e pastas compartilhadas.

### 1.2 Problema Identificado
Esse modelo descentralizado gera os seguintes problemas:

- **Dificuldade de rastreamento:** professores e coordenadores não têm visão unificada dos projetos entregues por turma, turno ou aluno.
- **Perda de histórico:** projetos enviados por e-mail não são facilmente localizados ou consultados posteriormente.
- **Falta de padronização:** não há um formato único de submissão, dificultando a comparação e avaliação.
- **Baixa visibilidade institucional:** empresas parceiras e interessados externos não têm acesso ao portfólio de projetos desenvolvidos pelos alunos.
- **Gargalo na avaliação:** professores precisam organizar manualmente os arquivos recebidos, aumentando o risco de erros e atrasos.

### 1.3 Pergunta de Pesquisa
> *Como uma plataforma web centralizada pode melhorar o processo de submissão, avaliação e visibilidade dos Projetos Integradores no curso de ADS do Senac?*

---

## 2. Revisão de Literatura

### 2.1 Gestão de Projetos Acadêmicos e Tecnologia
Estudos na área de educação tecnológica apontam que a adoção de plataformas digitais integradas melhora significativamente o acompanhamento do aprendizado e a gestão de entregas acadêmicas. Sistemas como **Moodle**, **Google Classroom** e **GitHub Education** demonstram que ambientes digitais estruturados aumentam o engajamento dos alunos e a eficiência da avaliação docente (MORAN, 2015; VALENTE, 2018).

### 2.2 Desenvolvimento Web com Python e Flask
O Python é consistentemente apontado como uma das linguagens mais utilizadas para desenvolvimento web, especialmente em contextos educacionais e de prototipagem. O framework Flask, por sua leveza e flexibilidade, é amplamente recomendado para sistemas de pequeno e médio porte que precisam de rápido desenvolvimento sem abrir mão de escalabilidade (GRINBERG, 2018). A combinação Flask + SQLAlchemy permite implementar padrões MVC de forma clara e com pouco código boilerplate.

### 2.3 LGPD e Proteção de Dados em Sistemas Educacionais
A Lei nº 13.709/2018 (LGPD) estabelece diretrizes obrigatórias para o tratamento de dados pessoais no Brasil. Em sistemas educacionais, essa preocupação é ainda mais relevante pois envolve dados de menores de idade e informações sensíveis sobre desempenho acadêmico. A LGPD exige consentimento informado, finalidade clara, minimização dos dados coletados e mecanismos de acesso e exclusão para os titulares (BIONI, 2019).

### 2.4 Controle de Acesso Baseado em Papéis (RBAC)
O modelo RBAC (*Role-Based Access Control*) é uma das abordagens mais difundidas para controle de acesso em sistemas multiusuário. Ao atribuir permissões a papéis (e não diretamente a usuários), o sistema torna-se mais fácil de gerenciar e auditar (FERRAIOLO; SANDHU; GAVRILA, 2001). No Observatório, esse modelo é implementado com os perfis: aluno, professor e admin.

---

## 3. Metodologia de Desenvolvimento

### 3.1 Abordagem
O projeto foi desenvolvido seguindo uma abordagem **iterativa e incremental**, inspirada nos princípios ágeis. As funcionalidades foram priorizadas por valor de negócio e implementadas em ciclos curtos, permitindo validação contínua.

### 3.2 Etapas do Desenvolvimento

| Etapa | Atividade | Ferramentas |
|---|---|---|
| 1. Análise | Levantamento de requisitos, definição dos perfis de usuário e regras de negócio | Reuniões, Trello |
| 2. Modelagem | Diagrama de classes, modelo de banco de dados, wireframes da interface | Draw.io, papel |
| 3. Implementação | Codificação do backend (Flask), banco de dados (MySQL), templates (HTML/CSS) | VS Code, Python |
| 4. Testes | Testes manuais de cada fluxo por perfil de usuário | Navegador, Postman |
| 5. Documentação | README, requisitos, política de privacidade, metodologia | Markdown, GitHub |
| 6. Entrega | Submissão do código e documentação no repositório GitHub | Git, GitHub |

### 3.3 Arquitetura do Sistema
O sistema segue o padrão arquitetural **MVC (Model-View-Controller)**, implementado com:

- **Model:** `models.py` — define as entidades do banco de dados com Flask-SQLAlchemy
- **View:** `templates/` — arquivos HTML com Jinja2 para renderização dinâmica
- **Controller:** `routes/` — Blueprints do Flask organizando as rotas por domínio (auth, projetos, admin, lgpd)

### 3.4 Stack Tecnológica Justificada

| Tecnologia | Justificativa |
|---|---|
| Python 3.x | Linguagem aprendida no módulo; ampla comunidade; produtividade alta |
| Flask 3.x | Microframework flexível; fácil aprendizado; sem overhead de frameworks maiores |
| MySQL | SGBD relacional robusto; compatível com os padrões aprendidos na UC de Banco de Dados |
| SQLAlchemy | ORM que abstrai o SQL; facilita migrações e manutenção |
| HTML5 + CSS3 | Padrões web modernos; interface responsiva sem dependência de frameworks pesados |
| Git + GitHub | Versionamento obrigatório; permite colaboração e rastreabilidade de mudanças |
| Trello | Gestão de tarefas visual; alinhado à metodologia ágil |

---

## 4. Análise de Viabilidade

### 4.1 Viabilidade Técnica
O sistema foi desenvolvido com tecnologias amplamente documentadas e de código aberto, eliminando custos de licença. O stack Python + Flask + MySQL roda em qualquer sistema operacional e pode ser hospedado em servidores VPS acessíveis (como DigitalOcean, Railway ou servidores da própria instituição). A complexidade técnica está dentro do escopo do 2º Módulo de ADS.

### 4.2 Viabilidade Operacional
O sistema substitui um processo manual existente, portanto já existe demanda real. A curva de aprendizado para professores e alunos é baixa, pois a interface é intuitiva e segue padrões familiares de plataformas web. O processo de implantação requer apenas um servidor com Python e MySQL instalados.

### 4.3 Viabilidade Econômica

| Item | Custo estimado |
|---|---|
| Infraestrutura (servidor VPS básico) | R$ 50–100/mês |
| Domínio (.com.br) | R$ 40/ano |
| Manutenção (após implantação) | Mínima, realizada pela própria equipe técnica do Senac |
| Licenças de software | R$ 0 (todo stack é open-source) |

O custo é significativamente inferior ao impacto gerado pela centralização do processo e pela visibilidade institucional dos projetos.

### 4.4 Viabilidade Legal
O sistema foi projetado em conformidade com a **LGPD (Lei nº 13.709/2018)**, coletando apenas os dados estritamente necessários para o funcionamento da plataforma, informando claramente aos usuários sobre o uso de seus dados e implementando mecanismos de controle de acesso adequados.

---

## 5. Resultados Esperados

| Resultado | Indicador de Sucesso |
|---|---|
| Centralização das entregas de PI | 100% dos projetos submetidos pela plataforma, eliminando e-mail/Teams |
| Agilidade na avaliação | Redução do tempo de avaliação em pelo menos 50% (feedback esperado) |
| Rastreabilidade total | Todo projeto com status visível e histórico de avaliação registrado |
| Visibilidade institucional | Acesso ao portfólio de projetos por professores, admins e parceiros |
| Conformidade com LGPD | Política de privacidade publicada e controle de acesso implementado |
| Portfólio dos alunos | Cada aluno tem um histórico de projetos acessível pelo sistema |

---

## 6. Impacto Social e Tecnológico

### 6.1 Impacto para os Alunos
A plataforma cria um **portfólio digital rastreável** dos projetos desenvolvidos ao longo do curso, o que tem valor direto para o mercado de trabalho. Alunos podem compartilhar o link do GitHub vinculado ao projeto, aumentando sua visibilidade profissional.

### 6.2 Impacto para a Instituição
O Senac passa a ter uma visão estratégica e centralizada da produção acadêmica dos alunos. Isso possibilita análises qualitativas por turma, turno e módulo, subsidiando decisões pedagógicas e a melhoria contínua do curso.

### 6.3 Impacto para o Mercado
Empresas parceiras do Senac poderão consultar projetos e identificar talentos diretamente na plataforma, criando uma ponte entre a formação acadêmica e o mercado de trabalho — impacto social direto da tecnologia desenvolvida.

### 6.4 Responsabilidade do Desenvolvedor
O desenvolvimento deste sistema reforça a consciência sobre a **responsabilidade ética e legal** do profissional de TI: proteger dados dos usuários, garantir acessibilidade, documentar o código e seguir as legislações vigentes. O projeto aplica na prática os conceitos discutidos nas UCs de Legislação e Pesquisa, Tecnologia e Sociedade.

---

## 7. Referências

- BIONI, Bruno Ricardo. *Proteção de Dados Pessoais: A Função e os Limites do Consentimento*. Rio de Janeiro: Forense, 2019.
- FERRAIOLO, D.; SANDHU, R.; GAVRILA, S. *Proposed NIST Standard for Role-Based Access Control*. ACM Transactions on Information and System Security, 2001.
- GRINBERG, Miguel. *Flask Web Development: Developing Web Applications with Python*. 2. ed. O'Reilly Media, 2018.
- MORAN, José Manuel. *Educação híbrida: um conceito-chave para a educação hoje*. In: BACICH, L.; NETO, A. T.; TREVISANI, F. M. (Org.). *Ensino Híbrido: Personalização e Tecnologia na Educação*. Porto Alegre: Penso, 2015.
- VALENTE, José Armando. *A sala de aula invertida e a possibilidade do ensino personalizado*. In: BACICH, L.; MORAN, J. (Org.). *Metodologias Ativas para uma Educação Inovadora*. Porto Alegre: Penso, 2018.
- BRASIL. *Lei nº 13.709, de 14 de agosto de 2018*. Lei Geral de Proteção de Dados Pessoais (LGPD). Diário Oficial da União, Brasília, 2018.

---

*Documento gerado para fins acadêmicos — ADS 2º Módulo Senac · 2025*
