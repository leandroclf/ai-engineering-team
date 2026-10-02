# Revisão da evolução do ai-engineering-team

Data: 01/10/2026, America/Sao_Paulo. Base examinada: `1c6e681f7b1176401f383da79c6b14aca2e0f852`.
Escopo: R1 nas correções locais do harness; publicação de branch/PR para revisão. Nenhuma alteração de permissões, merge ou implantação de produção.

## Conclusão
O projeto evoluiu de governança declarativa para um framework com harness, containers e evidências comportamentais reais via CLI. Há mérito na descoberta e correção dos problemas S02 (identidade após DELETE), S05 (R3) e nos testes de injeção. Ainda não é um Engineering Dot validado em operação contínua. Os testes não demonstram independência entre contas, autorização revogável em tempo real nem enforcement de merge.

A pesquisa anexada representa uma fotografia anterior. `CODEX-PRE-DOT` não deve ser tratado como inteiramente inédito: já existem execuções CLI registradas em `FINAL-REPORT.md`. Porém `harden-dot-native-operations` não existia na base examinada; esta change agora registra a diferença entre política, controle executável e evidência live, sem declarar tudo concluído.

## Evolução observável

| Área | Evidência atual | Limite |
|---|---|---|
| Arquitetura | Atlas coordena; Codex executa; Sentinel revisa; Argus fornece assurance | Dots ao vivo pendentes |
| Governança | AGENTS, Skills, OpenSpec, contratos e 76 artefatos estruturais obrigatórios | Tokens/parse não provam enforcement |
| Isolamento | Containers por função e checkout de revisores somente leitura | Atlas/Sentinel compartilham usuário OpenAI (W-001) |
| Comportamento CLI | S01–S06 e H02; defeitos encontrados e reruns documentados | Não repetidos neste ambiente; evidência histórica |
| Transporte | PRs #7/#8/#9 fechados sem merge, confirmados na API | Success publicado não garante validade de cada parecer |
| CI | Run 36946017161, success na base examinada | Validação estrutural; não comprova comportamento agentic |
| Autorizações | R3 exige confirmação separada; lease de concorrência possui expires_at | Falta contrato separado de autorização, revogação e validação por ação |
| Documentação | Requisitos, regras, casos de uso e rastreabilidade consolidados | Aumento documental não substitui validação operacional |

Não havia PRs abertos na inspeção inicial. Último commit da base: 01/10/2026 às 21:26:30 (-03:00).

## Auditoria de evidência histórica

O transporte antigo verificava o SHA do checkout em `check.txt`, mas extraía apenas `verdict` do texto. Ele não exigia que o próprio parecer declarasse esse SHA nem que seu YAML fosse válido.

| Cadeia | Sentinel | Argus no gate novo | Motivo |
|---|---|---|---|
| pr1 / PR #7 | Aceito no transporte | SHA_MISMATCH | Parecer declara `5545cbcc5309526413f3ce43a9ca8904a2d995b3`; PR/checkout é `45dc03d25caebdf9e219e19efd14cba1c43eeba4` |
| pr2 / PR #9 | Aceito no transporte | Aceito no transporte | Parecer estruturado e SHA `572740b1b25278a4419b76edd0a809d553b4e3f7` coincidem |
| pr3 / PR #8 | Aceito no transporte | INVALID_EVIDENCE | YAML do Argus não é parseável (valores simples contêm `: `); SHA textual coincide |

“Aceito no transporte” não significa confirmação independente da qualidade do código. O conteúdo de pr1 pode se referir a um commit de implementação equivalente, mas falta um vínculo explícito válido no resultado; equivalência não dispensa o contrato de SHA. pr3 pode ser reparado pela emissão de resultado estruturado válido, mas o registro original permanece preservado. Não alteramos os manifests antigos nem os statuses externos. A afirmação histórica de 3/3 deve ser lida com essa ressalva; pr1 e pr3 precisam de novas evidências.

## Correções desta revisão

- Executor ausente e timeout geram manifesto e diagnóstico em vez de traceback sem evidência.
- Falha de setup impede lançamento do executor; falha de executor/check retorna exit não zero.
- Identificador de execução não aceita traversal; timeout precisa ser positivo.
- CI tem deadline e precisa de success antes dos revisores.
- Cada processo de revisão tem seu exit aguardado; falha não desaparece em `wait`.
- O gate valida YAML, head SHA declarado, manifesto e exits observados antes de publicar success.
- 20 testes cobrem as falhas e auditam os seis resultados antigos; CI passa a executar esses testes.

Os testes do shell usam CLIs controladas em diretórios temporários. Eles validam o harness; não acessam GitHub nem executam modelos. O gate não valida ainda todo o conteúdo semântico dos findings, gates solicitados, autorizações ou assinatura/proveniência do parecer.

## Validação nesta sessão

`python -m unittest discover -s tests -p 'test_*.py' -v`: 20 testes aprovados.
`python scripts/validate.py`: aprovado, 76 artefatos obrigatórios.
`python scripts/validate_hardening.py`: aprovado.
`bash -n scripts/pr_chain.sh` e `git diff --check`: aprovados.

O preflight real `20261001-workmode-preflight` tentou iniciar Codex pelo harness e registrou BLOCKED, exit 127. Codex e Claude não estão instalados neste ambiente. Não houve execução de modelo, login, teste live Dot ou simulação apresentada como PASS comportamental.

## Próximas prioridades

1. Repetir a cadeia no runtime já configurado, exigindo parecer parseável e SHA exato; renovar pr1/pr3.
2. Completar authorization lease, schemas e validadores negativos; integrar budgets e revogação antes dos efeitos externos.
3. Resolver W-001 com conta distinta; manter a distinção entre conta, container e modelo independentes.
4. Configurar gates de merge mediante autorização específica de mudança de permissões. Status publicado e PR draft não bloqueiam merge por si só.
5. Bootstrap e testes nos Dots reais, incluindo revogação, stale memory, isolamento, concorrência e falhas. Fechar D8 somente então.

A recomendação é manter Atlas/Sentinel/Argus e priorizar enforcement e evidência. Expandir agentes ou documentação agora não resolve essas pendências.
