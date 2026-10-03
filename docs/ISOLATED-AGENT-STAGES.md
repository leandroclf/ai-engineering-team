# Três agentes, quatro etapas isoladas

Contrato do CLI local 0.2.0. Substitui a distribuição local anterior, sem reescrever a evidência histórica do harness ou instanciar Dots. Sem gateway, roteador aprendido, banco ou novo serviço.

| Etapa | Agente | CLI | Modelo padrão | Esforço |
| --- | --- | --- | --- | --- |
| plan | Atlas | Codex | `gpt-6-astra` | `xhigh` |
| implement | Argus | Claude Code | `claude-opus-5-5` | `high` |
| validate | Sentinel | Codex | `gpt-6-astra` | `xhigh` |
| review | Atlas em nova sessão | Claude Code | `claude-opus-5-5` | `high` |

Escolhas baseadas nos guias oficiais de 2026-10-03: Astra para raciocínio exigente e Opus 5.5 para programação com agentes. Não são superioridade comprovada no projeto. Acesso depende da conta/cliente/políticas nativas. `init` permite IDs explícitos do mesmo provedor e esforços suportados usando `--plan-model`, `--implement-model`, `--validate-model`, `--review-model` e os respectivos `--*-effort`. Não há troca automática se um modelo falhar.

## Isolamento

Cada chamada tem container, sessão, staging e handoff próprios. Volumes: `ai-team-atlas-plan-home`, `ai-team-argus-implement-home`, `ai-team-sentinel-validate-home`, `ai-team-atlas-review-home`. Codex é ephemeral; Claude não persiste sessão, usa modo restrito, hooks desabilitados e MCP vazio. Não há resume/continue de conversas. Volumes separados não provam identidades distintas.

Atlas planeja com checkout somente leitura: objetivo, escopo, premissas, risco, tarefas, critérios e validação. O host valida JSON, SHA e cobertura; calcula identidade SHA256 e escreve `openspec/changes/ai-team-<task>/<cycle>/`, com commit anterior à implementação. Plano R3 ou BLOCKED impede execução. O plano canônico fica fora do checkout e é montado somente leitura.

Argus implementa com Read/Grep/Glob/Edit/Write; Bash, Agent e MCP são removidos. Apenas implementação recebe checkout gravável; Git metadata permanece somente leitura para todos. O host executa checks offline sem contas. Argus devolve COMPLETE, BLOCKED ou REPLAN_REQUIRED; COMPLETE não substitui verificação.

Sentinel valida pedido/aceite/evidências. Atlas/Claude revisa correção, segurança, manutenção e regressões em nova sessão. Ambos recebem pedido original, plano, código e checks; o revisor não recebe o parecer nem a conversa do validador. Os dois resultados exigem HEAD, plano e evidência para cada critério, além de qualidade/segurança obrigatórias. JSON válido não prova veracidade.

Falhas verificáveis retornam ao Argus; plano inadequado retorna ao Atlas/OpenAI. Replanejamento consome o mesmo limite de ciclos/prazo. Erro de provedor, saída inválida ou estado incerto bloqueiam. Não há publicação, merge ou deploy automático.

## Evidência, atualização e retomada

state.json registra etapa, agente, provedor, modelo solicitado, esforço e plano. `resolved_model: null` significa modelo efetivo não confirmado, sem inferência. Artefatos por ciclo: plan, implement, tests, validate e review. Entrega revalida os dois pareceres e checks no HEAD atual.

Config/tarefas usam versão 2. Repita `init --upgrade` com imagem/checks explícitos para atualizar configuração; preserva backup privado. Não migra tarefas: versões antigas não retomam nem entregam sob contrato novo. Retomada mantém plano/modelos/prazo; estágio interrompido ou staging parcial não é repetido automaticamente.

## Aceitação operacional

Testes controlados comprovam contratos, ordem, falhas e comandos, não acesso aos modelos ou ferramentas reais. Rebuild, quatro logins, doctor e tarefa pequena no Linux do operador com diff inspecionado são necessários. Sandbox Codex depende do kernel/cliente; não contornar incompatibilidade com bypass. O isolamento não é DLP completo nem garantia de independência cognitiva.

Fontes: [modelos OpenAI](https://learn.chatgpt.com/docs/models), [raciocínio/configuração](https://learn.chatgpt.com/docs/config-file/config-reference), [modelos Claude](https://platform.claude.com/docs/en/models/overview), [CLI Claude](https://code.claude.com/docs/en/cli-reference). [OpenSpec e aceitação](../openspec/changes/isolated-agent-stages/tasks.md).
