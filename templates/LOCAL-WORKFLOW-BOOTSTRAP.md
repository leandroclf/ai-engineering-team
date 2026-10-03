# Bootstrap local Linux

Checklist do operador para o fluxo `ai-team`; não é um prompt de configuração de Dot. Consulte o [guia completo](../docs/LOCAL-LINUX-WORKFLOW.md).

1. Instale Git, Python 3.10+ com venv/ensurepip e Docker Engine usando a distribuição Linux. Confirme acesso ao daemon com seu usuário. Configure Git/gh no host apenas para entrega ao GitHub.
2. Clone a main do framework em um local permanente. Execute `bash scripts/install-local.sh --check` e, após corrigir pré-requisitos, `bash scripts/install-local.sh`. Inclua o diretório do comando no PATH.
3. Faça `ai-team login atlas --stage plan`, `ai-team login argus`, `ai-team login sentinel` e `ai-team login atlas --stage review`. Confirme Atlas/Sentinel em contas distintas; rode `ai-team doctor`.
4. No alvo, leia AGENTS/OpenSpec; identifique testes, lint, build, restrições e critérios de aceitação. Adapte [PROJECT-AGENTS.md](PROJECT-AGENTS.md) se faltarem instruções. Não copie indiscriminadamente o framework nem substitua regras existentes.
5. Prepare imagem de testes confiável com dependências offline. Commite os arquivos do alvo, mantenha branch nomeada e origin válido. Configure `ai-team init --test-image IMAGEM --check 'COMANDO REAL'`, repetindo checks necessários. Para configuração anterior, use `--upgrade` deliberadamente; preserva backup e não migra tarefas. Confira [modelos por etapa](../docs/ISOLATED-AGENT-STAGES.md) e acesso nas contas.
6. Comece com uma alteração pequena. Inspecione diff, checks e pareceres vinculados ao SHA; execute aceitação e cenários de falha antes de ampliar autonomia.
7. Use `deliver` para branch local; `--push` ou `--pr` para a entrega pretendida. Observe CI e revisão antes de autorizar merge. Deploy é uma ação distinta.

## Pedido inicial sugerido

Substitua os campos e passe o texto como argumento de `ai-team run` na raiz do alvo:

> Leia AGENTS.md e OpenSpec deste repositório. Objetivo: [mudança pequena e verificável]. Preserve [contratos e restrições]. Registre proposta, critérios e tarefas no OpenSpec antes de implementar. Faça a menor alteração pertinente e testes necessários. O coordenador executará os checks offline configurados e solicitará validação Sentinel/OpenAI e revisão Atlas/Claude em sessões isoladas. Reporte evidências e limites. Pare diante de aprovação necessária, estado incerto ou mudança fora do escopo.

Um prompt não instala ferramentas, autentica contas nem concede autorização de produção. Consulte [recuperação](../docs/SESSION-STATE.md) se o processo for interrompido.
