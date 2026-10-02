---
titulo: "Requisitos não funcionais"
projeto: "ai-engineering-team"
autor: "Não informado"
data: "2026-10-01"
versao: "1.0.0"
classificacao: "Não informada"
status: "Rascunho para revisão"
---

# Requisitos não funcionais

Navegação: [Índice](00-toc.md) · anterior: [03 Requisitos funcionais](03-requisitos-funcionais.md) · próximo: [05 Regras de negócio](05-regras-de-negocio.md)

## Como ler

Cada requisito não funcional (RNF) tem um **status**:

- **Confirmado:** a fonte define o requisito ou o valor.
- **Lacuna:** a fonte não define meta nem critério verificável. O que existe é o valor **observado** nas execuções, registrado como fato, e uma **proposta** claramente marcada como sujeita à validação.

Nenhuma meta numérica foi inventada. As propostas abaixo não são requisitos até que sejam aprovadas (REC-013).

<!-- BEGIN:gerado:rnf-tabela -->

| ID | Categoria | Requisito | Status | Meta, valor observado ou lacuna | Origem |
| --- | --- | --- | --- | --- | --- |
| RNF-001 | Segurança | **Menor privilégio e proteção de credenciais.** Acessos são mínimos e escopados, segredos nunca ficam no repositório, em prompts ou em evidências, e credenciais de provedor ficam apenas em volumes por conta. | Confirmado | Qualitativa. Varredura de tokens executada antes de cada commit de evidência; sem achados. | `docs/SECURITY.md#Security and Autonomy`<br>`runbooks/CONTAINER-RUNTIMES.md#Sign in`<br>`docs/DOT-PLUGIN-POLICY.md#Dot Plugin and Permission Policy` |
| RNF-002 | Confiabilidade | **Execução repetível e tolerante a falha.** Mutações externas são idempotentes, retentativas são limitadas e falha repetida interrompe a automação. | Confirmado | Valores definidos na especificação: 3 tentativas e 3 falhas para abrir o circuito. | `docs/DOT-RELIABILITY.md#Retry budget`<br>`docs/DOT-RELIABILITY.md#Circuit breaker` |
| RNF-003 | Observabilidade e auditabilidade | **Evidência observável e rastreável.** Toda execução relevante gera registro com SHA, comandos, resultados, aprovações e falhas, e vereditos de revisão são publicados por SHA. | Confirmado | Qualitativa. Cada run possui manifest com status PASS, FAIL, BLOCKED ou INCONCLUSIVE. | `docs/DOT-RELIABILITY.md#Idempotency`<br>`templates/EVIDENCE-RECORD.yaml#status`<br>`scripts/provider_run.py`<br>`scripts/pr_chain.sh` |
| RNF-004 | Compatibilidade e portabilidade | **Independência de pilha tecnológica e de runtime.** O núcleo é agnóstico de tecnologia, adaptadores locais cobrem pilhas específicas e cada projeto declara a faixa de governança compatível. | Confirmado | Faixa compatível do template: >=1.0.0 <2.0.0. CLIs fixadas na imagem: Codex 0.159.3 e Claude Code 2.1.287. | `openspec/specs/portability/spec.md#PORT-001`<br>`templates/PROJECT-REGISTRY.yaml#compatible_governance` |
| RNF-005 | Manutenibilidade | **Instruções enxutas e validação estrutural contínua.** O AGENTS.md é conciso, detalhes ficam em skills e specs com divulgação progressiva, e um validador executável roda em CI. | Confirmado | Qualitativa. O validador cobre artefatos obrigatórios, fixtures e status dos runs. | `openspec/project.md#Architecture principles`<br>`scripts/validate.py`<br>`.github/workflows/validate.yml#validate` |
| RNF-006 | Reprodutibilidade | **Validações reprodutíveis.** Cada cenário roda em clone descartável de um SHA fixado, em contêiner com versões fixas, com prompt e evidência preservados. | Confirmado | Qualitativa. A variabilidade do modelo é tratada com repetição 3x (RN-044), não eliminada. | `scripts/provider_run.py`<br>`runtimes/Dockerfile`<br>`openspec/changes/validate-agentic-framework/design.md#Principles` |
| RNF-007 | Custo | **Sem dependência de cobrança por API na V1.** A V1 não depende de chave de API; a execução usa CLIs por assinatura. | Confirmado | Qualitativa. Orçamentos de uso do Codex e do Work permanecem observáveis separadamente (docs/ROUTING-MATRIX.md). | `openspec/project.md#Goals`<br>`openspec/changes/adopt-claude-assurance/proposal.md#Execution principle — subscription CLIs are mandatory` |
| RNF-008 | Desempenho | **Esforço proporcional à complexidade.** A eficiência é definida como esforço proporcional com evidência adequada, e não como mínimo de atividade. | Lacuna | Sem meta numérica definida. Observado: revisões por CLI levaram 27 a 62 s (Sentinel, Argus); tarefas do Atlas, mediana de 20 a 144 s. PROPOSTA sujeita à validação: acordar limites de duração por classe de tarefa a partir de mais medições. | `openspec/changes/validate-agentic-framework/benchmark.md#Interpretation`<br>`docs/CONTEXT-BUDGETS.md#Context and Work Budgets` |
| RNF-009 | Disponibilidade | **Disponibilidade dos agentes e provedores.** Não há requisito de disponibilidade definido; o sistema depende das CLIs e APIs dos provedores e do GitHub, e a indisponibilidade resulta em BLOCKED ou INCONCLUSIVE. | Lacuna | Sem meta definida. Evento observado: indisponibilidade de rede do host interrompeu push e conferências da sessão por um período. PROPOSTA sujeita à validação: definir se algum SLO se aplica, dado que o framework é declarativo. | `docs/EXECUTION-ENVIRONMENTS.md#Hard rule` |
| RNF-010 | Escalabilidade | **Múltiplos projetos e revisões simultâneas.** O protocolo é reutilizável por vários projetos, revisões indexadas por projeto e SHA, e Dots especializados podem ser adicionados atrás dos mesmos contratos. | Lacuna | Sem limite definido de projetos ou execuções concorrentes. Observado: até 6 contêineres simultâneos no host de validação; nenhuma falha foi atribuída à concorrência, mas a degradação não foi medida. | `docs/ATLAS-SENTINEL-ARCHITECTURE.md#Scaling`<br>`docs/PORTFOLIO-GOVERNANCE.md#Portfolio Governance` |
| RNF-011 | Usabilidade | **Instrução curta do operador e relatórios claros.** O operador deve conseguir emitir um objetivo conciso e receber mudança planejada, implementada, testada e revisada com riscos residuais explícitos. | Lacuna | Sem métrica definida (por exemplo, taxa de retrabalho). docs/DOT-CALIBRATION.md sugere acompanhar falsa conclusão, aprovações desnecessárias e retrabalho, mas não fixa metas. | `openspec/project.md#Success criteria` |
| RNF-012 | Segurança e confiabilidade comportamental | **Tolerância zero a efeito R3 não autorizado e a falso PASS.** Nenhum efeito colateral R3 sem autorização e nenhum PASS em validação falha ou não executada é tolerado; qualquer ocorrência bloqueia DONE até remediação e novo teste. | Confirmado | Limite definido na fonte: 0 ocorrências. Observado: S05 falhou 3 de 3 antes da remediação e passou 3 de 3 depois; nenhum falso PASS em S04 (3 de 3). | `openspec/changes/validate-agentic-framework/benchmark.md#Thresholds`<br>`openspec/changes/validate-agentic-framework/design.md#Safety-critical` |

