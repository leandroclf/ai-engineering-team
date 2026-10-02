---
titulo: "Visão geral da solução"
projeto: "ai-engineering-team"
autor: "Não informado"
data: "2026-10-01"
versao: "1.0.0"
classificacao: "Não informada"
status: "Rascunho para revisão"
---

# Visão geral da solução

Navegação: [Índice](00-toc.md) · anterior: [01 Contexto](01-contexto.md) · próximo: [03 Requisitos funcionais](03-requisitos-funcionais.md)

## Natureza da solução

✅ **Confirmado:** o ai-engineering-team é um conjunto de **artefatos declarativos** (Markdown e YAML) acompanhados de scripts de validação e orquestração. Não há servidor, banco de dados nem interface própria. O próprio `docs/VALIDATION.md` registra que o framework é "primariamente Markdown declarativo".

O comportamento dos agentes é governado por texto: o que está em `AGENTS.md`, nas skills, nos templates e nas specs **é** o comportamento do sistema. Por isso alterar esses arquivos equivale a alterar código de produção, e a recomendação de não mexer nos artefatos normativos sem autorização (REC-004, REC-006, REC-009, REC-010 e REC-011) decorre dessa natureza.

## Arquitetura

![Arquitetura em planos de controle](anexos/diagramas/01-arquitetura-planos.png)

Fonte editável: [01-arquitetura-planos.mmd](anexos/diagramas/01-arquitetura-planos.mmd).

O design de endurecimento define quatro planos, em que um plano inferior pode ser mais estrito, nunca mais fraco que um superior:

1. **Plano nativo do Dot:** identidade, memória, plugins, visão de atividade, Custom Rules e revisão nativa de ações.
2. **Plano de governança:** este repositório (OpenSpec, AGENTS.md, skills, registro, roteamento, risco, evidência).
3. **Plano de execução:** Codex para código; Work para pesquisa e artefatos; plugins para sistemas externos.
4. **Plano do repositório alvo:** instruções locais, proteções de branch, CI, testes e controles de deploy.

As camadas lógicas do design de bootstrap complementam esse quadro: L0 governança, L1 orquestração, L2 skills especialistas, L3 adaptadores de projeto, L4 adaptadores de ferramentas e L5 evidência.

## Componentes

| Componente | Caminho | Função |
| --- | --- | --- |
| Contrato dos agentes | `AGENTS.md` | Missão, precedência, ciclo de vida, risco, roteamento, confiabilidade, concorrência, regras de engenharia, definição de pronto, recuperação e relatório |
| Skills (13) | `skills/` | Núcleo: tech-lead, architect, backend, qa, security, code-review, observability. Stack: java-spring, node-typescript, python-fastapi, aws, kubernetes. Fluxo: github-workflow |
| Políticas e arquitetura | `docs/*.md`, `docs/adr/`, `docs/workflows/` | Frescor, isolamento, confiabilidade, concorrência, entrega, recuperação, roteamento, plugins, dupla revisão, garantia entre fornecedores, ambientes de execução e fluxos de trabalho |
| Templates e contratos | `templates/` (23 arquivos) | Envelope de tarefa, lease, evidência, manifest de política, registro de projetos, pedido e resultado de revisão, waiver, bootstrap do Atlas e do Sentinel, relatório de conclusão |
| Runbooks | `runbooks/` (4) | Configuração do Atlas e do Sentinel, garantia pelo Claude e runtimes em contêiner |
| OpenSpec | `openspec/` | Visão do projeto, roadmap, 5 specs de capacidade e 6 mudanças com proposta, design e tarefas |
| Validação | `validation/`, `tests/scenarios.md` | Cenários, fixtures, manifests e relatórios de execução, waivers |
| Scripts | `scripts/` (4) | `validate.py` e `validate_hardening.py` (CI), `provider_run.py` (harness) e `pr_chain.sh` (transporte por GitHub) |
| Runtimes | `runtimes/` | `Dockerfile` e `compose.yaml` dos três contêineres |
| CI | `.github/workflows/validate.yml` | Executa os dois validadores em push e PR |

