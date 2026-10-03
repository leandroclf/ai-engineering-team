# Revisão documental e bootstrap — 2026-10-03

Base: main `68f7f60` (PR #12). A revisão compara as instruções operacionais com `scripts/local_team.py`, instalador/wrapper, contratos, Dockerfile e CI. Não altera versões de provedores nem revalida fontes externas históricas; fatos operacionais vêm do código atual.

## Escopo e decisões

| Grupo | Resultado |
| --- | --- |
| README, guia Linux, onboarding | Instalação pela main, pré-requisitos reais, imagem/checks offline, configuração externa, comandos e diagnóstico |
| Arquiteturas/roteamento/ambientes | Responsabilidades Atlas/Sentinel/Argus compartilhadas; local CLI, Dots nativos e harness explicitamente distintos |
| Entrega, estado, loops e recuperação | Checks/duas revisões antes da entrega; CI posterior; checkpoints limitados; nenhum replay de entrega incerta; merge/deploy separados |
| Runbooks e templates de bootstrap | Dots continuam como prompts nativos; novo checklist Linux; volumes/UIDs e autenticação do harness não confundidos com ai-team |
| Documentação numerada/anexos | Visão geral atualizada, baseline e diagramas históricos identificados; IDs/modelo de rastreabilidade preservados |
| Políticas e workflows genéricos | Frescor, risco, qualidade, segurança, concorrência e workflows por stack continuam aplicáveis; presença da política não comprova enforcement |
| OpenSpec e registro | Roadmap inclui fluxo local integrado e revisão documental; comandos completos referenciados em VALIDATION; tarefas LIVE mantidas abertas |
| Relatórios e validation/runs | Evidência datada preservada; não reescrever falhas, waivers ou conclusões antigas como novos PASS |

## Mudanças do bootstrap

Preflight antes de instalar: Linux, Python 3.10+/venv/ensurepip, Git, readlink, Docker daemon e conflito de destino. Compose deixa de ser requisito local. `--check` não instala; `--help` explica uso; `AI_TEAM_BIN_DIR` permite destino do usuário. Arquivos, diretórios e links quebrados de outras instalações são preservados. Um novo comando só é publicado após dependências/build; o destino é rechecado sem substituição forçada. Reinstalação do mesmo link é permitida. Wrapper informa como recuperar venv ausente.

O instalador não é transacional: falha pode deixar venv ou camadas de imagem. Não remove volumes, não autentica nem altera perfil/grupos/pacotes do host. Se o comando já existia desta instalação, ele continua apontando para ela durante a atualização; encerre tarefas antes de reinstalar.

## Verificação e limites

Comandos atuais estão em [VALIDATION.md](VALIDATION.md). O novo verificador cobre targets locais e fechamento de fences em todos os Markdown de README/AGENTS/docs/runbooks/templates/OpenSpec. O verificador consolidado cobre âncoras, IDs, front matter e diagramas. Nenhum deles prova semântica de todos os exemplos ou disponibilidade de URLs externas.

Testes do bootstrap usam executores controlados para observar efeitos e preservar destinos. CI executa a instalação real em Ubuntu e o canary Docker offline. A aceitação com três logins, contas OpenAI distintas e tarefa no site do operador permanece aberta. Enforcement por ferramenta, cancelamento remoto e Dots ao vivo não são demonstrados por esta revisão. Acompanhe [tarefas documentais](../openspec/changes/align-workflow-documentation/tasks.md) e [aceitação local](../openspec/changes/local-linux-workflow/tasks.md).

Verificação local executada: 23 testes do harness e 68 unitários aprovados; validadores estrutural/hardening/contratos aprovados; 116 Markdown verificados; consolidado com 1373 links e 572 referências de identificador; sintaxe Bash e help do instalador/CLI aprovados. Preflight real neste ambiente retornou BLOCKED por Docker ausente, antes de efeitos. Instalação/canary reais são observados separadamente no CI, conforme registro OpenSpec.

CI do commit `2d4bcf1`, [push](https://github.com/leandroclf/ai-engineering-team/actions/runs/37084628900) e [PR](https://github.com/leandroclf/ai-engineering-team/actions/runs/37084631354): SUCCESS. Em ambos, framework e runtime-smoke aprovaram; runtime-smoke executou build/probes offline dos CLIs, preflight/instalação reais, comando instalado e canary de isolamento/source imutável. Publicado na [PR #13](https://github.com/leandroclf/ai-engineering-team/pull/13); isso não significa merge ou aceitação autenticada.
