---
titulo: "Contexto, justificativa e glossário"
projeto: "ai-engineering-team"
autor: "Não informado"
data: "2026-10-01"
versao: "1.0.0"
classificacao: "Não informada"
status: "Rascunho para revisão"
---

# Contexto, justificativa e glossário

Navegação: [Índice](00-toc.md) · próximo: [02 Visão geral](02-visao-geral.md)

## Sumário executivo

O **ai-engineering-team** é o sistema operacional de engenharia e a fonte de bootstrap de um Engineering Dot da OpenAI. Reúne, em arquivos versionados, a política que governa como agentes de IA conduzem trabalho de engenharia: precedência de instruções, classes de risco, gates de qualidade, controles de confiabilidade, revisão independente entre fornecedores e contratos de evidência. Não é um runtime de agentes: o Dot coordena, o Codex executa o trabalho em repositórios e este repositório fornece a política, as skills, os contratos e a validação.

Esta análise percorreu o repositório (157 arquivos versionados fora de `validation/runs/` no início da análise; a cobertura por área e as exclusões estão em [00-toc.md](00-toc.md)), extraiu as regras de negócio com origem verificável e produziu a documentação em `docs/`. Principais achados:

- ✅ **Confirmado:** a política cobre risco, frescor, isolamento, idempotência, retentativa, circuit breaker, leases, entrega, recuperação, roteamento, revisão independente e execução por CLI. Cada regra tem origem em arquivo e seção.
- ✅ **Confirmado:** a camada de CLI foi validada por execução: Atlas (S01 a S06 e H02), Sentinel (AS02, AS04, AS05, AS06, AS08, AS09, AS10), Argus (CA01 a CA08) e a cadeia por GitHub PR e CI. Falhas reais foram preservadas e remediadas (S05 e S02).
- ⚠️ **Atenção:** a camada de Dots ao vivo, a aprovação nativa, a concorrência de leases e os cenários H01, H03 a H10 e AS07 **não foram validados**. Atlas e Sentinel compartilham um usuário OpenAI sob o waiver W-001, o que não comprova independência entre contas.
- ⚠️ **Atenção:** existem divergências entre documentos de origem (três variantes de ciclo de vida, cinco vocabulários de status, precedência do manifest) e requisitos sem especificação formal no OpenSpec.
- 🔄 **Alterado:** foram aplicadas as recomendações que dependiam só de documentação descritiva; as que alterariam artefatos normativos ficaram pendentes, com motivo, decisão necessária e próximo passo.

<!-- BEGIN:gerado:resumo-numeros -->

### Números da análise

| Elemento | Quantidade |
| --- | --- |
| Regras de negócio (RN) | 52 |
| Requisitos funcionais (RF) | 30 |
| Requisitos não funcionais (RNF) | 12 |
| Casos de uso (UC) | 20 |
| Critérios de aceitação (CA) | 32 |
| Recomendações aplicadas | 10 |
| Recomendações pendentes | 14 |
| RF validados por execução | 15 |
| RF parcialmente validados | 4 |
| RF não validados ou apenas estruturais | 11 |

<!-- END:gerado:resumo-numeros -->

## Contexto e justificativa

### Problema

Segundo a proposta de bootstrap, o Codex executa trabalho de engenharia, mas prompts avulsos e repetidos produzem planejamento, testes, revisão e comportamento arquitetural inconsistentes entre repositórios. A proposta aponta quatro riscos: decomposição excessiva de papéis desperdiça contexto, regras genéricas podem conflitar com convenções locais, autonomia falsa incentiva escritas e deploys inseguros, e instruções grandes diluem restrições importantes.

### Necessidade atendida

- Reutilização entre repositórios e pilhas tecnológicas, com menos repetição de prompts.
- Autonomia progressiva (consultiva, implementação, validação, entrega), com portões humanos para ações irreversíveis.
- Conclusão baseada em evidência, e não em confiança.
- Governança que não enfraquece as salvaguardas nativas da plataforma e dos provedores.

### Evolução do escopo

A evolução está registrada em `openspec/roadmap.md` e nas seis mudanças de `openspec/changes/`:

