---
titulo: "Documentação técnica do ai-engineering-team"
projeto: "ai-engineering-team"
autor: "Não informado"
data: "2026-10-01"
versao: "1.0.0"
classificacao: "Não informada"
status: "Rascunho para revisão"
---

# Documentação técnica do ai-engineering-team

## Identificação do documento

| Campo | Valor |
| --- | --- |
| Projeto | ai-engineering-team |
| Conjunto | Análise de requisitos e documentação técnica |
| Autor | Não informado |
| Data | 2026-10-01 |
| Versão | 1.0.0 |
| Classificação | Não informada |
| Status | Rascunho para revisão |
| Revisão do repositório analisada | `791ac89` (branch `main`) |

O autor e a classificação não constam nos artefatos analisados e não foram inventados (REC-020). Esta documentação foi produzida por análise assistida por IA a pedido do operador, sem aprovação humana de conteúdo registrada.

## Índice

| Documento | Conteúdo | Seções pedidas |
| --- | --- | --- |
| [00-toc.md](00-toc.md) | Este índice, identificação, escopo analisado e limitações | 3.1 |
| [01-contexto.md](01-contexto.md) | Sumário executivo, contexto e justificativa, glossário e siglas, vocabulários de status | 3.2, 3.3, 3.4 |
| [02-visao-geral.md](02-visao-geral.md) | Arquitetura, tecnologias, componentes, ciclo de vida, protótipos, dependências e integrações | 3.5, 3.10, 3.13 |
| [03-requisitos-funcionais.md](03-requisitos-funcionais.md) | Requisitos funcionais RF-001 a RF-030 | 3.6 |
| [04-requisitos-nao-funcionais.md](04-requisitos-nao-funcionais.md) | Requisitos não funcionais RNF-001 a RNF-012, lacunas e propostas | 3.7 |
| [05-regras-de-negocio.md](05-regras-de-negocio.md) | Regras RN-001 a RN-052, tabela-resumo, divergências | 3.8 |
| [06-casos-de-uso.md](06-casos-de-uso.md) | Casos de uso UC-001 a UC-020 e critérios de aceitação em Gherkin | 3.9, 3.12 |
| [07-matriz-rastreabilidade.md](07-matriz-rastreabilidade.md) | Regra x requisito x caso de uso x critério x fonte | 3.11 |
| [08-observacoes-analises.md](08-observacoes-analises.md) | Observações, recomendações, verificações, conclusão e registro de implementação | 3.14, 3.15, 3.16 |

Anexos:

| Anexo | Conteúdo |
| --- | --- |
| [anexos/diagramas/](anexos/diagramas/) | Sete diagramas em PNG, com fonte Mermaid editável (`.mmd`) e configuração de tema |
| [anexos/swagger/](anexos/swagger/) | Contrato consumido do GitHub (commit status) e nota sobre a ausência de API própria |
| [anexos/identidade/](anexos/identidade/) | Registro de origem, uso, decisões e pendências da identidade visual (os arquivos de imagem não são versionados) |
| [anexos/build/](anexos/build/) | Modelo de rastreabilidade, verificador, gerador de seções e exportador de PDF |

## Escopo analisado

Os **157 arquivos versionados** fora de `validation/runs/`, na revisão `791ac89`, foram lidos. O diretório `validation/runs/` (104 runs com manifest em 107 diretórios, 18 MB) foi tratado como **dados**: o status de todos os manifests foi agregado, e os relatórios e eventos foram lidos individualmente apenas dos runs que sustentam as conclusões desta documentação.

| Área | Arquivos | Tratamento |
| --- | --- | --- |
| Raiz (`AGENTS.md`, `README.md`) | 2 | Lidos |
| `openspec/` | 31 | Lidos: visão do projeto, roadmap, 5 specs e 6 mudanças |
| `docs/` | 36 | Lidos: 29 documentos, 6 fluxos de trabalho e 1 ADR |
| `skills/` | 13 | Lidos |
| `templates/` | 23 | Lidos |
| `runbooks/` | 4 | Lidos |
| `validation/` (exceto `runs/`) | 39 | Lidos: cenários, relatórios, waivers e fixtures |
| `scripts/` | 4 | Lidos |
| `runtimes/`, `tests/`, `.github/` | 4 | Lidos |
| `validation/runs/` | 628 arquivos | Dados: agregados e amostrados, como descrito acima |

Exclusões e limites:

- Não foi analisado nenhum repositório alvo gerenciado pelo Dot: não há nenhum no escopo.
- Não foram analisados o histórico Git completo nem as execuções do CI além do resultado de cada commit conferido.
- O comportamento de Dots ao vivo **não foi observado**: toda afirmação sobre ele é de especificação.
- Este projeto não tem código-fonte de aplicação. Os scripts são de validação e orquestração; "classes, métodos e funções" correspondem aos artefatos e scripts acima.

## Método

1. Inspeção dos insumos de identidade visual (ver [anexos/identidade/README.md](anexos/identidade/README.md)).
2. Leitura dos artefatos, extração das regras com fonte (arquivo e seção) e dos requisitos já identificados.
3. Modelagem única de rastreabilidade em YAML (`anexos/build/modelo-*.yaml`), com verificador que confere identificadores, vínculos e fontes.
4. Geração das tabelas e da matriz a partir do modelo, mantendo o texto restante escrito à mão.
5. Detecção de lacunas e divergências, registradas como recomendações com problema, justificativa e ação.
6. Aplicação imediata das recomendações que dependiam só de documentação descritiva; registro de pendência para as demais.
7. Verificações e exportação (ver [08](08-observacoes-analises.md), seção Verificações executadas).

## Convenções

- Identificadores com três dígitos: RN, RF, RNF, UC, CA e REC. Os identificadores originais do OpenSpec (AGENT, AUTO, ORCH, PORT, QUAL) foram preservados e mapeados em [03](03-requisitos-funcionais.md).
- **Comprovado**, **inferido** e **proposto** são distinguidos: tudo que é comprovado cita arquivo e seção; interpretações são marcadas como tal; metas sem base são propostas sujeitas à validação.
- Marcadores: ⚠️ **Atenção**, ✅ **Confirmado** e 🔄 **Alterado**.
- PDFs: cada `.md` gera um `.pdf` com identidade visual HIVEPlace. Os PDFs e os ativos de marca **não são versionados** (repositório público); são gerados localmente com `exportar.py` (ver REC-022 em [08](08-observacoes-analises.md)).

## Como regenerar

```text
python docs/anexos/build/modelo.py      # verifica a consistência cruzada
python docs/anexos/build/gerar.py       # preenche os blocos gerados nos Markdown
python docs/anexos/build/exportar.py    # gera os PDFs
```

O exportador exige Google Chrome, as bibliotecas Python `markdown` e `pyyaml`, e a fonte Manrope instalada. Os diagramas exigem `mmdc` (Mermaid CLI); os comandos estão em `anexos/diagramas/`.