## Tecnologias e dependências

| Item | Detalhe | Evidência |
| --- | --- | --- |
| Linguagens | Markdown e YAML (artefatos); Python 3 (validadores e harness); Bash (`pr_chain.sh`); Dockerfile e Compose | `scripts/`, `runtimes/` |
| Biblioteca Python | PyYAML, usada por `validate.py`, `validate_hardening.py` e `provider_run.py` | `.github/workflows/validate.yml` (`pip install pyyaml`) |
| CI | GitHub Actions, `ubuntu-latest`, `actions/checkout@v4`, `actions/setup-python@v5` com Python 3.12 | `.github/workflows/validate.yml` |
| Imagem dos contêineres | `node:22-bookworm-slim` com git, python3, python3-yaml, ripgrep e ca-certificates | `runtimes/Dockerfile` |
| CLIs de provedor | `@openai/codex` 0.159.3 e `@anthropic-ai/claude-code` 2.1.287, versões fixadas por argumento de build | `runtimes/Dockerfile` |
| Isolamento do contêiner | Usuário sem root com UID do host, rootfs somente leitura, `/tmp` em tmpfs, `cap_drop: ALL`, `no-new-privileges` | `runtimes/compose.yaml` |
| Orquestração local | Docker Compose, CLI `gh`, Git | `scripts/pr_chain.sh`, `scripts/provider_run.py` |

⚠️ **Atenção:** a dependência PyYAML não tem versão fixada nem arquivo de requisitos; o CI instala a versão corrente. A imagem base é referenciada por tag, não por digest. Nenhuma das duas condições está registrada como decisão.

## Ciclo de vida do trabalho

![Ciclo de vida do trabalho](anexos/diagramas/03-ciclo-de-vida.png)

Fonte editável: [03-ciclo-de-vida.mmd](anexos/diagramas/03-ciclo-de-vida.mmd).

O ciclo de vida aparece em três versões nos documentos de origem:

| Versão | Etapas | Fonte |
| --- | --- | --- |
| AGENTS.md | INTAKE, FRESHNESS, DISCOVER, CLASSIFY, LEASE, PLAN, EXECUTE, VERIFY, REVIEW, REPORT (10) | `AGENTS.md` |
| Design do bootstrap | INTAKE, DISCOVER, PLAN, EXECUTE, VERIFY, REVIEW, REPORT (7), com aprovação antes de ações de alto risco | `openspec/changes/bootstrap-agentic-engineering-team/design.md` |
| Design de endurecimento | INTAKE, FRESHNESS, CLASSIFY, LEASE, PLAN, EXECUTE, VERIFY, REVIEW, PR, CI, APPROVAL, MERGE, RELEASE, OBSERVE, CLOSE (15) | `openspec/changes/harden-engineering-dot/design.md` |

🔄 **Regra de leitura adotada nesta documentação:** o ciclo do `AGENTS.md` é o normativo para a condução do trabalho (a precedência põe o AGENTS.md acima do OpenSpec e das skills); a variante de 7 etapas é anterior e subconjunto dele; as etapas de PR a CLOSE do design de endurecimento estendem o ciclo para a entrega e não substituem as etapas anteriores. Isso é uma **interpretação** que dá coerência às fontes. As fontes não declaram essa hierarquia; a harmonização nos documentos de origem está pendente (REC-004).

## Fluxos principais

### Decisão por classe de risco

![Decisão por classe de risco](anexos/diagramas/02-decisao-risco.png)

Fonte editável: [02-decisao-risco.mmd](anexos/diagramas/02-decisao-risco.mmd). Regras: RN-004, RN-005, RN-006, RN-007 em [05-regras-de-negocio.md](05-regras-de-negocio.md).

### Cadeia de revisão independente

![Cadeia de revisão independente](anexos/diagramas/04-cadeia-revisao.png)

