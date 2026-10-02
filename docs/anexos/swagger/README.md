---
titulo: "Contratos de API"
projeto: "ai-engineering-team"
autor: "Não informado"
data: "2026-10-01"
versao: "1.0.0"
classificacao: "Não informada"
status: "Rascunho para revisão"
---

# Contratos de API

O ai-engineering-team **não expõe endpoints próprios**: é um framework de governança declarativa com scripts de validação e orquestração local. Por isso não há Swagger da API do sistema.

A única chamada HTTP explícita do código é a publicação de commit status do GitHub em `scripts/pr_chain.sh`. Ela está documentada como contrato **consumido**:

| Arquivo | Conteúdo | Natureza |
| --- | --- | --- |
| [github-commit-status.yaml](github-commit-status.yaml) | `POST /repos/{owner}/{repo}/statuses/{sha}` | Recorte de contrato de terceiro, derivado do uso. A documentação oficial do GitHub prevalece |

Outras chamadas ao GitHub (`gh pr create`, `gh pr comment`, `gh pr close`, `gh run list`) passam pela CLI `gh` e não foram descritas, porque o script não emite requisições HTTP explícitas para elas.

Verificação: estrutura do YAML lida e validada como OpenAPI (ver [08-observacoes-analises.md](../../08-observacoes-analises.md), Verificações executadas).
