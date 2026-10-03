# Operação local Linux — ai-team

Versão atual: 0.2.0, com [quatro etapas isoladas](ISOLATED-AGENT-STAGES.md). CLI para tarefas supervisionadas e ciclos locais limitados; não é certificação de produção autônoma. A aceitação com contas reais e um projeto do operador permanece obrigatória.

## Instalar uma vez

Pré-requisitos: Linux, Git, Python 3.10+ com venv/ensurepip e Docker Engine acessível ao usuário; `gh` é necessário somente para PR. Docker Compose é usado pelo harness histórico, não pelo CLI local. Acesso ao daemon Docker é uma autoridade ampla do host: não entregar socket ao agente. O instalador não usa sudo, não muda grupos e não instala pacotes do sistema.

```bash
git clone --branch main https://github.com/leandroclf/ai-engineering-team.git
cd ai-engineering-team
bash scripts/install-local.sh --check
bash scripts/install-local.sh
export PATH="$HOME/.local/bin:$PATH"
ai-team --help
```

Mantenha o checkout do framework; o link instalado depende dele. Atualize deliberadamente via Git e repita instalação/build, sem atualização durante uma tarefa. `.venv` não é versionado. O instalador preserva um comando ai-team preexistente de outra instalação.

O fluxo 0.1.0 foi integrado à main na PR #12. `--check` verifica plataforma, executáveis, Python, acesso ao daemon e conflito do destino sem instalar nada; não verifica login nem dependências offline do alvo. `--help` mostra as opções. O build precisa terminar com sucesso antes de publicar um novo link. Falhas podem deixar a venv ou camadas Docker: corrija a causa e repita o instalador; não apague dados de contas como recuperação.

Por padrão o destino é `~/.local/bin/ai-team`; `AI_TEAM_BIN_DIR` permite outro diretório do usuário. Ajuste PATH para esse diretório. Arquivos, diretórios e links quebrados de outra instalação são preservados. O bootstrap não altera seu perfil de shell, não faz login e precisa de rede para obter pacotes/imagem. Para atualizar, encerre tarefas, confira o checkout do framework, atualize via Git e repita preflight/instalação. Os IDs das imagens já congelados em tarefas não são atualizados.

## Autenticar

```bash
ai-team login atlas --stage plan
ai-team login sentinel
ai-team login argus
ai-team login atlas --stage review
ai-team doctor
```

Cada etapa usa `ai-team-<role>-<stage>-home`, distinto dos volumes antigos. Atlas autentica OpenAI em plan e Claude em review; Argus usa Claude em implement e Sentinel usa OpenAI em validate. Não copiar credenciais entre volumes. Atlas/Sentinel devem usar contas distintas para satisfazer W-001; usar janelas privadas distintas no login. Argus usa a assinatura configurada do Claude. Modelos e esforços são explícitos por etapa; consulte [perfis](ISOLATED-AGENT-STAGES.md). Login é feito diretamente na interface oficial; não envie credenciais ao chat.

Doctor verifica executáveis, imagem, capacidades e disponibilidade dos quatro logins; retorna código 2 se requisitos ou logins obrigatórios faltarem. A ausência de gh não bloqueia trabalho local. Doctor não comprova contas distintas, acesso ao projeto ou correção das respostas. Logins consomem a assinatura conforme as regras do provedor. Timeout/turnos não são limite de cobrança.

## Configurar o repositório alvo

Na raiz do seu site, com checkout limpo, branch nomeada e origin configurado. Salve/commite o trabalho existente antes de iniciar; não use stash/reset automático para contornar a proteção. O exemplo simples abaixo pressupõe dependências disponíveis na imagem; para npm, use a imagem e os checks completos da próxima seção:

```bash
cd ~/projetos/meu-site
ai-team init --test-image meu-site-tests:local \
  --check 'npm run lint' --check 'npm test' --check 'npm run build'
```

`meu-site-tests:local` precisa existir e conter ferramentas/dependências necessárias para executar sem rede. Prepare a imagem de testes conforme a stack do site; não colocar credenciais no Dockerfile nem na imagem. Para Python padrão, uma imagem Python previamente baixada pode bastar; para Node com dependências, use imagem própria com cache offline e inclua a cópia das dependências no comando. Não executar npm ci com expectativa de internet neste runner.

