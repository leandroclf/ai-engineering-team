# Revisão dos guias oficiais dos provedores

Revisão: 01/10/2026 (America/Sao_Paulo). Bases: main `1c6e681`, PR #10 `a88bc6e`, PR #11 `10f5252`. Fontes consultadas diretamente, sem assumir que o relatório anterior descreve o estado atual. Este documento registra conhecimento verificado nesta data; não promete atualização permanente do modelo nem validade indefinida dos guias.

## Resultado da revisão

A arquitetura Atlas → Codex → GitHub/CI → Sentinel → Argus continua adequada ao objetivo de engenharia assistida. O projeto agora tem contratos e experimentos reais de CLI, mas a publicação de um status depende de um host confiável e o D8 continua aberto. As duas PRs se sobrepunham no OpenSpec, CI e documentação; foram reconciliadas em uma única linha de integração, preservando as evidências históricas e as duas suítes de testes.

## Fontes e decisões

| Fonte oficial | Orientação verificada | Aplicação no projeto |
|---|---|---|
| [OpenAI: execução não interativa](https://learn.chatgpt.com/docs/non-interactive-mode) | JSONL para eventos; JSON Schema para resposta; permissões mínimas; autenticação de conta tem restrições em CI público | Codex usa `--output-schema` nas revisões; CI público executa apenas verificadores, sem login de usuário |
| [OpenAI: autenticação](https://learn.chatgpt.com/docs/auth) | Login de conta e credenciais API são caminhos distintos; `codex login status` inspeciona o método | Preflight não inicia login, copia credenciais ou muda cobrança |
| [OpenAI: comandos](https://learn.chatgpt.com/docs/developer-commands) | Flags oficiais de aprovação, sandbox, resultado e modo efêmero | Aprovação `never` no harness sem operador; Sentinel host em read-only; container continua com fronteira externa explícita |
| [OpenAI: aprovações](https://learn.chatgpt.com/docs/agent-approvals-security) | Aprovação e isolamento são controles distintos | Falta de operador significa negação; não adotar `--yolo` |
| [Claude: CLI](https://code.claude.com/docs/en/cli-reference) | `--restricted` é destinado a harnesses; tools disponíveis diferem de tools pré-aprovadas; prompts podem ser negados; limite de turnos disponível | Argus usa restricted, tools explícitas, MCP negado, `dontAsk`, `--permission-prompts none`, 30 turnos |
| [Claude: execução programática](https://code.claude.com/docs/en/headless) | Saída conforme schema aparece em `structured_output`; JSON é diferente de stream-json | Extração explícita e validação local; nunca procurar PASS em prosa como fallback |
| [Claude: permissões](https://code.claude.com/docs/en/permissions) | `dontAsk` nega o que exigiria interação, preservando limites administrados | Sem bypass de permissões; cenários que exigem interação ficam bloqueados |
| [Claude: settings](https://code.claude.com/docs/en/settings) e [hooks](https://code.claude.com/docs/en/hooks) | Projeto pode carregar automação; políticas administradas têm precedência | Restricted evita settings de projeto/usuário; desativação local de hooks preserva política administrada |
| [Claude: autenticação](https://code.claude.com/docs/en/authentication) | Login de assinatura é distinto de API; variáveis de ambiente podem alterar o caminho | Não converter silenciosamente assinatura em API; verificar conta e método no runtime do operador |
| [Claude: instalação](https://code.claude.com/docs/en/setup) | npm continua disponível e requer Node 22+; releases têm mecanismos de integridade | Manter Node 22 e versões CLI pinadas até validação; planejar verificação de integridade da imagem |
| [GitHub: segurança de Actions](https://docs.github.com/en/actions/reference/security/secure-use) | SHA completo torna a referência da action imutável; cuidado com código de PR em contextos privilegiados | Actions pinadas; eventos push/pull_request; nenhum pull_request_target privilegiado |
| [GitHub: GITHUB_TOKEN](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token) | Conceder apenas permissões necessárias | `contents: read`; credenciais GitHub removidas do ambiente do subprocesso do provedor |
| [checkout](https://github.com/actions/checkout) e [setup-python](https://github.com/actions/setup-python) | Guias atuais usam v7; setup-python requer runner compatível com Node 24 | v7 por SHA consultado no repositório oficial; `persist-credentials: false`; ubuntu-latest e Python 3.12 |
| [Dots](https://learn.chatgpt.com/docs/dots) | Disponibilidade depende de plano/workspace; ambiente Codex Cloud deve existir | Preflight humano/live inclui acesso real e ambiente preparado; não inferir elegibilidade da conta |
| [Controle de Dots](https://learn.chatgpt.com/docs/dots/controls) | Pausar Dot não encerra automaticamente filhos nem agendamentos | Runbook de parada enumera tarefas delegadas e schedules separadamente |
| [Acesso local](https://learn.chatgpt.com/docs/enterprise/cloud-local-access) | Revogação administrativa pode deixar tarefa Dot já autorizada terminar | Testar efeito em trabalho ativo e próximo efeito externo; não equiparar revogação a cancelamento imediato |
| [Codex App Server](https://learn.chatgpt.com/docs/app-server) | Aprovações são eventos do protocolo, associados a thread/turn/item | Avaliar adaptador fino que componha leases com eventos nativos; sem criar runtime paralelo |

A seleção de modelos, assinaturas e contas permanece a configurada pelo operador. Não há troca automática por modelos recém-lançados nem uso de API paga introduzido nesta revisão.

## Implementado

1. Parecer JSON obrigatório na cadeia PR: schema local, SHA exato, identidade da função, gates quality/security e bloqueio de HIGH/CRITICAL aberto ou sem verificação.
2. Captura correta do JSON estruturado do Claude e do arquivo final do Codex; erro de evento não pode ser mascarado por exit zero.
3. Preflight dos dois CLIs: versão, flags necessárias, login disponível; saída de autenticação não persistida. Divergência da versão revisada é reportada, sem upgrade implícito.
4. Timeout encerra o grupo de processos locais em POSIX. Isso não prova que uma tarefa remota ou container saiu.
5. Filtragem de credenciais GitHub/SSH do subprocesso e remoção de reasoning/init sensível de eventos. Valores sob chaves conhecidas são redigidos. Texto livre, stderr, prompts e patches ainda exigem inspeção antes de publicação; isso não é DLP completo.
6. CI com mínimo privilégio, limite de duração, cancelamento de execução obsoleta, ambas as suítes e Actions v7 pinadas. Dependabot propõe atualizações, sem auto-merge.
7. Dockerfile instala os mesmos requisitos de validação em venv; contexto de build limitado por dockerignore. CI inclui build e smoke offline/sem login; a execução autenticada permanece separada.

## Achados que continuam materiais

| Prioridade | Achado | Evolução e aceite |
|---|---|---|
| P0 | Leases são checagens puras; não interceptam cada ação do CLI | Adaptador confiável com revalidação imediatamente antes da operação, reserva atômica e deduplicação; teste revogação/concorrência |
| P0 | Testes Python executam código do checkout; container autenticado pode ler a própria credencial e acessar rede | Executor de testes sem credenciais, egress restrito e credencial fora do ambiente de código; canário de exfiltração controlado |
| P0 | Pareceres/hashes são afirmações até corroborados por host/CI confiáveis | Artefatos gravados fora do alcance do agente, proveniência e consulta GitHub do SHA; não aceitar hashes como autenticação |
| P1 | Sentinel usa a mesma conta de Atlas sob W-001 | Conta distinta e repetição AS; container distinto não prova independência |
| P1 | Cancelamento de cliente, container, Dot, filhos e agenda têm efeitos diferentes | Runbook de parada e reconciliação; comprovar ausência de novos efeitos após revogação |
| P1 | Novas flags/schemas ainda sem execução autenticada neste ambiente | Rebuild container, preflight em cada serviço, canário e repetição da cadeia pr1/pr3 |
| P1 | Status publicado não é proteção de branch nem prova de autor confiável | Ruleset/required checks e origem esperada configurados com autorização específica; validar bloqueio real de merge |
| P2 | Versões atualizadas automaticamente poderiam mudar comportamento de segurança | Descobrir release oficial → revisar changelog → canário → atualizar pin → repetir cenários críticos; nunca atualizar no meio da tarefa |
| P2 | Evidência cresce, não há métricas consolidadas de falha/custo | Medir duração, retry, falsos PASS, intervenção e consumo disponível por executor; não confundir custo estimado com cobrança da assinatura |

## Conclusão operacional

A evolução prioritária é conectar controles confiáveis às ações, reduzir exposição das credenciais e validar as superfícies nativas. Mais prompts/agentes não substituem essas etapas. O schema melhora o formato; a revisão independente e a evidência externa continuam necessárias. Ver `openspec/changes/align-provider-official-guidance/` e o hardening consolidado.