<!-- END:gerado:rnf-tabela -->

## Propostas sujeitas à validação

As propostas dependem de decisão do operador e de mais medições. O volume observado é pequeno e não sustenta metas estatísticas.

| Requisito | Proposta | Base observada | Pendente |
| --- | --- | --- | --- |
| RNF-008 Desempenho | Definir limite de duração por classe de tarefa e por revisão independente, com percentil e tamanho mínimo de amostra | Revisões do Sentinel e do Argus levaram de 27 a 62 s nos runs de validação; tarefas do Atlas tiveram mediana por cenário de 20 a 144 s | Amostra maior e escolha do percentil |
| RNF-009 Disponibilidade | Decidir se algum objetivo de nível de serviço se aplica a um framework declarativo; manter BLOCKED ou INCONCLUSIVE como resposta à indisponibilidade de provedores | Uma interrupção de rede do host impediu push e consultas ao GitHub durante parte da sessão de validação | Decisão do operador |
| RNF-010 Escalabilidade | Definir o teto de contêineres e de revisões simultâneas depois de medir a latência sob carga crescente | Até 6 contêineres simultâneos foram usados, sem falha atribuída à concorrência; degradação não medida | Teste de carga controlado |
| RNF-011 Usabilidade | Adotar os indicadores já sugeridos em `docs/DOT-CALIBRATION.md` (falsa conclusão, aprovações desnecessárias e ausentes, incidentes de contexto obsoleto, retentativas e circuit breaker, retrabalho, falhas de CI após mudança de agente, fan-out desnecessário) com metas a definir | Falsa conclusão: nenhuma em S04 (3 de 3) | Metas e coleta contínua |

## Cobertura das categorias

| Categoria pedida | Situação | RNF |
| --- | --- | --- |
| Segurança | Confirmado | RNF-001, RNF-012 |
| Desempenho | Lacuna | RNF-008 |
| Disponibilidade | Lacuna | RNF-009 |
| Escalabilidade | Lacuna | RNF-010 |
| Usabilidade | Lacuna | RNF-011 |
| Manutenibilidade | Confirmado | RNF-005 |
| Observabilidade | Confirmado | RNF-003 |
| Compatibilidade | Confirmado | RNF-004 |
| Confiabilidade | Confirmado | RNF-002, RNF-006, RNF-012 |
| Custo (adicional) | Confirmado | RNF-007 |

⚠️ **Atenção:** os RNF de desempenho, disponibilidade, escalabilidade e usabilidade permanecem sem critério numérico verificável. Isso é uma lacuna da especificação, não uma omissão desta documentação.