Configuração fica em `$XDG_STATE_HOME/ai-team/projects/<id>/config.json` (padrão `~/.local/state`). O caminho é exibido pelo init. Verifique os comandos antes de usar: são shell dentro do container de testes, nunca no host. O init não sobrescreve configuração existente. Limites: `--timeout` por etapa, `--max-cycles` até cinco e `--max-seconds` até oito horas; padrão 900 segundos/3 ciclos/2 horas.

Para migrar uma configuração existente, encerre tarefas e repita o comando init com `--upgrade`, imagem e todos os checks explícitos. O coordenador salva backup privado da configuração anterior. Config/tarefas usam versão 2; tarefas antigas não são convertidas nem retomadas/entregues sob o novo fluxo. Modelos e esforços ficam na configuração e são congelados por tarefa; flags `--plan-model`, `--implement-model`, `--validate-model`, `--review-model` e `--*-effort` permitem escolhas deliberadas do mesmo provedor. Não há fallback automático. Defaults e limites: [contrato de etapas](ISOLATED-AGENT-STAGES.md).

### Exemplo de imagem para um site npm

Se seu projeto usa `package-lock.json`, prepare este Dockerfile de testes fora do framework (ajuste a versão Node ao projeto):

```dockerfile
FROM node:22-bookworm-slim
WORKDIR /deps
COPY package.json package-lock.json ./
RUN npm ci
WORKDIR /work
```

Salve o exemplo como `Dockerfile.tests`, revise o contexto de build e configure `.dockerignore` para excluir credenciais. Commite os arquivos de configuração no alvo antes de `run`, pois o checkout deve estar limpo. Construa deliberadamente no repositório alvo:

```bash
docker build -f Dockerfile.tests -t meu-site-tests:local .
ai-team init --test-image meu-site-tests:local \
  --check 'cp -R /deps/node_modules /work/node_modules' \
  --check 'npm run lint' --check 'npm test' --check 'npm run build'
```

Esse exemplo requer que os scripts existam no package.json. O build da imagem obtém dependências com rede antes da tarefa; a execução dos checks fica offline. Se Argus alterar o lockfile, reconstrua a imagem e configure uma nova tarefa: a imagem de uma tarefa iniciada é imutável. Não reutilize dependências antigas como evidência para um novo lockfile.

## Pedir trabalho

```bash
ai-team run 'Melhore o formulário de contato. Registre plano e critérios no OpenSpec, preserve o contrato atual e adicione testes pertinentes.'
ai-team run --background 'Corrija o bug documentado na issue local e valide a solução'
ai-team status
ai-team status <task-id>
ai-team stop <task-id>
ai-team resume <task-id>
```

Fluxo: cópia Git independente → Atlas/OpenAI planeja → host registra OpenSpec → Argus/Claude implementa → commit do host → testes offline → Sentinel/OpenAI valida → Atlas/Claude revisa em nova sessão → correção ou replanejamento limitado → REVIEWED. O checkout original permanece intacto. O clone e evidências ficam no diretório da tarefa exibido por status. Não copiar o framework para cada projeto. Instruções AGENTS/OpenSpec do alvo são lidas pelo executor.

Resume aceita somente uma tarefa RUNNING com checkpoint conhecido e sem processo ativo registrado. Uma interrupção no meio da etapa, pasta de staging parcial ou efeito externo incerto exige inspeção; não há repetição automática. Uma tarefa FAILED/STOPPED exige um novo pedido depois de resolver a causa. O prazo original não é estendido por retomada.

## Entregar

```bash
ai-team deliver <task-id>
ai-team deliver <task-id> --push
ai-team deliver <task-id> --pr
```

Sem flags, importa os commits para uma nova branch `ai-team/<task-id>` no alvo, sem trocar seu checkout. `--push` publica essa branch; `--pr` publica e abre PR draft no GitHub usando Git/gh do operador. Só é permitido se alvo, origin e SHA revisado não mudaram. O origin deve usar GitHub HTTPS ou SSH padrão; aliases customizados exigem adaptação explícita. O host precisa de autenticação Git/gh configurada. Push normal, nunca force; nenhum merge/deploy.

Se entrega ficar DELIVERY_PENDING, consulte o remoto/PR antes de qualquer novo efeito. A CLI bloqueia replay automático; preserve state.json, logs e SHAs. Uma nova revisão é necessária depois de alterar código ou base. REVIEWED não substitui CI/proteção de branch do GitHub.

