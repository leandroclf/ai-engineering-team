# Evolução do ai-engineering-team — 1º de outubro de 2026

Baseline auditada: `1c6e681f7b1176401f383da79c6b14aca2e0f852` (`main`). Último commit observado: 01/10/2026 às 21:26:30, America/Sao_Paulo. Ambiente desta análise/implementação: CHAT-GITHUB, com execução local dos verificadores de repositório. Risco: R2, contratos de autorização/evidência. Nenhum merge, deploy ou alteração de conta/permissão.

## Diagnóstico

O projeto evoluiu de uma arquitetura declarativa para uma camada CLI com evidências reais de implementação, falha, correção e revisão cruzada. Ainda não é um Engineering Dot operacional validado: coordenação persistente, delegação nativa, autorização revogável em execução e independência de contas não foram comprovadas.

| Dimensão | Evidência observada | Limite da conclusão |
|---|---|---|
| Governança e arquitetura | AGENTS, OpenSpec, contratos e documentação consolidada | Presença/consistência não garantem adesão de um agente |
| Codex/Atlas | S01-S06 e H02 registrados; falhas S02/S05 corrigidas e reexecutadas | Fixtures controladas; não constituem operação de portfólio |
| Sentinel | Revisões CLI e montagem read-only registradas | Mesma conta OpenAI de Atlas, waiver W-001; sem independência de conta |
| Argus/Claude | CA01-CA08 e cadeia CLI registradas | Provedor distinto; mesma infraestrutura de harness/transporte pode falhar correlacionadamente |
| GitHub | PRs #7/#8/#9 confirmadas fechadas sem merge; sentinel/review e argus/assurance success nos SHAs de cada PR | Status publicados pelo orquestrador; não equivalem a branch protection ou identidade independente |
| CI | Relatório final preserva três cadeias PR/CI | Nesta auditoria, a consulta do conector para o último SHA da main não retornou workflow/status; não se presume CI verde para essa revisão |
| Hardening | Políticas existentes + novos schemas/checks/testes executáveis | Adaptador confiável antes de cada ação ainda ausente |
| Dots reais | D8/H6 continuam abertos | Sem evidência de OPENAI-DOT-A/B nesta sessão |

## Auditoria de evidências anteriores

104 manifests encontrados em `validation/runs/`: 83 PASS, 5 FAIL, 15 INCONCLUSIVE e 1 BLOCKED. Todos os caminhos declarados em `evidence_locations` existem. Isso é uma verificação de integridade referencial; não reexecuta os agentes, não autentica a origem dos arquivos e não converte 83 PASS de cenários distintos numa taxa de confiabilidade geral.

| Ambiente | PASS | FAIL | INCONCLUSIVE | BLOCKED |
|---|---:|---:|---:|---:|
| OPENAI-CLI-A | 31 | 5 | 3 | 1 |
| OPENAI-CLI-B | 21 | 0 | 0 | 0 |
| CLAUDE-CLI | 31 | 0 | 12 | 0 |

A evidência mais valiosa é a falha reproduzida e corrigida. S02 revelou colisão de identificador/perda de dados após DELETE; S05 revelou interpretação indevida de urgência como autorização R3. Os reruns corrigidos sustentam a melhoria nessas fixtures, sem autorizar a conclusão de segurança universal.

Os relatórios Argus e pre-Dot e o roadmap ainda continham bloqueios antigos: sandbox do Atlas, cadeia CLI e S02. Foram acrescentadas reconciliações explícitas, preservando o histórico. `validation/FINAL-REPORT.md` continua sendo a referência consolidada da camada CLI.

## Alterações desta rodada

Change: `openspec/changes/harden-dot-native-operations/`.

- Quatro JSON schemas estritos para task, lease, estado atual de autorização e evidência.
- Checagem de escopo/revisão, expiração, revogação, projeto/repositório/branch/base, ações permitidas/negadas e caminhos.
- R0 sem mutação e R3 entregue ao fluxo de aprovação; limites de tentativas, duração e writes; circuito aberto interrompe a checagem.
- Consistência de evidência: comando obrigatório, exit code, artefato/hash, SHA final e CI, sem converter hash em prova de autenticidade.
- Preflight CLI somente leitura, sem expor saída de autenticação; ausência/timeout/login não geram falso PASS.
- Testes de falha e CI ampliado com schemas, unitários e verificação da documentação consolidada.

Os checks são uma biblioteca para o adaptador confiável. Não reservam orçamento, não persistem circuito, não executam writes, não fazem lease locking e não impõem regras ao Dot nativo. O hardening operacional permanece em andamento até essa integração.

## Validação desta rodada

25 testes unitários passaram. Os verificadores estrutural, hardening, JSON schemas/exemplos e documentação passaram; a documentação consolidada contém 11 documentos, 1.342 links relativos e 572 referências de identificador verificados. Evidências locais dos comandos: `validation/repository-checks/20261001-dot-native/`.

O preflight real retornou UNAVAILABLE/exit 2: Codex CLI ausente. Também não foram encontrados `claude`, `gh` ou `docker` neste ambiente. Portanto, CODEX-PRE-DOT com CLI autenticado, novas execuções Sentinel/Argus e criação/validação de Dots não foram executados aqui. As execuções históricas dos containers não são invalidadas pela ausência desses executáveis nesta sessão.

## Próxima evolução recomendada

1. Revisar esta implementação R2 no SHA da PR com Sentinel e Argus; integrar o gate a um adaptador com estado confiável, reserva atômica e reconciliação idempotente.
2. Rodar CODEX-PRE-DOT nos containers já utilizados, agora com os contratos executáveis. Preservar falhas e verificar CI por revisão.
3. Resolver W-001 com segunda conta e reexecutar os cenários de independência; validar AS07 de waiver.
4. Executar Atlas/Sentinel reais, revogação durante execução, isolamento entre projetos, orçamento/outage e aprovações nativas sem side effects destrutivos.
5. Exercitar portfólio controlado e fechar H6/D8 somente depois; gerar DOT-NATIVE-FINAL-REPORT com evidência reconciliada.

Não há motivo evidenciado para adicionar mais personas ou redesenhar a arquitetura. O próximo ganho vem de integração confiável dos controles e testes adversariais reais. Produção, merge-gating e novas permissões continuam fora desta rodada.
