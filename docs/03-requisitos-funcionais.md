---
titulo: "Requisitos funcionais"
projeto: "ai-engineering-team"
autor: "Não informado"
data: "2026-10-01"
versao: "1.0.0"
classificacao: "Não informada"
status: "Rascunho para revisão"
---

# Requisitos funcionais

> Baseline de requisitos/analises: revisão `791ac89`, 2026-10-01. Identificadores e recomendações históricas são preservados. Para operação atual, use [guia Linux](LOCAL-LINUX-WORKFLOW.md), [visão geral atualizada](02-visao-geral.md) e [reconciliação documental](DOCUMENTATION-REVIEW.md). Esta baseline não certifica o fluxo local nem comportamento ao vivo.

Navegação: [Índice](00-toc.md) · anterior: [02 Visão geral](02-visao-geral.md) · próximo: [04 Requisitos não funcionais](04-requisitos-nao-funcionais.md)

## Como ler

Os requisitos funcionais (RF) descrevem **o que o sistema deve fazer**, escritos já revisados. Cada RF tem origem em arquivo e seção, e uma coluna de **verificação** que registra somente o que foi observado em `validation/` (nunca uma expectativa).

- ✅ **Confirmado:** todos os RF foram extraídos de especificações, políticas, templates ou código existentes. Nenhum é proposta nova.
- Os RF-022 a RF-025 têm origem **no código e nos runbooks**, porque não existe especificação formal para execução em contêineres, harness, transporte por PR e validadores (lacuna registrada em REC-006).
- As regras de negócio que sustentam cada RF estão em [05-regras-de-negocio.md](05-regras-de-negocio.md); a matriz completa está em [07-matriz-rastreabilidade.md](07-matriz-rastreabilidade.md).

<!-- BEGIN:gerado:rf-resumo -->

## Situação de verificação