## Fronteiras e operação

Os agentes têm rede para autenticar/usar modelos e podem ler as próprias credenciais no respectivo container. Tests não recebem volumes de contas, GitHub token/SSH agent, Docker socket nem rede. Rootfs dos containers é read-only, usuário não-root, recursos e processos limitados; workspace de testes é temporário. O host e daemon Docker são confiáveis. Use imagens próprias confiáveis e repositórios conhecidos; não alegar isolamento de kernel ou DLP completo.

Git metadata é montado read-only para agentes; só o host faz commits. Evidências finais ficam fora dos mounts de agentes; apenas staging de saída é gravável por uma função. Logs brutos podem conter informações do projeto: diretório privado, inspecione antes de compartilhar. Hash registra integridade dos bytes, não autentica veracidade do parecer.

Stop registra pedido local, termina processo e remove container correspondente. Interromper cliente/container não comprova cancelamento da tarefa remota. Verifique atividade dos provedores separadamente. Não apagar volumes para resolver um erro sem avaliar perda do login. Nunca usar docker system prune como recuperação automática.

O coordenador valida suas etapas, não cada tool call interno. Aprovações nativas continuam obrigatórias; R3 não deve ser automatizado via prompt. Integração fina de leases com cada ação e testes reais de revogação seguem no OpenSpec.

Argus implementa com ferramentas de arquivo sem Bash/Agent/MCP. Atlas planeja e Sentinel valida com sandbox Codex read-only e checkout somente leitura; execução de código do alvo nesses contextos continua proibida por política. O isolamento é mecânico para a etapa de checks do host; a proibição dentro do agente é política e precisa de um adaptador nativo para enforcement por ferramenta. Esta versão é candidata a uso supervisionado em repositórios confiáveis, não uma garantia de segurança para código hostil.

## Aceitação antes de uso produtivo

1. Doctor com quatro logins disponíveis e confirmação de contas Atlas/Sentinel distintas.
2. Primeira tarefa pequena no seu site, com checks offline aprovados, dois pareceres e diff inspecionado.
3. Testar falha de checks, parecer inválido, timeout, stop, interrupção e retomada.
4. Entregar branch/PR e observar CI do SHA final; configurar proteção de merge com autorização específica.
5. Somente então aumentar escopo e autonomia; manter merge/deploy separados.

## Referência de comandos e diagnóstico

| Comando | Uso |
| --- | --- |
| `ai-team --help`, `ai-team <comando> --help`, `ai-team --version` | Consultar a interface instalada |
| `ai-team doctor` | Probes de ferramentas, imagem e quatro logins |
| `ai-team login atlas --stage plan`, `ai-team login atlas --stage review`, `ai-team login sentinel`, `ai-team login argus` | Quatro contextos de login isolados |
| `ai-team init --test-image IMAGEM --check COMANDO` | Configuração externa; repetir checks na ordem de execução |
| `ai-team run 'pedido'` | Tarefa supervisionada; `--background` desacopla o processo local |
| `ai-team status [task-id]` | Listar ou inspecionar tarefas |
| `ai-team stop task-id`, `ai-team resume task-id` | Parada local e retomada em checkpoint seguro |
| `ai-team deliver task-id`, `--push`, `--pr` | Branch local, publicação ou PR draft explícitos |

Erros de instalação: confirme Python com venv/ensurepip, serviço Docker e acesso do usuário; use o gerenciador de pacotes da distribuição para corrigir pré-requisitos. Se o checkout do framework foi movido ou removido, reinstale a partir do novo caminho e resolva o link anterior deliberadamente. Não execute o instalador com sudo para contornar acesso ao daemon.

Estado/evidências usam `$XDG_STATE_HOME/ai-team` (padrão `~/.local/state/ai-team`), com configuração por projeto e clone/logs por tarefa. Preserve o diretório para recuperação; logs podem conter dados sensíveis e não há expurgo automático. Os volumes de login Docker têm ciclo de vida separado. Faça backup privado das evidências necessárias, sem versionar credenciais.

Planejamento: [tarefas e aceitação](../openspec/changes/local-linux-workflow/tasks.md). Referências registradas na revisão de provedores: [Codex não interativo](https://learn.chatgpt.com/docs/non-interactive-mode), [Claude CLI](https://code.claude.com/docs/en/cli-reference), [Docker run](https://docs.docker.com/engine/containers/run/).