| Marco | Resumo | Situação declarada na fonte |
| --- | --- | --- |
| M0 a M2 | Baseline do OpenSpec, núcleo Codex, pacotes de stack | Implementado |
| M3 | Alinhamento ao Dot: Dot coordena, Codex executa | Implementado como baseline |
| M4 | Endurecimento de produção | Implementado estruturalmente; validação ao vivo pendente |
| M5 a M8 | Validação comportamental, portfólio, Dots especializados, operação contínua | Sem situação declarada na fonte |
| M9 | Atlas e Sentinel com garantia independente | Modelo estrutural implementado; validação ao vivo pendente |
| M10 | Aplicação dos ambientes de execução | Definido; nota de 2026-10-01 no roadmap registra evidência parcial |

Capacidades sem marco próprio no roadmap: garantia entre fornecedores (Argus), execução por CLI em contêineres isolados por conta e transporte por GitHub PR e CI. Estão documentadas em `docs/CLAUDE-ASSURANCE-ARCHITECTURE.md`, `runbooks/CONTAINER-RUNTIMES.md` e `scripts/pr_chain.sh`.

### Princípios

A decisão central, registrada no ADR-0001, é **não construir um runtime concorrente**: persistência, agendamento e capacidades de nuvem do Dot são nativos; o repositório define apenas contratos portáveis de governança, auditoria e fallback. O princípio de execução, decidido na mudança de garantia entre fornecedores, é usar sempre a CLI oficial de cada provedor com a assinatura já configurada do operador, sem chave de API.

## Glossário e siglas

### Termos