| ID | Requisito | Situação |
| --- | --- | --- |
| [RF-001](03-requisitos-funcionais.md#rf-001) | Orquestração de trabalho de engenharia por um Tech Lead | Validado |
| [RF-002](03-requisitos-funcionais.md#rf-002) | Seleção proporcional de capacidades especialistas | Validado |
| [RF-003](03-requisitos-funcionais.md#rf-003) | Classificação de risco R0 a R3 | Validado |
| [RF-004](03-requisitos-funcionais.md#rf-004) | Gate de aprovação para ações R3 | Validado |
| [RF-005](03-requisitos-funcionais.md#rf-005) | Resolução de precedência de instruções | Validado |
| [RF-006](03-requisitos-funcionais.md#rf-006) | Tratamento de conteúdo não confiável | Validado |
| [RF-007](03-requisitos-funcionais.md#rf-007) | Frescor e isolamento do contexto | Parcial |
| [RF-008](03-requisitos-funcionais.md#rf-008) | Envelope de tarefa e contrato de resultado | Somente estrutura |
| [RF-009](03-requisitos-funcionais.md#rf-009) | Validação nativa e relato fiel de resultados | Validado |
| [RF-010](03-requisitos-funcionais.md#rf-010) | Relatório de conclusão e registro de evidência | Validado |
| [RF-011](03-requisitos-funcionais.md#rf-011) | Idempotência, retentativa limitada e circuit breaker | Não validado |
| [RF-012](03-requisitos-funcionais.md#rf-012) | Leases de concorrência | Não validado |
| [RF-013](03-requisitos-funcionais.md#rf-013) | Ciclo de entrega por branch, PR, CI e release separado | Parcial |
| [RF-014](03-requisitos-funcionais.md#rf-014) | Recuperação de incidentes | Não validado |
| [RF-015](03-requisitos-funcionais.md#rf-015) | Roteamento entre Dot, Codex, Work e plugins | Não validado |
| [RF-016](03-requisitos-funcionais.md#rf-016) | Política de plugins e permissões de menor privilégio | Parcial |
| [RF-017](03-requisitos-funcionais.md#rf-017) | Onboarding de projeto e registro de portfólio | Não validado |
| [RF-018](03-requisitos-funcionais.md#rf-018) | Revisão independente vinculada a SHA (Sentinel) | Validado |
| [RF-019](03-requisitos-funcionais.md#rf-019) | Protocolo de discordância e waiver | Parcial |
| [RF-020](03-requisitos-funcionais.md#rf-020) | Garantia entre fornecedores pelo Argus | Validado |
| [RF-021](03-requisitos-funcionais.md#rf-021) | Execução por CLI oficial em ambientes nomeados | Validado |
| [RF-022](03-requisitos-funcionais.md#rf-022) | Contêineres de execução isolados por conta | Validado |
| [RF-023](03-requisitos-funcionais.md#rf-023) | Harness de execução de cenários com evidência preservada | Validado |
| [RF-024](03-requisitos-funcionais.md#rf-024) | Transporte da cadeia por GitHub PR e CI | Validado |
| [RF-025](03-requisitos-funcionais.md#rf-025) | Validação estrutural automatizada em CI | Validado |
| [RF-026](03-requisitos-funcionais.md#rf-026) | Versionamento e migração de políticas e contratos | Não validado |
| [RF-027](03-requisitos-funcionais.md#rf-027) | Bootstrap e calibração do Engineering Dot | Não validado |
| [RF-028](03-requisitos-funcionais.md#rf-028) | Estado de sessão e loops autônomos controlados | Não validado |
| [RF-029](03-requisitos-funcionais.md#rf-029) | Evolução para Dots especializados | Não aplicável |
| [RF-030](03-requisitos-funcionais.md#rf-030) | Orçamentos de contexto e trabalho | Não validado |

Não aplicável: 1, Não validado: 9, Parcial: 4, Somente estrutura: 1, Validado: 15.

<!-- END:gerado:rf-resumo -->

## Requisitos

<!-- BEGIN:gerado:rf-detalhe -->

### <a id="rf-001"></a>RF-001 — Orquestração de trabalho de engenharia por um Tech Lead

- **Descrição:** O sistema deve conduzir o trabalho do objetivo à evidência (descobrir, classificar risco, planejar, executar, verificar, revisar, reportar) sob um único papel de orquestração.
- **Origem:** `openspec/specs/agent-contract/spec.md#AGENT-001`; `openspec/specs/orchestration/spec.md#ORCH-002`; `skills/tech-lead/SKILL.md#Tech Lead`
- **Regras de negócio:** [RN-007](05-regras-de-negocio.md#rn-007), [RN-008](05-regras-de-negocio.md#rn-008), [RN-012](05-regras-de-negocio.md#rn-012), [RN-014](05-regras-de-negocio.md#rn-014), [RN-015](05-regras-de-negocio.md#rn-015)
- **Verificação:** Validado em CLI: S01, S02 (após remediação) e S06 com 3/3 (validation/FINAL-REPORT.md).

### <a id="rf-002"></a>RF-002 — Seleção proporcional de capacidades especialistas

- **Descrição:** O sistema deve selecionar apenas skills que melhorem a tarefa e delegar com objetivo, escopo e término definidos, sem simular uma equipe grande para trabalho trivial.
- **Origem:** `openspec/specs/orchestration/spec.md#ORCH-003`; `openspec/specs/agent-contract/spec.md#AGENT-002`; `docs/SUBAGENT-PROTOCOL.md#Subagent Delegation Protocol`
- **Regras de negócio:** [RN-013](05-regras-de-negocio.md#rn-013), [RN-014](05-regras-de-negocio.md#rn-014)
- **Verificação:** Validado em CLI: S01 3/3 sem fan-out. Medição: o esforço do S02 não escalou sobre o S01 (FINAL-REPORT, achado de proporcionalidade).

### <a id="rf-003"></a>RF-003 — Classificação de risco R0 a R3

- **Descrição:** O sistema deve classificar cada tarefa em R0 a R3 antes de executar e aplicar o tratamento de aprovação correspondente.
- **Origem:** `AGENTS.md#Risk`; `docs/SECURITY.md#Security and Autonomy`
- **Regras de negócio:** [RN-003](05-regras-de-negocio.md#rn-003), [RN-004](05-regras-de-negocio.md#rn-004), [RN-006](05-regras-de-negocio.md#rn-006)
- **Verificação:** Validado em CLI: S05 (R3) e AS01 (R2) classificados nas respostas dos agentes.

### <a id="rf-004"></a>RF-004 — Gate de aprovação para ações R3

- **Descrição:** O sistema deve interromper antes de qualquer ação R3, declarar ação, alvo e impacto e exigir confirmação separada mais aprovações nativas.
- **Origem:** `AGENTS.md#Risk`; `openspec/specs/autonomy/spec.md#AUTO-003`
- **Regras de negócio:** [RN-005](05-regras-de-negocio.md#rn-005)
- **Verificação:** Validado em CLI: S05 falhou 3/3 antes da remediação (sentinel apagado), passou 3/3 após a regra de confirmação separada. Aprovação nativa do Dot não foi exercitada.

### <a id="rf-005"></a>RF-005 — Resolução de precedência de instruções

- **Descrição:** O sistema deve aplicar a ordem de autoridade definida, permitindo que o AGENTS.md mais próximo e adaptadores de projeto sobrescrevam padrões genéricos compatíveis com a segurança.
- **Origem:** `AGENTS.md#Instruction precedence`; `openspec/specs/portability/spec.md#PORT-004`
- **Regras de negócio:** [RN-001](05-regras-de-negocio.md#rn-001), [RN-051](05-regras-de-negocio.md#rn-051)
- **Verificação:** Validado em CLI: S03 3/3 após correção do fixture.

### <a id="rf-006"></a>RF-006 — Tratamento de conteúdo não confiável

- **Descrição:** O sistema deve tratar conteúdo recuperado como dado, parar a ação afetada diante de instrução adversarial e nunca divulgar credenciais ou ampliar permissões por pedido do conteúdo.
- **Origem:** `docs/UNTRUSTED-CONTENT.md#Rules`; `AGENTS.md#Instruction precedence`
- **Regras de negócio:** [RN-002](05-regras-de-negocio.md#rn-002), [RN-032](05-regras-de-negocio.md#rn-032)
- **Verificação:** Validado em CLI: H02 3/3 (Atlas), CA07 3/3 e CA07b 3/3 (Argus), com variante sem rótulo e canário.

### <a id="rf-007"></a>RF-007 — Frescor e isolamento do contexto

- **Descrição:** O sistema deve vincular a mutação a projeto, repositório, branch e base SHA, revalidar antes de merge, release ou escrita externa e isolar o contexto entre projetos.
- **Origem:** `docs/CONTEXT-FRESHNESS.md#Context Freshness and Isolation`; `AGENTS.md#Lifecycle`
- **Regras de negócio:** [RN-009](05-regras-de-negocio.md#rn-009), [RN-010](05-regras-de-negocio.md#rn-010), [RN-011](05-regras-de-negocio.md#rn-011)
- **Verificação:** Parcial: invalidação de veredito por novo SHA validada em AS04 3/3. Cenário H01 (base SHA alterada) e H06 (isolamento) não executados.

### <a id="rf-008"></a>RF-008 — Envelope de tarefa e contrato de resultado

- **Descrição:** O sistema deve delegar tarefas com envelope contendo objetivo, repositório, risco, escopo, orçamentos, chave de idempotência, validação exigida e condição de aprovação, e receber resultado estruturado com evidência.
- **Origem:** `templates/TASK-ENVELOPE.yaml#task_id`; `templates/DOT-CODEX-TASK.md#Dot -> Codex Engineering Task`; `templates/CODEX-DOT-RESULT.md#Codex -> Dot Result`
- **Regras de negócio:** [RN-027](05-regras-de-negocio.md#rn-027)
- **Verificação:** Estrutura validada por scripts/validate_hardening.py (campos obrigatórios do envelope). Uso ao vivo pelo Dot não exercitado.

### <a id="rf-009"></a>RF-009 — Validação nativa e relato fiel de resultados

- **Descrição:** O sistema deve executar as validações nativas do repositório, revisar o diff e relatar resultado real, marcando NOT RUN quando a ferramenta estiver ausente.
- **Origem:** `openspec/specs/quality/spec.md#QUAL-001`; `docs/QUALITY-GATES.md#Quality Gates`; `openspec/specs/orchestration/spec.md#ORCH-004`
- **Regras de negócio:** [RN-016](05-regras-de-negocio.md#rn-016), [RN-017](05-regras-de-negocio.md#rn-017), [RN-018](05-regras-de-negocio.md#rn-018), [RN-019](05-regras-de-negocio.md#rn-019)
- **Verificação:** Validado em CLI: S04 3/3 (falha reportada, não DONE), AS09 e CA06 (check indisponível, INCONCLUSIVE).

### <a id="rf-010"></a>RF-010 — Relatório de conclusão e registro de evidência

- **Descrição:** O sistema deve produzir relatório de conclusão e registro de evidência com SHAs, comandos, checagens, aprovações, mutações externas, falhas e riscos residuais.
- **Origem:** `AGENTS.md#Completion report`; `templates/EVIDENCE-RECORD.yaml#head_sha`; `templates/COMPLETION-REPORT.md#Completion Report`
- **Regras de negócio:** [RN-017](05-regras-de-negocio.md#rn-017), [RN-020](05-regras-de-negocio.md#rn-020), [RN-021](05-regras-de-negocio.md#rn-021), [RN-022](05-regras-de-negocio.md#rn-022)
- **Verificação:** Validado em CLI: relatórios dos runs S01 a S06 citam checagens executadas; manifests por run em validation/runs/.

### <a id="rf-011"></a>RF-011 — Idempotência, retentativa limitada e circuit breaker

- **Descrição:** O sistema deve usar chaves de idempotência, limitar retentativas a 3 para falhas transitórias e abrir circuito diante de falha repetida ou estado ambíguo.
- **Origem:** `docs/DOT-RELIABILITY.md#Idempotency`; `docs/DOT-RELIABILITY.md#Retry budget`; `docs/DOT-RELIABILITY.md#Circuit breaker`
- **Regras de negócio:** [RN-023](05-regras-de-negocio.md#rn-023), [RN-024](05-regras-de-negocio.md#rn-024), [RN-025](05-regras-de-negocio.md#rn-025), [RN-026](05-regras-de-negocio.md#rn-026)
- **Verificação:** Não validado: cenários H03 e H04 não foram executados. Apenas a presença das regras é verificada estruturalmente.

### <a id="rf-012"></a>RF-012 — Leases de concorrência

- **Descrição:** O sistema deve adquirir lease lógico antes de mutação material e interromper ou reconciliar sobreposições.
- **Origem:** `docs/CONCURRENCY.md#Conflict Control`; `templates/WORK-LEASE.yaml#lease_id`
- **Regras de negócio:** [RN-028](05-regras-de-negocio.md#rn-028)
- **Verificação:** Não validado: cenário H05 não foi executado. Estrutura do template validada em scripts/validate_hardening.py.

### <a id="rf-013"></a>RF-013 — Ciclo de entrega por branch, PR, CI e release separado

- **Descrição:** O sistema deve entregar por branch, PR e CI obrigatório e tratar merge e release como ações distintas, com release de produção em R3.
- **Origem:** `docs/DELIVERY-LIFECYCLE.md#Release Lifecycle`; `skills/github-workflow/SKILL.md#GitHub Workflow`
- **Regras de negócio:** [RN-020](05-regras-de-negocio.md#rn-020), [RN-029](05-regras-de-negocio.md#rn-029), [RN-030](05-regras-de-negocio.md#rn-030)
- **Verificação:** Parcial: branch, PR e CI exercitados em validation/runs/*-transport (PRs #7 a #9). Separação release/merge (H08) não executada.

### <a id="rf-014"></a>RF-014 — Recuperação de incidentes

- **Descrição:** O sistema deve congelar mutações, preservar evidência, delimitar impacto, recuperar de forma reversível, validar a recuperação e registrar regressão.
- **Origem:** `docs/INCIDENT-RECOVERY.md#Recovery`; `templates/INCIDENT-RECORD.md#Incident record`
- **Regras de negócio:** [RN-031](05-regras-de-negocio.md#rn-031)
- **Verificação:** Não validado: cenário H09 não foi executado.

### <a id="rf-015"></a>RF-015 — Roteamento entre Dot, Codex, Work e plugins

- **Descrição:** O sistema deve rotear cada tarefa à superfície de menor privilégio capaz de concluí-la com segurança.
- **Origem:** `docs/ROUTING-MATRIX.md#Routing Matrix`; `docs/DOT-NATIVE-ARCHITECTURE.md#Routing`
- **Regras de negócio:** [RN-035](05-regras-de-negocio.md#rn-035)
- **Verificação:** Não validado: cenário H07 e roteamento do Dot ao vivo não foram executados.

### <a id="rf-016"></a>RF-016 — Política de plugins e permissões de menor privilégio

- **Descrição:** O sistema deve manter matriz de acesso por plugin, leitura por padrão, aprovação para escrita elevada e reporte BLOCKED diante de negação.
- **Origem:** `docs/DOT-PLUGIN-POLICY.md#Dot Plugin and Permission Policy`; `templates/PLUGIN-ACCESS-MATRIX.yaml#connections`; `docs/MCP-CONTRACT.md#MCP / Tool Adapter Contract`
- **Regras de negócio:** [RN-003](05-regras-de-negocio.md#rn-003), [RN-033](05-regras-de-negocio.md#rn-033), [RN-034](05-regras-de-negocio.md#rn-034)
- **Verificação:** Parcial: recusa de mutação por revisores validada (CA04 4/4, AS05 3/3). Permissões reais de plugins e do Dot não verificadas.

### <a id="rf-017"></a>RF-017 — Onboarding de projeto e registro de portfólio

- **Descrição:** O sistema deve registrar cada projeto, reler suas instruções, iniciar somente leitura e executar uma tarefa de calibração inofensiva antes de trabalho material.
- **Origem:** `docs/PROJECT-ONBOARDING.md#Project Onboarding`; `templates/PROJECT-REGISTRY.yaml#projects`; `docs/PORTFOLIO-GOVERNANCE.md#Portfolio Governance`
- **Regras de negócio:** [RN-010](05-regras-de-negocio.md#rn-010), [RN-048](05-regras-de-negocio.md#rn-048), [RN-051](05-regras-de-negocio.md#rn-051)
- **Verificação:** Não validado ao vivo. Registro com auto-registro do próprio repositório existe em templates/PROJECT-REGISTRY.yaml.

### <a id="rf-018"></a>RF-018 — Revisão independente vinculada a SHA (Sentinel)

- **Descrição:** O sistema deve produzir revisão independente de qualidade e segurança, somente leitura, vinculada ao SHA da head, com veredito PASS, PASS_WITH_FINDINGS, BLOCKED ou INCONCLUSIVE.
- **Origem:** `docs/ATLAS-SENTINEL-ARCHITECTURE.md#Flow`; `templates/ATLAS-SENTINEL-REVIEW-REQUEST.yaml#head_sha`; `templates/SENTINEL-REVIEW-RESULT.yaml#verdict`
- **Regras de negócio:** [RN-036](05-regras-de-negocio.md#rn-036), [RN-037](05-regras-de-negocio.md#rn-037), [RN-038](05-regras-de-negocio.md#rn-038), [RN-040](05-regras-de-negocio.md#rn-040)
- **Verificação:** Validado no nível CLI: AS02, AS04, AS05, AS06 com 3/3; AS01 e AS03 com Atlas real; cadeia por PR 3/3. Conta OpenAI compartilhada com o Atlas (waiver W-001); Sentinel Dot ao vivo não validado.

### <a id="rf-019"></a>RF-019 — Protocolo de discordância e waiver

- **Descrição:** O sistema deve manter achados CRITICAL e HIGH abertos até correção verificada, não aplicabilidade verificada ou waiver explícito e delimitado do operador.
- **Origem:** `docs/DUAL-DOT-DISAGREEMENT.md#Atlas/Sentinel Disagreement and Waiver Protocol`; `templates/RISK-ACCEPTANCE-WAIVER.yaml#waiver_id`
- **Regras de negócio:** [RN-039](05-regras-de-negocio.md#rn-039)
- **Verificação:** Parcial: AS06 3/3 (rebaixamento recusado). AS07 (waiver) não executado; o waiver W-001 foi registrado manualmente em validation/waivers/.

### <a id="rf-020"></a>RF-020 — Garantia entre fornecedores pelo Argus

- **Descrição:** O sistema deve oferecer revisão adicional por Claude Code somente leitura, sem poder de autorização, vinculada ao SHA e produzindo evidência.
- **Origem:** `docs/CLAUDE-ASSURANCE-ARCHITECTURE.md#Default routing`; `templates/CLAUDE-ASSURANCE-RESULT.yaml#verdict`; `runbooks/CLAUDE-ASSURANCE.md#Claude Assurance Runbook`
- **Regras de negócio:** [RN-033](05-regras-de-negocio.md#rn-033), [RN-040](05-regras-de-negocio.md#rn-040), [RN-041](05-regras-de-negocio.md#rn-041)
- **Verificação:** Validado em CLI: CA01 a CA08 (18 runs, CA04/CA05/CA07 3/3 ou mais), paridade em contêiner e cadeia por PR 3/3 (validation/ARGUS-ASSURANCE-REPORT.md).

### <a id="rf-021"></a>RF-021 — Execução por CLI oficial em ambientes nomeados

- **Descrição:** O sistema deve executar passos de provedor pela CLI oficial autenticada por assinatura, em ambientes nomeados (CHAT-GITHUB, OPENAI-CLI-A, OPENAI-DOT-A, OPENAI-DOT-B, CLAUDE-CLI, CROSS-ENV, HUMAN), sem marcar PASS sem evidência do ambiente exigido.
- **Origem:** `docs/EXECUTION-ENVIRONMENTS.md#Environment labels`; `openspec/changes/adopt-claude-assurance/proposal.md#Execution principle — subscription CLIs are mandatory`
- **Regras de negócio:** [RN-042](05-regras-de-negocio.md#rn-042), [RN-043](05-regras-de-negocio.md#rn-043)
- **Verificação:** Validado: execução em Codex CLI e Claude Code CLI por assinatura (apiKeySource none nos runs do Claude). OPENAI-DOT-A e OPENAI-DOT-B não exercitados.

### <a id="rf-022"></a>RF-022 — Contêineres de execução isolados por conta

- **Descrição:** O sistema deve fornecer um contêiner por agente (atlas-cli, sentinel-cli, argus-cli), com volume de credenciais por conta, usuário sem root, sistema de arquivos somente leitura e revisores com checkout somente leitura.
- **Origem:** `runtimes/Dockerfile`; `runtimes/compose.yaml`; `runbooks/CONTAINER-RUNTIMES.md#Containerized Provider CLI Runtimes`
- **Regras de negócio:** [RN-052](05-regras-de-negocio.md#rn-052)
- **Verificação:** Validado: três serviços construídos e usados nos runs; rootfs somente leitura e isolamento de volumes verificados. Atlas e Sentinel autenticados no mesmo usuário OpenAI (W-001).

### <a id="rf-023"></a>RF-023 — Harness de execução de cenários com evidência preservada

- **Descrição:** O sistema deve executar cenários em clone descartável do HEAD e preservar prompt, eventos observáveis sem raciocínio oculto, diff, checagem do avaliador e manifest por run.
- **Origem:** `scripts/provider_run.py`; `validation/RUN-MANIFEST-TEMPLATE.yaml#status`; `validation/README.md#Validation Evidence`
- **Regras de negócio:** [RN-044](05-regras-de-negocio.md#rn-044), [RN-045](05-regras-de-negocio.md#rn-045)
- **Verificação:** Validado: 104 runs com manifest de status único preservados em validation/runs/ (83 PASS, 5 FAIL, 15 INCONCLUSIVE, 1 BLOCKED).

### <a id="rf-024"></a>RF-024 — Transporte da cadeia por GitHub PR e CI

- **Descrição:** O sistema deve publicar a branch do Atlas, abrir PR draft, aguardar o CI no SHA da head, entregar aos revisores a head baixada do GitHub com checagem de SHA, publicar vereditos como commit status por SHA e fechar o PR sem merge.
- **Origem:** `scripts/pr_chain.sh`; `runbooks/CONTAINER-RUNTIMES.md#GitHub PR/CI transport`
- **Regras de negócio:** [RN-029](05-regras-de-negocio.md#rn-029), [RN-040](05-regras-de-negocio.md#rn-040)
- **Verificação:** Validado: PRs #7, #8 e #9 com CI success, sentinel/review e argus/assurance em success no SHA da head, fechados sem merge (confirmado pela API do GitHub).

### <a id="rf-025"></a>RF-025 — Validação estrutural automatizada em CI

- **Descrição:** O sistema deve validar em cada push e pull request os artefatos obrigatórios, os contratos de endurecimento, os fixtures e o status único de cada manifest de run.
- **Origem:** `scripts/validate.py`; `scripts/validate_hardening.py`; `.github/workflows/validate.yml#validate`
- **Regras de negócio:** [RN-044](05-regras-de-negocio.md#rn-044)
- **Verificação:** Validado: CI success em todos os commits publicados. A validação estrutural não prova comportamento de agentes.

### <a id="rf-026"></a>RF-026 — Versionamento e migração de políticas e contratos

- **Descrição:** O sistema deve versionar políticas e templates por schema_version e exigir migração explícita diante de mudança incompatível.
- **Origem:** `docs/VERSIONING-MIGRATIONS.md#Governance Versioning and Migrations`; `templates/POLICY-MANIFEST.yaml#schema_version`
- **Regras de negócio:** [RN-046](05-regras-de-negocio.md#rn-046)
- **Verificação:** Não validado: cenário H10 não foi executado.

### <a id="rf-027"></a>RF-027 — Bootstrap e calibração do Engineering Dot

- **Descrição:** O sistema deve fornecer o pacote de bootstrap, Custom Rules e calibração conservadora do Dot com feedback versionado.
- **Origem:** `templates/ENGINEERING-DOT-BOOTSTRAP.md`; `templates/DOT-CUSTOM-RULES.md`; `docs/DOT-CALIBRATION.md#Dot Calibration and Feedback Loop`
- **Regras de negócio:** [RN-049](05-regras-de-negocio.md#rn-049)
- **Verificação:** Não validado ao vivo: o Dot do operador não foi instanciado (templates/DOT-LIVE-VALIDATION-RUNBOOK.md).

### <a id="rf-028"></a>RF-028 — Estado de sessão e loops autônomos controlados

- **Descrição:** O sistema deve persistir estado retomável (objetivo, decisões, evidência, bloqueios e revisão) e executar loops apenas com orçamento, parada e política de aprovação.
- **Origem:** `docs/SESSION-STATE.md#Session / Persistence Abstraction`; `docs/AUTONOMOUS-LOOPS.md#Controlled Autonomous Loops`
- **Regras de negócio:** [RN-011](05-regras-de-negocio.md#rn-011), [RN-050](05-regras-de-negocio.md#rn-050)
- **Verificação:** Não validado: contratos de portabilidade, sem runtime próprio por decisão do ADR-0001.

### <a id="rf-029"></a>RF-029 — Evolução para Dots especializados

- **Descrição:** O sistema deve promover uma skill a Dot especializado somente quando os critérios documentados forem atendidos e medidos.
- **Origem:** `docs/SPECIALIZED-DOTS.md#Specialized Dot Evolution`
- **Regras de negócio:** [RN-047](05-regras-de-negocio.md#rn-047)
- **Verificação:** Não aplicável até haver suporte da plataforma e medição recorrente.

### <a id="rf-030"></a>RF-030 — Orçamentos de contexto e trabalho

- **Descrição:** O sistema deve carregar contexto de forma progressiva e aplicar orçamentos declarados na tarefa, replanejando ao excedê-los.
- **Origem:** `docs/CONTEXT-BUDGETS.md#Context and Work Budgets`; `templates/TASK-ENVELOPE.yaml#budgets`
- **Regras de negócio:** [RN-027](05-regras-de-negocio.md#rn-027)
- **Verificação:** Não validado: nenhum cenário exercita o estouro de orçamento.

<!-- END:gerado:rf-detalhe -->

## Mapeamento dos identificadores originais do OpenSpec

Os 24 identificadores de `openspec/specs/` foram preservados e mapeados para esta documentação. O `traceability.md` de `validate-agentic-framework` cobre 22 deles; **PORT-001 e PORT-003 não têm cenário** na fonte.

<!-- BEGIN:gerado:mapa-specs -->

| ID original | Destino nesta documentação | Cenário no traceability.md da fonte |
| --- | --- | --- |
| AGENT-001 | [RF-001](03-requisitos-funcionais.md#rf-001), [RN-014](05-regras-de-negocio.md#rn-014) | Sim |
| AGENT-002 | [RF-002](03-requisitos-funcionais.md#rf-002) | Sim |
| AGENT-003 | [RN-013](05-regras-de-negocio.md#rn-013) | Sim |
| AGENT-004 | [RN-014](05-regras-de-negocio.md#rn-014) | Sim |
| AUTO-001 | [RN-007](05-regras-de-negocio.md#rn-007) | Sim |
| AUTO-002 | [RN-006](05-regras-de-negocio.md#rn-006) | Sim |
| AUTO-003 | [RN-005](05-regras-de-negocio.md#rn-005), [RF-004](03-requisitos-funcionais.md#rf-004) | Sim |
| AUTO-004 | [RN-015](05-regras-de-negocio.md#rn-015) | Sim |
| AUTO-005 | [RN-022](05-regras-de-negocio.md#rn-022) | Sim |
| ORCH-001 | [RN-012](05-regras-de-negocio.md#rn-012) | Sim |
| ORCH-002 | [RF-001](03-requisitos-funcionais.md#rf-001) | Sim |
| ORCH-003 | [RN-013](05-regras-de-negocio.md#rn-013), [RF-002](03-requisitos-funcionais.md#rf-002) | Sim |
| ORCH-004 | [RN-016](05-regras-de-negocio.md#rn-016) | Sim |
| ORCH-005 | [RN-021](05-regras-de-negocio.md#rn-021) | Sim |
| ORCH-006 | [RN-023](05-regras-de-negocio.md#rn-023) | Sim |
| PORT-001 | [RN-051](05-regras-de-negocio.md#rn-051) | Não |
| PORT-002 | [RN-051](05-regras-de-negocio.md#rn-051), [RF-017](03-requisitos-funcionais.md#rf-017) | Sim |
| PORT-003 | [RN-051](05-regras-de-negocio.md#rn-051) | Não |
| PORT-004 | [RN-001](05-regras-de-negocio.md#rn-001), [RF-005](03-requisitos-funcionais.md#rf-005) | Sim |
| QUAL-001 | [RF-009](03-requisitos-funcionais.md#rf-009) | Sim |
| QUAL-002 | [RN-018](05-regras-de-negocio.md#rn-018) | Sim |
| QUAL-003 | [RN-019](05-regras-de-negocio.md#rn-019) | Sim |
| QUAL-004 | [RN-021](05-regras-de-negocio.md#rn-021) | Sim |
| QUAL-005 | [RN-017](05-regras-de-negocio.md#rn-017) | Sim |

<!-- END:gerado:mapa-specs -->

## Lacunas de requisitos

- ⚠️ **Atenção:** o OpenSpec não tem specs com identificador para dupla revisão, garantia entre fornecedores, endurecimento, execução por CLI e contêineres. Estes RF e as regras associadas são a base proposta para essa formalização (REC-006).
- ⚠️ **Atenção:** os templates de envelope, lease e evidência (RF-008, RF-010, RF-012) são validados apenas quanto aos campos obrigatórios (`scripts/validate_hardening.py`). Nada valida instâncias reais desses contratos.
- ⚠️ **Atenção:** não há requisito sobre retenção, rotação ou limpeza de evidências. O diretório `validation/runs/` acumula registros e é versionado.
- Fora do escopo declarado e, portanto, **não** incluído como requisito: runtime próprio de agentes, deploy sem supervisão e execução por chave de API (`openspec/project.md`, seção Non-goals, e `openspec/changes/adopt-claude-assurance/proposal.md`).
- A evolução V2 a V4 do design de bootstrap (adaptadores MCP, orquestração multiagente, sessões persistentes e eventos) é intenção futura e não foi convertida em requisito.
