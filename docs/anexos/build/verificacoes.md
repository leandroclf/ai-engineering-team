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