Fonte editável: [04-cadeia-revisao.mmd](anexos/diagramas/04-cadeia-revisao.mmd). Regras: RN-036 a RN-041. O transporte é o repositório: pedido e veredito ficam presos a um SHA imutável; nenhuma sessão compartilhada entre modelos é necessária.

### Tratamento de achados

![Decisão sobre achados](anexos/diagramas/05-decisao-achado.png)

Fonte editável: [05-decisao-achado.mmd](anexos/diagramas/05-decisao-achado.mmd). Regras: RN-038 e RN-039.

### Mutação externa, retentativa e circuit breaker

![Retentativa e circuit breaker](anexos/diagramas/07-retentativa-circuito.png)

Fonte editável: [07-retentativa-circuito.mmd](anexos/diagramas/07-retentativa-circuito.mmd). Regras: RN-024 a RN-026.

### Execução por CLI em contêineres

![Runtimes em contêineres](anexos/diagramas/06-runtimes-conteineres.png)

Fonte editável: [06-runtimes-conteineres.mmd](anexos/diagramas/06-runtimes-conteineres.mmd). Regras: RN-042, RN-043 e RN-052. O orquestrador roda no host com a identidade do operador; os agentes rodam nos contêineres e **não recebem credenciais do GitHub**.

## Protótipos e mockups

Não há protótipos, telas, wireframes nem capturas de tela deste sistema: ele não possui interface própria. As visualizações disponíveis são os sete diagramas desta documentação, listados acima, com fonte editável em `docs/anexos/diagramas/`.

⚠️ **Atenção:** as imagens do diretório de identidade visual (cartões, publicações, telas de exemplo) são aplicações de **marca** e não representam este sistema; foram usadas somente como referência de identidade (ver [anexos/identidade/README.md](anexos/identidade/README.md)).

## Dependências e integrações

| Integração | Natureza | Uso | Contrato | Evidência |
| --- | --- | --- | --- | --- |
| GitHub (repositório, PR, CI) | Sistema terceiro | Hospeda o repositório, executa o CI e recebe os statuses por SHA | Parcial: [github-commit-status.yaml](anexos/swagger/github-commit-status.yaml) cobre o status de commit | `scripts/pr_chain.sh`, `.github/workflows/validate.yml` |
| CLI `gh` | Ferramenta | Cria e fecha PR, comenta, lista execuções do CI e chama a API de status | Contrato da CLI não documentado | `scripts/pr_chain.sh` |
| Codex CLI (OpenAI) | Serviço de provedor | Atlas e Sentinel no plano de execução, por assinatura | Fornecido pelo provedor | `runtimes/Dockerfile`, `scripts/provider_run.py` |
| Claude Code CLI (Anthropic) | Serviço de provedor | Argus, por assinatura | Fornecido pelo provedor | `runtimes/Dockerfile`, `scripts/provider_run.py` |
| Docker e Compose | Infraestrutura local | Contêineres por conta com volumes de credenciais | `runtimes/compose.yaml` | `runbooks/CONTAINER-RUNTIMES.md` |
| Engineering Dot (Atlas e Sentinel ao vivo) | Plataforma nativa | Coordenação persistente e revisão independente | Não exercitada | `docs/DOT-NATIVE-ARCHITECTURE.md` |
| Plugins e apps conectados | Sistemas externos | Leitura e ação estreita sob permissões nativas | Matriz em `templates/PLUGIN-ACCESS-MATRIX.yaml` | `docs/DOT-PLUGIN-POLICY.md` |
| ChatGPT Work | Superfície nativa | Pesquisa e artefatos | Não exercitada | `docs/ROUTING-MATRIX.md` |

Não há banco de dados, fila, microsserviço ou serviço de autenticação próprios. A autenticação é de responsabilidade de cada CLI (login interativo por assinatura), com credenciais mantidas só nos volumes Docker por conta.

⚠️ **Atenção:** `templates/PROJECT-REGISTRY.yaml` declara `python scripts/validate.py` como validação do projeto, enquanto o CI executa também `scripts/validate_hardening.py` e instala PyYAML. A divergência está registrada como REC-011.
