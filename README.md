# ai-engineering-team

Fluxo de engenharia com Atlas (implementação/Codex), Sentinel (revisão/Codex em outra conta) e Argus (revisão/Claude Code), usando governança versionada e evidências por SHA.

## Começar no Linux

O comando `ai-team` permite pedir trabalho na raiz de um repositório alvo. Ele prepara um clone independente, executa ciclos limitados de implementação, testes offline e duas revisões. A entrega é explícita em branch/PR; merge e deploy são ações separadas.

```bash
git clone --branch main https://github.com/leandroclf/ai-engineering-team.git
cd ai-engineering-team
bash scripts/install-local.sh --check
bash scripts/install-local.sh
export PATH="$HOME/.local/bin:$PATH"
ai-team login atlas
ai-team login sentinel
ai-team login argus
ai-team doctor
```

Requer Linux, Git, Python 3.10+ com venv/ensurepip e Docker Engine acessível ao usuário. `gh` é opcional até a criação de PR. O instalador não instala pacotes do sistema nem configura contas. Mantenha este checkout: o comando instalado aponta para ele.

No alvo, prepare uma imagem de testes com dependências offline e configure checks reais da stack. Siga o exemplo completo do [guia local Linux](docs/LOCAL-LINUX-WORKFLOW.md) antes da primeira tarefa. Use o [checklist de bootstrap local](templates/LOCAL-WORKFLOW-BOOTSTRAP.md) para configurar o host e o projeto.

## Modos de operação

| Modo | Entrada | Coordenação e evidência |
| --- | --- | --- |
| Local Linux, implementado | `ai-team` no alvo | Coordenador limitado em Python; Docker por função; checks sem credenciais; dois pareceres antes da entrega |
| Dots nativos | [Bootstrap do Engineering Dot](templates/ENGINEERING-DOT-BOOTSTRAP.md) | Coordenação persistente na plataforma, sob permissões nativas; aceitação ao vivo continua separada |
| Harness de validação | [Runbook dos containers](runbooks/CONTAINER-RUNTIMES.md) | Fixtures por CLI e transporte experimental `pr_chain.sh`; não é a entrada do usuário para trabalhar em um site |

O CLI local não instancia Dots, não é um serviço sempre ativo e não substitui a plataforma de nenhum provedor. Templates de Dots não são scripts de instalação do host. A configuração `ai-team init` fica fora do alvo; o registro YAML de portfólio pertence ao modo de governança/Dots.

## Documentação

- [Instalação, comandos, recuperação e limites](docs/LOCAL-LINUX-WORKFLOW.md)
- [Onboarding de projetos](docs/PROJECT-ONBOARDING.md) e [ambientes de execução](docs/EXECUTION-ENVIRONMENTS.md)
- [Entrega e aprovação](docs/DELIVERY-LIFECYCLE.md), [validação](docs/VALIDATION.md) e [revisão documental](docs/DOCUMENTATION-REVIEW.md)
- [Planejamento local e aceitação pendente](openspec/changes/local-linux-workflow/tasks.md) e [roadmap](openspec/roadmap.md)
- [Arquitetura de Dots](docs/DOT-NATIVE-ARCHITECTURE.md), [contratos executáveis](docs/DOT-NATIVE-OPERATION-GATES.md) e [guias dos provedores](docs/PROVIDER-GUIDANCE-REVIEW.md)
- [Documentação consolidada e baseline de requisitos](docs/00-toc.md)
- [Marketplace de skills](skills/README.md) e [catálogo versionado](skills/catalog.yaml)
- [Benchmarks e avaliação de skills](docs/SKILL-BENCHMARKS.md) e [contrato interno de avaliação](evaluation/benchmarks.yaml)

## Governança e prontidão

R0: leitura; R1: mudanças locais reversíveis; R2: dependências, infraestrutura e segurança; R3: produção, ações destrutivas ou irreversíveis. R3 exige autorização específica e todas as aprovações nativas. Leia [AGENTS.md](AGENTS.md) e as instruções do alvo antes de modificar código.

Os agentes conseguem ler suas próprias credenciais no container. Os checks do coordenador usam um container separado, offline e sem volumes de contas. A restrição de executar testes dentro do agente ainda é política; não existe enforcement de cada ferramenta interna. A aceitação com contas reais distintas e um projeto no Linux do operador permanece aberta. CI e testes controlados não certificam produção autônoma.

Skills disponíveis: tech-lead, architect, backend, qa, security, code-review, observability, java-spring, node-typescript, python-fastapi, aws, kubernetes e github-workflow. O framework deve manter a governança portátil e usar as ferramentas oficiais dos provedores.
