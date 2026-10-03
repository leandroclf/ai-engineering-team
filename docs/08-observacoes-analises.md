---
titulo: "Observações, análises, recomendações e conclusão"
projeto: "ai-engineering-team"
autor: "Não informado"
data: "2026-10-01"
versao: "1.0.0"
classificacao: "Não informada"
status: "Rascunho para revisão"
---

# Observações, análises, recomendações e conclusão

> Baseline de requisitos/analises: revisão `791ac89`, 2026-10-01. Identificadores e recomendações históricas são preservados. Para operação atual, use [guia Linux](LOCAL-LINUX-WORKFLOW.md), [visão geral atualizada](02-visao-geral.md) e [reconciliação documental](DOCUMENTATION-REVIEW.md). Esta baseline não certifica o fluxo local nem comportamento ao vivo.

Navegação: [Índice](00-toc.md) · anterior: [07 Matriz de rastreabilidade](07-matriz-rastreabilidade.md)

## Legenda

- ⚠️ **Atenção:** risco, inconsistência, lacuna ou ponto que exige análise.
- ✅ **Confirmado:** informação comprovada pelos artefatos analisados.
- 🔄 **Alterado:** item modificado em decorrência de uma recomendação.

## Observações e análises

### Confirmado

- ✅ **Validação estrutural:** `scripts/validate.py` e `scripts/validate_hardening.py` passam, e o CI do GitHub (`validate`) foi bem-sucedido em cada commit publicado e conferido durante a validação. Isso comprova a estrutura, não o comportamento.
- ✅ **Camada de CLI validada por execução:** Atlas (S01 a S06 e H02), Sentinel (AS02, AS04, AS05, AS06, AS08, AS09, AS10), Argus (CA01 a CA08, com CA04, CA05 e CA07 em 3 de 3 ou mais) e a cadeia Atlas, Sentinel e Argus, inclusive por GitHub PR e CI (PRs #7, #8 e #9). Relatórios em `validation/FINAL-REPORT.md`, `validation/SENTINEL-CLI-REPORT.md` e `validation/ARGUS-ASSURANCE-REPORT.md`.
- ✅ **O processo de validação encontrou e preservou falhas reais:** S05 falhou 3 de 3 antes da regra de confirmação separada e passou 3 de 3 depois; S02 falhou 2 de 3 por regressão de perda de dados e passou 3 de 3 depois da regra de interação com invariantes; o fixture do S03 estava errado e foi corrigido; a primeira versão do harness travava aguardando entrada e o Argus ficou INCONCLUSIVE em quatro iterações da cadeia por permissões ausentes no harness, sem nunca emitir PASS sem evidência.
- ✅ **Sandbox do Codex indisponível no host:** o `bwrap` do Codex não inicia no host nem no contêiner (restrição de namespaces de usuário). A mitigação adotada foi o contêiner como fronteira, com checkout somente leitura para revisores.
- ✅ **Waiver registrado:** o uso do mesmo usuário OpenAI para Atlas e Sentinel está coberto pelo W-001 (`validation/waivers/W-001-shared-openai-account.yaml`), com escopo, controles compensatórios e expiração em 2026-10-31.

### Atenção

- ⚠️ **Independência entre contas não comprovada:** Atlas e Sentinel usam o mesmo usuário OpenAI. As revisões do Sentinel mostram o comportamento do revisor, não o isolamento entre contas (REC-015).
- ⚠️ **Camada de Dots ao vivo não validada:** Dot Atlas, Dot Sentinel, aprovação nativa, concorrência de leases, H01, H03 a H10 e AS07 não foram exercitados (REC-017). Estes itens permanecem INCONCLUSIVE, não PASS.
- ⚠️ **Sem branch protection:** os statuses `sentinel/review` e `argus/assurance` são publicados, mas nada impede merge sem eles (REC-016).
- ⚠️ **Divergências entre fontes:** ciclo de vida (REC-004), precedência do manifest (REC-010), comando de validação do registro (REC-011), status das propostas (REC-009), semântica do limite de retentativas (REC-023) e enquadramento de dependências em R2 (REC-024).
- ⚠️ **Especificação incompleta:** o OpenSpec tem 24 identificadores; o `traceability.md` da fonte cobre 22 (PORT-001 e PORT-003 sem cenário), e as capacidades posteriores não têm spec (REC-006).
- ⚠️ **Proporcionalidade não demonstrada:** o esforço do S02 não escalou sobre o do S01 (mediana de 5 comandos contra 6), e foi a execução com menos revisão que deixou passar a regressão (`validation/FINAL-REPORT.md`). O resultado atual do S02 vale para um único fixture.
- ⚠️ **Credenciais e rede nos contêineres:** o agente consegue ler as credenciais da própria conta dentro do contêiner, e a rede de saída é aberta, porque as CLIs precisam das APIs dos provedores (`runbooks/CONTAINER-RUNTIMES.md`, seção Limits). Por isso as evidências são varridas por tokens antes de cada commit.
- ⚠️ **Dependências sem versão fixada:** PyYAML é instalada sem versão no CI, e a imagem base é referenciada por tag (ver [02-visao-geral.md](02-visao-geral.md)).
- ⚠️ **Evidência sem política de retenção:** `validation/runs/` é versionado e cresce a cada execução; não há regra de retenção, rotação ou limpeza.
- ⚠️ **Ativos de marca em repositório público:** os arquivos de `docs/anexos/identidade/` são material da HIVEPlace e não foram publicados (REC-022).

## Recomendações

Cada recomendação traz o problema, a justificativa, a ação e os arquivos e seções alterados. As aplicadas estão com 🔄 e as pendentes com ⚠️.

<!-- BEGIN:gerado:rec-detalhe -->

### <a id="rec-001"></a>REC-001 — Consolidar glossário e siglas do domínio

- 🔄 **Alterado**
- **Problema:** Os termos Atlas, Sentinel, Argus, Dot, lease, waiver, veredito, gate, SHA, envelope e as siglas R0 a R3 são usados em dezenas de arquivos sem definição única.
- **Justificativa:** Termos sem definição central geram interpretações divergentes entre agentes e leitores.
- **Ação:** Glossário e siglas completos criados, incluindo os termos novos identificados durante a análise.
- **Arquivos alterados:** `docs/01-contexto.md`
- **Seção:** 01-contexto.md, Glossário e siglas

### <a id="rec-002"></a>REC-002 — Consolidar os vocabulários de status

- 🔄 **Alterado**
- **Problema:** Existem cinco vocabulários distintos (status de mudança no OpenSpec, status de run, veredito de revisão, status de resultado Codex para Dot e marcador NOT RUN) sem tabela de correspondência.
- **Justificativa:** Usar PASS, DONE e VALIDATED como sinônimos induz falsa conclusão, risco que o próprio framework combate.
- **Ação:** Tabela consolidada de vocabulários criada, com significado e onde cada um se aplica.
- **Arquivos alterados:** `docs/01-contexto.md`
- **Seção:** 01-contexto.md, Vocabulários de status

### <a id="rec-003"></a>REC-003 — Documentar a hierarquia entre as variantes do ciclo de vida

- 🔄 **Alterado**
- **Problema:** O ciclo de vida aparece em três versões (AGENTS.md com 10 etapas; design do bootstrap com 7 etapas; design de endurecimento com 15 etapas incluindo PR, CI, aprovação, merge e release).
- **Justificativa:** Sem hierarquia declarada, não está claro qual é normativa.
- **Ação:** Documentadas as três variantes com a regra de leitura (AGENTS.md normativo para o trabalho; demais como extensões de contexto) e diagrama do ciclo.
- **Arquivos alterados:** `docs/02-visao-geral.md`; `docs/anexos/diagramas/03-ciclo-de-vida.mmd`
- **Seção:** 02-visao-geral.md, Ciclo de vida do trabalho

### <a id="rec-004"></a>REC-004 — Harmonizar as variantes do ciclo de vida nos documentos de origem

- ⚠️ **Atenção (pendente)**
- **Problema:** Os documentos de origem continuam divergentes entre si; a hierarquia está apenas documentada na nova documentação.
- **Justificativa:** A fonte da verdade deveria declarar a hierarquia, e não só a documentação derivada.
- **Ação:** Proposta de marcar o ciclo do AGENTS.md como normativo e os demais como visões estendidas.
- **Arquivos alterados:** nenhum
- **Seção:** openspec/changes/bootstrap-agentic-engineering-team/design.md e openspec/changes/harden-engineering-dot/design.md
- **Motivo da pendência:** Altera documentos de design do OpenSpec, que são fontes normativas, e a instrução proíbe alterar o comportamento do sistema sem autorização específica.
- **Decisão ou informação necessária:** O mantenedor confirmar que o ciclo do AGENTS.md é o único normativo.
- **Próximo passo:** Abrir mudança OpenSpec que acrescente nota de hierarquia aos dois designs e reexecutar python scripts/validate.py.

### <a id="rec-005"></a>REC-005 — Atribuir identificadores estáveis e matriz de rastreabilidade

- 🔄 **Alterado**
- **Problema:** Apenas 24 requisitos têm identificador no OpenSpec (AGENT, AUTO, ORCH, PORT, QUAL), e o traceability.md da fonte cobre 22 deles (PORT-001 e PORT-003 ficaram sem cenário); as demais políticas (frescor, confiabilidade, dupla revisão, assurance, execução) não são rastreáveis a cenários ou critérios.
- **Justificativa:** Sem identificadores estáveis não há como relacionar regra, requisito, caso de uso e critério.
- **Ação:** Criados RF, RNF, RN, UC e CA com origem verificável e matriz regra x requisito x caso de uso x critério x fonte, gerada de um modelo único com verificador automático.
- **Arquivos alterados:** `docs/03-requisitos-funcionais.md`; `docs/05-regras-de-negocio.md`; `docs/06-casos-de-uso.md`; `docs/07-matriz-rastreabilidade.md`; `docs/anexos/build/modelo.py`
- **Seção:** 03, 05, 06 e 07

### <a id="rec-006"></a>REC-006 — Formalizar os requisitos posteriores como especificação OpenSpec

- ⚠️ **Atenção (pendente)**
- **Problema:** O diretório openspec/specs cobre só cinco capacidades originais; Atlas e Sentinel, endurecimento, garantia entre fornecedores, execução por CLI e contêineres não têm spec com identificadores.
- **Justificativa:** O README do OpenSpec determina acrescentar deltas de spec quando o comportamento muda.
- **Ação:** Os identificadores RF e RN desta documentação estão prontos para servir de base, mas não foram gravados em openspec/specs.
- **Arquivos alterados:** nenhum
- **Seção:** openspec/specs/
- **Motivo da pendência:** Gravar em openspec/specs altera artefatos normativos que governam o comportamento dos agentes.
- **Decisão ou informação necessária:** Aprovar a criação de uma mudança OpenSpec que importe os RF e RN como specs.
- **Próximo passo:** Criar openspec/changes/formalize-requirements com proposal, design, tasks e deltas de spec, e rodar os validadores.

### <a id="rec-007"></a>REC-007 — Atualizar a descrição dos validadores em docs/VALIDATION.md

- 🔄 **Alterado**
- **Problema:** O documento afirma que scripts/validate.py verifica apenas artefatos obrigatórios, frontmatter de skills e marcadores do AGENTS.md. Hoje ele também exige fixtures de execução e o status único dos manifests de run, e o CI roda também scripts/validate_hardening.py.
- **Justificativa:** Documentação desatualizada subestima o que o CI prova e o que ele não prova.
- **Ação:** Reescrita a descrição, incluindo o segundo validador, as checagens novas, o harness e os limites do que a validação estrutural prova.
- **Arquivos alterados:** `docs/VALIDATION.md`
- **Seção:** docs/VALIDATION.md

### <a id="rec-008"></a>REC-008 — Ligar o README à documentação completa

- 🔄 **Alterado**
- **Problema:** A lista Start here do README não referencia a documentação consolidada, a matriz de ambientes de execução, os runbooks de contêiner nem os relatórios de validação.
- **Justificativa:** Quem chega pelo README não encontra a documentação nem a evidência de validação.
- **Ação:** Acrescentados ao README links para docs/00-toc.md, docs/EXECUTION-ENVIRONMENTS.md, runbooks/CONTAINER-RUNTIMES.md e validation/FINAL-REPORT.md.
- **Arquivos alterados:** `README.md`
- **Seção:** README.md, Start here

### <a id="rec-009"></a>REC-009 — Alinhar o status das propostas OpenSpec ao estado das tarefas

- ⚠️ **Atenção (pendente)**
- **Problema:** A proposta bootstrap-agentic-engineering-team consta como PLANNED enquanto suas fases estáticas estão marcadas como concluídas, e adopt-dot-native-architecture consta como PLANNED enquanto seu tasks.md declara IN_PROGRESS.
- **Justificativa:** O vocabulário de status do OpenSpec (PLANNED, IN_PROGRESS, BLOCKED, VALIDATED, DONE) perde valor se os status divergem.
- **Ação:** Divergência documentada; nenhum status foi alterado.
- **Arquivos alterados:** nenhum
- **Seção:** openspec/changes/*/proposal.md
- **Motivo da pendência:** O status correto depende da decisão sobre o que conta como VALIDATED enquanto há tarefas ao vivo abertas, e o campo é metadado normativo.
- **Decisão ou informação necessária:** Definir o status de cada mudança (por exemplo, IN_PROGRESS enquanto houver validação ao vivo pendente).
- **Próximo passo:** Atualizar a linha Status das proposals após a decisão.

### <a id="rec-010"></a>REC-010 — Alinhar a precedência do POLICY-MANIFEST ao AGENTS.md

- ⚠️ **Atenção (pendente)**
- **Problema:** templates/POLICY-MANIFEST.yaml lista 6 níveis de precedência e omite os padrões gerais (nível 7 do AGENTS.md), além de usar nomes diferentes (por exemplo, native_platform_and_safety).
- **Justificativa:** O validador exige apenas que o primeiro item seja a plataforma nativa; o restante pode divergir sem detecção.
- **Ação:** Divergência documentada em 05-regras-de-negocio.md na regra RN-001; o template não foi alterado.
- **Arquivos alterados:** nenhum
- **Seção:** templates/POLICY-MANIFEST.yaml
- **Motivo da pendência:** O template é versionado por schema_version, e acrescentar um item é mudança MINOR que exige a política de migração.
- **Decisão ou informação necessária:** Aprovar a adição de general_defaults ao fim da lista.
- **Próximo passo:** Editar o template, incrementar governance_version e estender scripts/validate_hardening.py para comparar com o AGENTS.md.

### <a id="rec-011"></a>REC-011 — Alinhar o comando de validação do registro de projetos ao CI

- ⚠️ **Atenção (pendente)**
- **Problema:** templates/PROJECT-REGISTRY.yaml declara python scripts/validate.py como validação do projeto, mas o CI também roda scripts/validate_hardening.py e instala pyyaml.
- **Justificativa:** Quem seguir o registro executa menos verificações que o CI.
- **Ação:** Divergência documentada em 02-visao-geral.md; o template não foi alterado.
- **Arquivos alterados:** nenhum
- **Seção:** templates/PROJECT-REGISTRY.yaml
- **Motivo da pendência:** O template é versionado e consumido pelo Dot.
- **Decisão ou informação necessária:** Decidir se o registro lista um ou os dois comandos.
- **Próximo passo:** Atualizar o campo validation.command e registrar a dependência pyyaml.

### <a id="rec-012"></a>REC-012 — Registrar lacunas e propostas dos requisitos não funcionais

- 🔄 **Alterado**
- **Problema:** Não há metas definidas para desempenho, disponibilidade, escalabilidade e usabilidade.
- **Justificativa:** Requisito sem meta não é verificável; inventar metas seria falsificar a especificação.
- **Ação:** Lacunas registradas como tal, com valores observados reais e propostas marcadas como sujeitas à validação.
- **Arquivos alterados:** `docs/04-requisitos-nao-funcionais.md`
- **Seção:** 04-requisitos-nao-funcionais.md

### <a id="rec-013"></a>REC-013 — Aprovar e fixar metas numéricas dos requisitos não funcionais

- ⚠️ **Atenção (pendente)**
- **Problema:** As propostas de RNF-008 a RNF-011 aguardam aprovação.
- **Justificativa:** Sem decisão, os requisitos permanecem sem critério numérico.
- **Ação:** Propostas descritas em 04-requisitos-nao-funcionais.md.
- **Arquivos alterados:** nenhum
- **Seção:** 04-requisitos-nao-funcionais.md
- **Motivo da pendência:** As metas dependem de decisão do operador e de mais medições.
- **Decisão ou informação necessária:** Aprovar, ajustar ou descartar cada proposta.
- **Próximo passo:** Coletar mais execuções, fixar as metas no OpenSpec e acrescentar critérios de aceitação.

### <a id="rec-014"></a>REC-014 — Documentar o contrato HTTP consumido pelo transporte via GitHub

- 🔄 **Alterado**
- **Problema:** O sistema não expõe endpoint próprio, mas scripts/pr_chain.sh grava commit status pela API REST do GitHub sem contrato documentado.
- **Justificativa:** A interface consumida é a base do gate de revisão por SHA e deve ter contrato verificável.
- **Ação:** Criada a definição OpenAPI do trecho consumido (POST de commit status) e registrado que a API própria não existe.
- **Arquivos alterados:** `docs/anexos/swagger/github-commit-status.yaml`; `docs/anexos/swagger/README.md`
- **Seção:** 02-visao-geral.md, Dependências e integrações, e anexos/swagger

### <a id="rec-015"></a>REC-015 — Eliminar a dependência da conta OpenAI compartilhada entre Atlas e Sentinel

- ⚠️ **Atenção (pendente)**
- **Problema:** O Atlas e o Sentinel estão autenticados no mesmo usuário OpenAI (waiver W-001, validade até 2026-10-31), o que não comprova independência entre contas.
- **Justificativa:** A independência é premissa da arquitetura; sem ela, as revisões do Sentinel não são conclusivas sobre isolamento.
- **Ação:** Risco registrado nesta documentação e vinculado ao waiver W-001.
- **Arquivos alterados:** nenhum
- **Seção:** 08-observacoes-analises.md
- **Motivo da pendência:** Requer novo login interativo do operador numa segunda conta OpenAI.
- **Decisão ou informação necessária:** Fornecer a segunda conta ou renovar o waiver W-001.
- **Próximo passo:** Autenticar o sentinel-cli na segunda conta, verificar identidades distintas por hash do sub e reexecutar os cenários AS.

### <a id="rec-016"></a>REC-016 — Exigir os statuses de revisão por branch protection

- ⚠️ **Atenção (pendente)**
- **Problema:** Os statuses sentinel/review e argus/assurance são publicados, mas nada impede merge sem eles.
- **Justificativa:** Sem proteção de branch, o gate de revisão independente é apenas informativo.
- **Ação:** Nenhuma alteração feita nas configurações do repositório.
- **Arquivos alterados:** nenhum
- **Seção:** Configurações do repositório
- **Motivo da pendência:** Altera configurações do repositório, ação que exige autorização expressa e permissão de administração.
- **Decisão ou informação necessária:** Autorizar a regra de proteção da branch main.
- **Próximo passo:** Configurar required status checks para validate, sentinel/review e argus/assurance.

### <a id="rec-017"></a>REC-017 — Executar a validação ao vivo dos Dots e dos cenários restantes

- ⚠️ **Atenção (pendente)**
- **Problema:** Atlas e Sentinel como Dots, aprovação nativa, concorrência de leases, H01, H03 a H10 e AS07 não foram exercitados.
- **Justificativa:** Sem execução, o comportamento permanece INCONCLUSIVE e não pode ser marcado PASS.
- **Ação:** Lacuna registrada por requisito e caso de uso em 03-requisitos-funcionais.md e 06-casos-de-uso.md.
- **Arquivos alterados:** nenhum
- **Seção:** 03 e 06
- **Motivo da pendência:** Depende da criação dos Dots nas contas ChatGPT do operador.
- **Decisão ou informação necessária:** Instanciar o Atlas e o Sentinel conforme os runbooks.
- **Próximo passo:** Executar templates/DOT-LIVE-VALIDATION-RUNBOOK.md e preservar a evidência em validation/runs.

### <a id="rec-018"></a>REC-018 — Obter a tipografia principal da marca

- ⚠️ **Atenção (pendente)**
- **Problema:** A tipografia principal oficial é Neue Haas Grotesk (Adobe Fonts), indisponível neste ambiente.
- **Justificativa:** A regra pede seguir a identidade oficial sem inventar substituições.
- **Ação:** Os PDFs usam Manrope, a tipografia secundária oficial, como decisão técnica de apresentação, registrada como tal.
- **Arquivos alterados:** `docs/anexos/identidade/README.md`
- **Seção:** anexos/identidade/README.md
- **Motivo da pendência:** A fonte é licenciada pela Adobe e não está instalada na máquina.
- **Decisão ou informação necessária:** Fornecer a fonte licenciada ou aprovar o uso de Manrope.
- **Próximo passo:** Instalar Neue Haas Grotesk e regenerar os PDFs com python docs/anexos/build/exportar.py.

### <a id="rec-019"></a>REC-019 — Usar o logotipo oficial para fundo claro

- 🔄 **Alterado**
- **Problema:** Na primeira inspeção do diretório de identidade, o logotipo com texto grafite só aparecia como imagem rasterizada dentro do manual, e não como arquivo.
- **Justificativa:** Recriar o logotipo contraria a regra de usar somente a versão oficial; faltava um arquivo oficial para páginas claras.
- **Ação:** Inspeção completa do diretório localizou o arquivo oficial no template MODELO ATA DE REUNIÃO (DOCX); ele foi copiado sem alteração e usado nas páginas internas, junto com a padronagem clara oficial. A assinatura Powered by BBTS SkillTech do cabeçalho do template não foi usada. Os arquivos ficam apenas localmente e não são versionados (REC-022).
- **Arquivos alterados:** `docs/anexos/identidade/README.md`; `docs/anexos/identidade/hiveplace-logotipo-horizontal-fundo-claro.png`; `docs/anexos/identidade/padrao-hexagonos-claro.png`
- **Seção:** anexos/identidade/README.md

### <a id="rec-020"></a>REC-020 — Definir autoria e classificação documental

- ⚠️ **Atenção (pendente)**
- **Problema:** Nenhum artefato define o autor oficial nem a classificação dos documentos.
- **Justificativa:** A instrução proíbe inventar autoria e classificação.
- **Ação:** Registrado Não informado no front matter e nas capas.
- **Arquivos alterados:** `docs/00-toc.md`
- **Seção:** Front matter e capas
- **Motivo da pendência:** A informação não existe nos artefatos.
- **Decisão ou informação necessária:** Informar autor e classificação (por exemplo, a etiqueta interna usada nos materiais da marca).
- **Próximo passo:** Atualizar o front matter de todos os documentos e regenerar os PDFs.

### <a id="rec-021"></a>REC-021 — Instalar e configurar o Vale

- ⚠️ **Atenção (pendente)**
- **Problema:** O Vale não está instalado, e não há estilo oficial de Português do Brasil definido.
- **Justificativa:** A instrução pede conformidade com Vale ou ferramenta equivalente quando disponível.
- **Ação:** Executados markdownlint (formatação) e o verificador próprio de links, YAML e identificadores; a análise textual do Vale não foi executada.
- **Arquivos alterados:** nenhum
- **Seção:** 08-observacoes-analises.md, Verificações executadas
- **Motivo da pendência:** Não há binário nem configuração .vale.ini no ambiente.
- **Decisão ou informação necessária:** Escolher os estilos do Vale para Português do Brasil.
- **Próximo passo:** Instalar o Vale, adicionar .vale.ini e rodar sobre docs/.

### <a id="rec-022"></a>REC-022 — Manter ativos de marca e PDFs fora do repositório público

- 🔄 **Alterado**
- **Problema:** O repositório leandroclf/ai-engineering-team é público e os PNGs de identidade e os PDFs gerados embutem logotipo, símbolo e padronagens da HIVEPlace.
- **Justificativa:** Publicar material de marca de empresa em repositório pessoal público é decisão do operador, que optou por não publicá-lo.
- **Ação:** Os PNGs de identidade e todos os PDFs foram incluídos no .gitignore e permanecem só na máquina de origem; o README de identidade e os Markdown, que apenas descrevem a marca, são versionados. A documentação registra como regenerar os PDFs.
- **Arquivos alterados:** `.gitignore`; `docs/anexos/identidade/README.md`; `docs/00-toc.md`
- **Seção:** .gitignore e anexos/identidade

### <a id="rec-023"></a>REC-023 — Definir se o limite de retentativas conta tentativas totais ou adicionais

- ⚠️ **Atenção (pendente)**
- **Problema:** docs/DOT-RELIABILITY.md fixa "3 attempts" (tentativas) para falhas transitórias, enquanto templates/TASK-ENVELOPE.yaml usa o campo max_retries com valor 3 (retentativas). Com a primeira execução, 3 retentativas somam 4 tentativas.
- **Justificativa:** A fonte permite duas leituras com resultados diferentes no mesmo cenário (H04); escolher uma delas arbitrariamente alteraria o comportamento.
- **Ação:** Divergência documentada em RN-025 sem escolher uma leitura.
- **Arquivos alterados:** nenhum
- **Seção:** docs/DOT-RELIABILITY.md e templates/TASK-ENVELOPE.yaml
- **Motivo da pendência:** Os dois documentos são normativos e versionados, e a evidência disponível não indica a intenção.
- **Decisão ou informação necessária:** O mantenedor decidir se o limite é de tentativas totais ou de retentativas.
- **Próximo passo:** Alinhar o nome do campo ou o texto da política, incrementar a versão do template e cobrir com o cenário H04.

### <a id="rec-024"></a>REC-024 — Esclarecer o enquadramento de mudanças de dependência em R2

- ⚠️ **Atenção (pendente)**
- **Problema:** AGENTS.md e docs/SECURITY.md tratam dependências como R2; docs/workflows/dependency-change.md restringe a "mudanças materiais de dependências de runtime"; tests/scenarios.md (item 4) diz que mudança de dependência é no mínimo R2.
- **Justificativa:** Sem critério de materialidade, o mesmo ajuste pode ser classificado em R1 ou R2, mudando a exigência de revisão independente.
- **Ação:** Divergência documentada em RN-004 sem definir o critério.
- **Arquivos alterados:** nenhum
- **Seção:** docs/workflows/dependency-change.md
- **Motivo da pendência:** Definir materialidade é decisão de governança que altera a classificação de risco.
- **Decisão ou informação necessária:** Definir se toda mudança de dependência é R2 ou qual critério torna uma mudança material.
- **Próximo passo:** Atualizar o workflow e o AGENTS.md pela política de migração e acrescentar cenário de teste.

<!-- END:gerado:rec-detalhe -->

## Verificações executadas

<!-- BEGIN:gerado:verificacoes -->

Esta seção registra apenas o que foi **efetivamente executado**, com a ferramenta e o resultado. O que não foi executado está em "Não executado ou parcial".

### Executado

| Verificação | Ferramenta | Resultado |
| --- | --- | --- |
| Consistência cruzada entre regras, requisitos, casos de uso, critérios, recomendações e fontes: identificadores sem duplicidade nem lacunas, vínculos existentes, critério de cada caso de uso presente, Gherkin com Dado, Quando e Então, fontes e âncoras existentes nos arquivos, 24 identificadores originais do OpenSpec mapeados | `docs/anexos/build/modelo.py` | Aprovado: 52 RN, 30 RF, 12 RNF, 20 UC, 32 CA, 24 REC |
| Front matter YAML com título, autor, data e versão; links relativos e âncoras; imagens; identificadores citados nos textos; PDF correspondente de cada Markdown | `docs/anexos/build/verificar_docs.py` | Aprovado: 11 documentos, 1342 links relativos, 571 referências de identificador |
| Lint de Markdown, com MD013 desligada (tabelas e parágrafos longos), MD033 restrita a `a` e `br`, MD024 só entre títulos irmãos e MD041 desligada | `markdownlint-cli2` 0.23.3 (markdownlint 0.41.1) | Aprovado: 0 problemas em 11 arquivos. Uma primeira execução apontou mais de 40 ocorrências de MD022 (título logo após a linha da âncora), corrigidas no gerador |
| Contrato OpenAPI do GitHub consumido | `openapi-spec-validator` | Válido como OpenAPI 3.0.3 |
| Validadores do repositório com os arquivos novos presentes | `scripts/validate.py`, `scripts/validate_hardening.py` | Aprovados: 76 artefatos obrigatórios; contratos H01 a H10 |
| Renderização dos 7 diagramas | `mmdc` (Mermaid CLI) com Chrome | Sem erros; inspeção visual de cada PNG |
| Geração dos 11 PDFs | Chrome headless | 11 PDFs gerados; fontes Manrope, DejaVu Sans Mono e Noto Color Emoji embutidas; texto com acentos e emoji extraível; capa em retrato; documentos 04, 05 e 07 em página paisagem |

### Inspeção visual

Foram vistos em resolução legível: a capa e as páginas 2 e 3 do índice; a página 4 do contexto (glossário); a página 5 da visão geral (diagrama); a página 2 do 04; as páginas 3 e 11 do 05; a página 3 do 07; a página 15 do 06 (Gherkin); a página 12 do 08 (registro); e os sete diagramas. Todos os 11 documentos foram vistos em folhas de contato de baixa resolução.

Defeitos encontrados e **corrigidos** na inspeção:

- Diagramas: texto cortado nos nós (a fonte carregava depois da medição), rótulos de aresta invisíveis, ciclo de vida largo demais para ler, numeração de mensagens ilegível e ator sem nome no diagrama de sequência, arestas cruzando nós no diagrama de contêineres.
- PDFs: marca d'água no lugar errado, rodapé quebrado em duas linhas, nome do projeto quebrado no título da capa, palavras partidas ao meio em colunas estreitas, tabelas dos documentos 04, 05 e 07 estreitas demais em retrato, e linhas de texto longas demais em paisagem.

### Não executado ou parcial

- ⚠️ **Vale:** não está instalado e não há estilo de Português do Brasil definido; a análise textual não foi feita (REC-021). O `markdownlint` cobre formatação, não redação.
- ⚠️ **Inspeção parcial:** as páginas não listadas acima foram vistas apenas nas folhas de contato, em baixa resolução.
- ⚠️ **Outros leitores de PDF e o GitHub:** os PDFs foram verificados apenas pela extração de texto e por renderização do Chrome (`pdftoppm`); a renderização dos Markdown no GitHub não foi verificada, embora as âncoras sigam a regra de títulos do GitHub.
- ⚠️ **CI:** o resultado do CI do GitHub sobre estes arquivos não está registrado aqui, pois só existe depois da publicação.
- ⚠️ **Conformidade visual integral não declarada:** a tipografia principal da marca não estava disponível (REC-018), e a classificação documental não foi definida (REC-020).

### Efeitos no ambiente

Para executar as verificações e a exportação foram instalados fora do repositório: um ambiente virtual Python em `/tmp/docvenv` (markdown, pyyaml, openapi-spec-validator), a fonte Manrope em `~/.local/share/fonts` (necessária para os diagramas e os PDFs) e o cache do `npx` do `markdownlint-cli2`. Nenhuma dependência foi adicionada ao projeto.

<!-- END:gerado:verificacoes -->

## Conclusão

<!-- BEGIN:gerado:conclusao -->

A análise produziu 52 regras de negócio, 30 requisitos funcionais, 12 requisitos não funcionais, 20 casos de uso e 32 critérios de aceitação em Gherkin, todos rastreáveis entre si e a fontes verificáveis, além de sete diagramas, o contrato do GitHub consumido pelo transporte e a identidade visual aplicada aos PDFs.

**Implementado (10):** REC-001 (consolidar glossário e siglas do domínio); REC-002 (consolidar os vocabulários de status); REC-003 (documentar a hierarquia entre as variantes do ciclo de vida); REC-005 (atribuir identificadores estáveis e matriz de rastreabilidade); REC-007 (atualizar a descrição dos validadores em docs/VALIDATION.md); REC-008 (ligar o README à documentação completa); REC-012 (registrar lacunas e propostas dos requisitos não funcionais); REC-014 (documentar o contrato HTTP consumido pelo transporte via GitHub); REC-019 (usar o logotipo oficial para fundo claro); REC-022 (manter ativos de marca e PDFs fora do repositório público).

**Pendente (14), com motivo, decisão e próximo passo em cada item:** REC-004, REC-006, REC-009, REC-010, REC-011, REC-013, REC-015, REC-016, REC-017, REC-018, REC-020, REC-021, REC-023, REC-024. Nenhuma pendência é apresentada como concluída. As mais relevantes para a confiança no sistema são a independência real entre as contas do Atlas e do Sentinel (REC-015), a validação ao vivo dos Dots (REC-017) e a exigência dos statuses de revisão por proteção de branch (REC-016).

**Todas as recomendações aplicáveis foram implementadas e registradas. As pendências estão documentadas com seus motivos e próximos passos.**

<!-- END:gerado:conclusao -->

## Registro de implementação das recomendações

<!-- BEGIN:gerado:rec-registro -->

| Recomendação | Arquivo(s) Alterado(s) | Seção | Status |
| --- | --- | --- | --- |
| [REC-001](08-observacoes-analises.md#rec-001) Consolidar glossário e siglas do domínio | `docs/01-contexto.md` | 01-contexto.md, Glossário e siglas | Aplicada |
| [REC-002](08-observacoes-analises.md#rec-002) Consolidar os vocabulários de status | `docs/01-contexto.md` | 01-contexto.md, Vocabulários de status | Aplicada |
| [REC-003](08-observacoes-analises.md#rec-003) Documentar a hierarquia entre as variantes do ciclo de vida | `docs/02-visao-geral.md`<br>`docs/anexos/diagramas/03-ciclo-de-vida.mmd` | 02-visao-geral.md, Ciclo de vida do trabalho | Aplicada |
| [REC-004](08-observacoes-analises.md#rec-004) Harmonizar as variantes do ciclo de vida nos documentos de origem | Nenhum | openspec/changes/bootstrap-agentic-engineering-team/design.md e openspec/changes/harden-engineering-dot/design.md | Pendente |
| [REC-005](08-observacoes-analises.md#rec-005) Atribuir identificadores estáveis e matriz de rastreabilidade | `docs/03-requisitos-funcionais.md`<br>`docs/05-regras-de-negocio.md`<br>`docs/06-casos-de-uso.md`<br>`docs/07-matriz-rastreabilidade.md`<br>`docs/anexos/build/modelo.py` | 03, 05, 06 e 07 | Aplicada |
| [REC-006](08-observacoes-analises.md#rec-006) Formalizar os requisitos posteriores como especificação OpenSpec | Nenhum | openspec/specs/ | Pendente |
| [REC-007](08-observacoes-analises.md#rec-007) Atualizar a descrição dos validadores em docs/VALIDATION.md | `docs/VALIDATION.md` | docs/VALIDATION.md | Aplicada |
| [REC-008](08-observacoes-analises.md#rec-008) Ligar o README à documentação completa | `README.md` | README.md, Start here | Aplicada |
| [REC-009](08-observacoes-analises.md#rec-009) Alinhar o status das propostas OpenSpec ao estado das tarefas | Nenhum | openspec/changes/*/proposal.md | Pendente |
| [REC-010](08-observacoes-analises.md#rec-010) Alinhar a precedência do POLICY-MANIFEST ao AGENTS.md | Nenhum | templates/POLICY-MANIFEST.yaml | Pendente |
| [REC-011](08-observacoes-analises.md#rec-011) Alinhar o comando de validação do registro de projetos ao CI | Nenhum | templates/PROJECT-REGISTRY.yaml | Pendente |
| [REC-012](08-observacoes-analises.md#rec-012) Registrar lacunas e propostas dos requisitos não funcionais | `docs/04-requisitos-nao-funcionais.md` | 04-requisitos-nao-funcionais.md | Aplicada |
| [REC-013](08-observacoes-analises.md#rec-013) Aprovar e fixar metas numéricas dos requisitos não funcionais | Nenhum | 04-requisitos-nao-funcionais.md | Pendente |
| [REC-014](08-observacoes-analises.md#rec-014) Documentar o contrato HTTP consumido pelo transporte via GitHub | `docs/anexos/swagger/github-commit-status.yaml`<br>`docs/anexos/swagger/README.md` | 02-visao-geral.md, Dependências e integrações, e anexos/swagger | Aplicada |
| [REC-015](08-observacoes-analises.md#rec-015) Eliminar a dependência da conta OpenAI compartilhada entre Atlas e Sentinel | Nenhum | 08-observacoes-analises.md | Pendente |
| [REC-016](08-observacoes-analises.md#rec-016) Exigir os statuses de revisão por branch protection | Nenhum | Configurações do repositório | Pendente |
| [REC-017](08-observacoes-analises.md#rec-017) Executar a validação ao vivo dos Dots e dos cenários restantes | Nenhum | 03 e 06 | Pendente |
| [REC-018](08-observacoes-analises.md#rec-018) Obter a tipografia principal da marca | `docs/anexos/identidade/README.md` | anexos/identidade/README.md | Pendente |
| [REC-019](08-observacoes-analises.md#rec-019) Usar o logotipo oficial para fundo claro | `docs/anexos/identidade/README.md`<br>`docs/anexos/identidade/hiveplace-logotipo-horizontal-fundo-claro.png`<br>`docs/anexos/identidade/padrao-hexagonos-claro.png` | anexos/identidade/README.md | Aplicada |
| [REC-020](08-observacoes-analises.md#rec-020) Definir autoria e classificação documental | `docs/00-toc.md` | Front matter e capas | Pendente |
| [REC-021](08-observacoes-analises.md#rec-021) Instalar e configurar o Vale | Nenhum | 08-observacoes-analises.md, Verificações executadas | Pendente |
| [REC-022](08-observacoes-analises.md#rec-022) Manter ativos de marca e PDFs fora do repositório público | `.gitignore`<br>`docs/anexos/identidade/README.md`<br>`docs/00-toc.md` | .gitignore e anexos/identidade | Aplicada |
| [REC-023](08-observacoes-analises.md#rec-023) Definir se o limite de retentativas conta tentativas totais ou adicionais | Nenhum | docs/DOT-RELIABILITY.md e templates/TASK-ENVELOPE.yaml | Pendente |
| [REC-024](08-observacoes-analises.md#rec-024) Esclarecer o enquadramento de mudanças de dependência em R2 | Nenhum | docs/workflows/dependency-change.md | Pendente |

<!-- END:gerado:rec-registro -->

### Alterações em artefatos existentes

Apenas `README.md` e `docs/VALIDATION.md` já existiam e foram alterados (REC-007 e REC-008). Diff aplicado:

<!-- BEGIN:gerado:diffs -->

```diff
diff --git a/README.md b/README.md
index 4deb644..278344e 100644
--- a/README.md
+++ b/README.md
@@ -8,6 +8,7 @@ Human -> Engineering Dot -> versioned governance -> Codex / Work / Plugins -> ta
 The Dot is the persistent coordinator. Codex is the default executor for repository engineering. Work handles deep research/artifact-heavy work. Plugins perform narrow external actions under native permissions. This repository owns portable OpenSpec, AGENTS rules, Skills, project adapters, quality gates, reliability/security controls, delegation contracts and validation.
 
 ## Start here
+- `docs/00-toc.md` (consolidated documentation: requirements, business rules, use cases, traceability)
 - `docs/DOT-NATIVE-ARCHITECTURE.md`
 - `docs/DOT-RELIABILITY.md`
 - `docs/CONTEXT-FRESHNESS.md`
@@ -19,6 +20,9 @@ The Dot is the persistent coordinator. Codex is the default executor for reposit
 - `templates/TASK-ENVELOPE.yaml`
 - `templates/PROJECT-REGISTRY.yaml`
 - `openspec/changes/harden-engineering-dot/`
+- `docs/EXECUTION-ENVIRONMENTS.md`
+- `runbooks/CONTAINER-RUNTIMES.md`
+- `validation/FINAL-REPORT.md`
 
 ## Skills
 Core: tech-lead, architect, backend, qa, security, code-review, observability.
diff --git a/docs/VALIDATION.md b/docs/VALIDATION.md
index e535d61..426d353 100644
--- a/docs/VALIDATION.md
+++ b/docs/VALIDATION.md
@@ -1,6 +1,16 @@
 # Validation Strategy
-The repository uses a lightweight executable validator because the framework is primarily declarative Markdown.
+The repository uses lightweight executable validators because the framework is primarily declarative Markdown.
 
-`python scripts/validate.py` checks mandatory artifacts, Skill frontmatter and core AGENTS contract markers. GitHub Actions runs it on pushes and pull requests.
+`python scripts/validate.py` checks mandatory artifacts, Skill frontmatter, core AGENTS contract markers, the provider-execution fixtures, and that every `validation/runs/*/manifest.yaml` carries exactly one allowed status (PASS, FAIL, BLOCKED or INCONCLUSIVE).
 
-Scenario-level validation is defined in `tests/scenarios.md`. Behavioral benchmarking against live Codex executions requires a Codex runtime and is intentionally reported separately from static repository validation; it must never be marked passing without execution evidence.
+`python scripts/validate_hardening.py` checks the hardening contracts: required policy tokens, YAML validity of the task envelope, lease, evidence record, policy manifest and project registry, required envelope and lease fields, native-safeguard precedence in the policy manifest, and the H01-H10 scenario list.
+
+GitHub Actions runs both validators on pushes and pull requests (`.github/workflows/validate.yml`, Python 3.12 with PyYAML installed by `pip install pyyaml`).
+
+## What structural validation proves
+Artifacts exist, parse and satisfy the checked constraints. It does not prove agent behavior, live Dot behavior, native approvals or independence between accounts. A green CI run must never be reported as behavioral validation.
+
+## Behavioral validation
+Scenario-level validation is defined in `tests/scenarios.md` and the scenario files under `validation/`. Runs execute through the provider CLIs with `scripts/provider_run.py` in disposable clones, normally inside the per-account containers described in `runbooks/CONTAINER-RUNTIMES.md`. Evidence is preserved under `validation/runs/<run-id>/`. `scripts/pr_chain.sh` exercises the Atlas -> Sentinel -> Argus chain over GitHub pull requests and CI. Results are summarized in `validation/FINAL-REPORT.md` and the per-agent reports.
+
+Behavioral benchmarking requires a live provider runtime and is reported separately from static validation; it must never be marked passing without execution evidence.
```

<!-- END:gerado:diffs -->