| Termo | Definição | Fonte |
| --- | --- | --- |
| Achado (finding) | Defeito ou risco apontado por um revisor, com reivindicação, severidade, revisão afetada, evidência, propriedade esperada e orientação de correção | `docs/DUAL-DOT-DISAGREEMENT.md` |
| AGENTS.md | Arquivo de instruções para agentes; o mais próximo do arquivo alterado prevalece sobre o do diretório pai | `AGENTS.md` |
| Argus | Agente de garantia entre fornecedores, executado pelo Claude Code com a assinatura Claude do operador; revisor independente somente leitura | `docs/EXECUTION-ENVIRONMENTS.md` |
| Assurance (garantia) | Revisão adicional independente de um terceiro fornecedor, que produz evidência e não autoridade | `docs/CLAUDE-ASSURANCE-ARCHITECTURE.md` |
| Atlas | Engineering Dot primário, líder de engenharia, na conta OpenAI primária | `docs/ATLAS-SENTINEL-ARCHITECTURE.md` |
| Base SHA | Revisão do branch alvo à qual a tarefa foi vinculada; se mudar, as premissas são invalidadas | `docs/CONTEXT-FRESHNESS.md` |
| Circuit breaker | Mecanismo que interrompe a mutação após falha repetida ou estado ambíguo | `docs/DOT-RELIABILITY.md` |
| ChatGPT Work | Superfície para pesquisa profunda e artefatos não de código | `docs/ROUTING-MATRIX.md` |
| Codex | Executor padrão de engenharia em repositórios: código, testes, comandos e revisão | `README.md` |
| Contêiner de execução | Serviço Docker por agente (atlas-cli, sentinel-cli, argus-cli), com volume de credenciais por conta | `runbooks/CONTAINER-RUNTIMES.md` |
| Custom Rules | Regras do Dot configuradas a partir do template do repositório; não guardam segredos nem fatos mutáveis | `templates/DOT-CUSTOM-RULES.md` |
| Definição de pronto | Condições para declarar DONE: implementação completa, validação executada, diff revisado, evidência e riscos reportados | `AGENTS.md` |
| Engineering Dot | Coordenador persistente, nativo da plataforma, que roteia trabalho e aplica a governança | `docs/DOT-NATIVE-ARCHITECTURE.md` |
| Envelope de tarefa | Contrato estruturado de delegação, com objetivo, repositório, risco, escopo, orçamentos, chave de idempotência e validação exigida | `templates/TASK-ENVELOPE.yaml` |
| Evidência | Registro observável (SHA, comandos, checagens, aprovações, falhas) de uma execução; nunca inclui raciocínio oculto | `docs/DOT-RELIABILITY.md` |
| Fixture | Material determinístico de teste usado para exercitar um cenário | `validation/fixtures/README.md` |
| Frescor | Propriedade de o contexto refletir o estado atual da fonte, garantida por releitura antes de mutar | `docs/CONTEXT-FRESHNESS.md` |
| Gate | Ponto de controle de qualidade ou aprovação; gate ausente nunca equivale a gate aprovado | `docs/QUALITY-GATES.md` |
| Harness | Script que executa um cenário em clone descartável e preserva a evidência | `scripts/provider_run.py` |
| Head SHA | Revisão da ponta do branch ou PR sob revisão, à qual o veredito fica preso | `docs/CLAUDE-ASSURANCE-ARCHITECTURE.md` |
| Idempotência | Propriedade de repetir uma operação sem duplicar o efeito; exige task_id e idempotency_key | `docs/DOT-RELIABILITY.md` |
| Lease | Reserva lógica e consultiva de uma superfície de mudança para uma tarefa | `docs/CONCURRENCY.md` |
| Manifest de run | Arquivo YAML que registra cenário, ambiente, agente, SHAs, checagens, aprovação, evidências e status de um run | `validation/RUN-MANIFEST-TEMPLATE.yaml` |
| OpenSpec | Diretório fonte da verdade das mudanças planejadas, com proposta, design, tarefas e specs | `openspec/README.md` |
| Orçamento | Limite declarado de arquivos, escritas externas, retentativas ou tempo | `docs/CONTEXT-BUDGETS.md` |
| Plugin | Conexão estreita a sistema externo, sob as permissões nativas do provedor | `docs/DOT-PLUGIN-POLICY.md` |
| Portfólio | Conjunto de projetos coordenados pelo Dot por meio de um registro versionado | `docs/PORTFOLIO-GOVERNANCE.md` |
| Precedência | Ordem de autoridade entre fontes de instrução | `AGENTS.md` |
| Registro de projetos | Índice versionado de projetos; nunca substitui a releitura do repositório | `templates/PROJECT-REGISTRY.yaml` |
| Revisão independente | Revisão por agente distinto de quem implementou, somente leitura por padrão | `docs/ATLAS-SENTINEL-ARCHITECTURE.md` |
| Run | Uma execução de cenário, com diretório próprio em `validation/runs/` | `validation/README.md` |
| Sentinel | Engineering Dot de qualidade e segurança, na conta OpenAI secundária; revisor independente | `docs/ATLAS-SENTINEL-ARCHITECTURE.md` |
| Severidade | Classificação de achado em CRITICAL, HIGH, MEDIUM, LOW ou INFO | `docs/DUAL-DOT-AUTHORITY.md` |
| Skill | Procedimento especializado e carregado sob demanda; papel de especialista | `skills/tech-lead/SKILL.md` |
| Tech Lead | Papel de orquestração que responde do requisito à evidência | `skills/tech-lead/SKILL.md` |
| Transporte | Meio pelo qual a cadeia de revisão troca artefatos; aqui, GitHub, OpenSpec e evidência | `docs/CLAUDE-ASSURANCE-ARCHITECTURE.md` |
| Veredito | Resultado de uma revisão: PASS, PASS_WITH_FINDINGS, BLOCKED ou INCONCLUSIVE, preso a um SHA | `templates/SENTINEL-REVIEW-RESULT.yaml` |
| Waiver | Aceitação explícita de risco pelo operador, delimitada por achado, revisão, escopo, expiração e controles | `templates/RISK-ACCEPTANCE-WAIVER.yaml` |
| W-001 | Waiver que autoriza, até 2026-10-31, o uso do mesmo usuário OpenAI para Atlas e Sentinel nas execuções por CLI | `validation/waivers/W-001-shared-openai-account.yaml` |

### Ambientes de execução

