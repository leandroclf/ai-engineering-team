---
titulo: "Identidade visual aplicada à documentação"
projeto: "ai-engineering-team"
autor: "Não informado"
data: "2026-10-01"
versao: "1.0.0"
classificacao: "Não informada"
status: "Rascunho para revisão"
---

# Identidade visual aplicada à documentação

Este anexo registra quais insumos da identidade visual HIVEPlace foram usados nos PDFs e diagramas, de onde vieram e o que foi decisão técnica de apresentação. Nada aqui declara conformidade integral com a marca: as pendências estão na seção [Pendências](#pendências).

## Fonte oficial inspecionada

Diretório: `/home/leandro/Imagens/logos/Identidade Visual` (caminho da máquina de origem; nenhum arquivo da documentação depende dele).

| Arquivo | Como foi inspecionado | Conteúdo relevante |
| --- | --- | --- |
| Guia Rapido de Marca- HIVE (PDF, 13 páginas) | Texto extraído e as 8 primeiras páginas vistas como imagem | Significado da marca, regras do logotipo, elementos gráficos, cores, tipografia, tom de voz |
| Guia Rapido de Marca- HIVE (PPTX) | Mídia embutida extraída e identificada | Logotipo, símbolo, padronagens e fontes embutidas |
| [Hive] Identidade Visual_V.3 (PDF, 24 páginas) | Texto extraído; páginas de logotipo, paleta e aplicações vistas | Padronagem, logotipo, paleta com valores hexadecimais, tipografia e aplicações |
| [HivePlace] Identidade Verbal_v1.1 - Cliente (PDF, 44 páginas) | Texto extraído das primeiras páginas (tom de voz e discurso) | Tom de voz "Visionário Soberano": preciso, pragmático, sem jargões vazios |
| [Hiveplace] Apresentação_Institucional (PPTX, 37 lâminas) | Convertido em PDF; 20 lâminas vistas em miniatura; texto das demais pesquisado por termos de marca, sem achados | Uso da paleta em apresentações: fundos escuros e claros, destaque dourado |
| MODELO ATA DE REUNIÃO (DOCX) | Convertido em PDF, página vista como imagem; XML e mídia extraídos | Único template de documento: página clara, filete de cabeçalho, padronagem clara, rodapé com logotipo e frase da marca |

Limite da inspeção: as 17 lâminas restantes da apresentação institucional e as páginas 4 a 44 da identidade verbal não foram vistas como imagem.

## O que veio dos materiais oficiais

| Elemento | Valor ou arquivo | Origem |
| --- | --- | --- |
| Logotipo horizontal para fundo escuro (texto branco, transparente) | `hiveplace-logotipo-horizontal.png` (2048 x 513) | Mídia do PPTX do guia rápido (`image2.png`) |
| Logotipo horizontal para fundo claro (texto grafite, fundo branco) | `hiveplace-logotipo-horizontal-fundo-claro.png` (994 x 280) | Mídia do template MODELO ATA DE REUNIÃO (`image3.png`), usado ali no rodapé |
| Símbolo isolado (dourado, transparente) | `hiveplace-simbolo.png` (1255 x 1455) | Mídia do PPTX do guia rápido (`image4.png`) |
| Padronagem hexagonal para fundo escuro | `padrao-hexagonos-a.png` e `padrao-hexagonos-b.png` | Mídia do PPTX do guia rápido (`image1.png`, `image3.png`) |
| Padronagem hexagonal para fundo claro | `padrao-hexagonos-claro.png` | Mídia do template de ata (`image2.png`) |
| Paleta | `#0D0D0E`, `#332528`, `#EFB41B`, `#D98E06`, `#5D2E07`, `#1A1214`, `#1A1A1C`, `#404146`, `#EEF1F0` | Página de paleta do manual V.3 |
| Tipografia secundária | Manrope (Google Fonts) | Guia rápido e manual V.3 |
| Frase de rodapé | Transformando conexões invisíveis em inteligência coletiva | Rodapé do template de ata |
| Regras do logotipo | Usar sempre a versão oficial; não alterar cores, não distorcer, não aplicar sombras, não criar novas versões | Guia rápido, página de logotipo |
| Uso do dourado | Destacar informações importantes sem competir com o restante da composição | Guia rápido, página de cores |

Soma de verificação (SHA-256) dos arquivos copiados:

```text
06b840760ba9dfcddd72b90314ecdeee6026f7de3b09b9927ce5c6a6972c9f45  hiveplace-logotipo-horizontal.png
7a3e3bf1f5326052caaebf12897190cf9bf44088502bd9c69ab6d50b42e1648f  hiveplace-logotipo-horizontal-fundo-claro.png
9cd0db15916ba0cb92e388cb9c5c1f1e9c56a15ac6b4e994e5a31939cfd984b7  hiveplace-simbolo.png
6a61e3e3ac8c65252f42fe40654dd3cf63a8036f924526eb36dfe8c467b68021  padrao-hexagonos-a.png
371636310986cf014d82ff425a46e5f33f084891c6a558588d41edbe4d4e60ea  padrao-hexagonos-b.png
109517446d36f418ae7f79c47df2efb66d3d6fdd1ecdd7f6b323863a60bc64b3  padrao-hexagonos-claro.png
```

Os arquivos não foram redimensionados, recoloridos nem redesenhados. **Eles não são versionados neste repositório:** por serem material de marca e o repositório ser público, os PNGs e os PDFs gerados ficam apenas na máquina de origem (ignorados pelo Git). Para regenerar os PDFs, copie os arquivos listados acima para esta pasta, a partir do diretório oficial de identidade. O cabeçalho do template de ata usa o logotipo com o selo "Powered by BBTS SkillTech", que é uma assinatura de parceiros. Ela **não** foi usada, para não sugerir endosso de terceiros.

## Como a identidade foi aplicada

| Artefato | Aplicação |
| --- | --- |
| Capa do PDF | Fundo `#332528` com padronagem hexagonal oficial, logotipo branco oficial, título em branco e destaque dourado `#EFB41B` |
| Páginas internas | Página branca, como no template de ata. Cabeçalho com o logotipo para fundo claro, título e versão do documento, e filete. Padronagem clara oficial no canto inferior direito. Rodapé com o símbolo, a frase da marca e a numeração |
| Títulos e tabelas | Títulos em `#332528` com filete dourado; cabeçalho de tabela `#332528` com texto `#EEF1F0`; linhas alternadas em `#EEF1F0` |
| Diagramas | Nós `#332528` com borda `#EFB41B`, decisões em dourado, linhas `#404146`, fundo `#EEF1F0` |

## Decisões técnicas de apresentação

Estas escolhas não vêm de uma definição oficial; foram adotadas porque os insumos não cobrem o caso.

- Tipografia Manrope em todos os textos, por falta da fonte principal.
- Texto do corpo em `#1A1214`, para legibilidade de documentos longos.
- Margens, espaçamentos e escala tipográfica do PDF.
- Cores das caixas de atenção, confirmação e alteração, derivadas da paleta.
- Fundo `#EEF1F0` nos diagramas, para que as cores dos nós mantenham contraste.
- O tom dos textos segue a identidade verbal em termos gerais: frases diretas, sem adjetivação vazia.

## Pendências

- **Tipografia principal:** Neue Haas Grotesk (Adobe Fonts) não está disponível neste ambiente. Os PDFs usam Manrope. Ver REC-018 em [08-observacoes-analises.md](../../08-observacoes-analises.md).
- **Publicação:** decidida pelo operador. Ativos de marca e PDFs não são publicados no repositório. Ver REC-022.
- **Classificação documental:** os materiais usam etiquetas como `#interna` e `#pública`, mas não definem a classificação desta documentação. Ver REC-020.
- **Inspeção parcial:** ver o limite na primeira seção.