| Rótulo | Significado | Fonte |
| --- | --- | --- |
| CHAT-GITHUB | Ambiente de chat com GitHub conectado: prepara e inspeciona artefatos do repositório | `docs/EXECUTION-ENVIRONMENTS.md` |
| OPENAI-CLI-A | CLI Codex com a conta OpenAI primária (Atlas) | `docs/EXECUTION-ENVIRONMENTS.md` |
| OPENAI-CLI-B | CLI Codex com a conta OpenAI secundária (Sentinel), plano de execução de repositório | `docs/EXECUTION-ENVIRONMENTS.md` |
| OPENAI-DOT-A | Dot Atlas ao vivo | `docs/EXECUTION-ENVIRONMENTS.md` |
| OPENAI-DOT-B | Dot Sentinel ao vivo | `docs/EXECUTION-ENVIRONMENTS.md` |
| CLAUDE-CLI | Claude Code CLI com a assinatura Claude (Argus) | `docs/EXECUTION-ENVIRONMENTS.md` |
| CROSS-ENV | Cenário que exige evidência de dois ou mais ambientes | `docs/EXECUTION-ENVIRONMENTS.md` |
| HUMAN | Ação explícita e indelegável do operador | `docs/EXECUTION-ENVIRONMENTS.md` |

### Siglas

| Sigla | Significado |
| --- | --- |
| ADR | Architecture Decision Record, registro de decisão de arquitetura |
| API | Application Programming Interface |
| CA | Critério de aceitação (identificador desta documentação) |
| CI | Integração contínua |
| CLI | Interface de linha de comando |
| IAM | Gerenciamento de identidade e acesso |
| MCP | Model Context Protocol; `docs/MCP-CONTRACT.md` o trata como contrato de adaptadores de ferramentas |
| PR | Pull request |
| R0 a R3 | Classes de risco: R0 somente leitura, R1 local reversível, R2 sensível, R3 produção ou irreversível |
| REC | Recomendação (identificador desta documentação) |
| RF | Requisito funcional |
| RN | Regra de negócio |
| RNF | Requisito não funcional |
| SHA | Identificador de revisão do Git |
| SLO | Objetivo de nível de serviço, citado na skill de observabilidade |
| UC | Caso de uso |

## Vocabulários de status

O repositório usa vocabulários de status distintos para objetos diferentes. Eles **não são sinônimos**: confundi-los é uma forma de falsa conclusão.

| Vocabulário | Valores | Aplica-se a | Fonte |
| --- | --- | --- | --- |
| Status de mudança | PLANNED, IN_PROGRESS, BLOCKED, VALIDATED, DONE | Mudanças do OpenSpec | `openspec/README.md` |
| Status de run | PASS, FAIL, BLOCKED, INCONCLUSIVE | Cada execução de cenário | `validation/README.md` |
| Veredito de revisão | PASS, PASS_WITH_FINDINGS, BLOCKED, INCONCLUSIVE | Resultados do Sentinel e do Argus | `templates/SENTINEL-REVIEW-RESULT.yaml` |
| Resultado de tarefa Codex | DONE, FAILED, BLOCKED, INCONCLUSIVE | Retorno do Codex ao Dot | `templates/CODEX-DOT-RESULT.md` |
| Estado de gate | NOT RUN (e os demais resultados do gate) | Checagem não executada | `docs/QUALITY-GATES.md` |
| Resposta a achado | FIXED, DISPUTED, ACCEPTED_RISK, NOT_APPLICABLE | Resposta do Atlas a um achado | `docs/DUAL-DOT-DISAGREEMENT.md` |
| Status de commit no GitHub | success, failure, pending, error | Gates publicados no PR | `docs/anexos/swagger/github-commit-status.yaml` |

Correspondência adotada por `scripts/pr_chain.sh` na publicação dos vereditos: PASS e PASS_WITH_FINDINGS resultam em success; BLOCKED, em failure; INCONCLUSIVE ou ausência de veredito, em pending; divergência de SHA, em error.

Significados que a fonte permite distinguir:

- **BLOCKED:** o passo não pode prosseguir por falta de autorização, credencial, contexto ou capacidade.
- **INCONCLUSIVE:** o critério não pôde ser provado no ambiente disponível.
- **NOT RUN:** a ferramenta de validação não foi executada, com o motivo registrado; não conta como aprovada.
- **DONE:** a definição de pronto foi atendida (implementação, validação executada, diff revisado, evidência e riscos reportados). Não implica VALIDATED nem deploy.

⚠️ **Atenção:** as fontes não definem formalmente os valores de status de lease além de `active`, nem a equivalência entre DONE, VALIDATED e PASS. Ver REC-002 em [08-observacoes-analises.md](08-observacoes-analises.md).
