# Skill marketplace

Este diretório contém pacotes de orientação reutilizáveis para trabalho de engenharia. O catálogo em [`catalog.yaml`](catalog.yaml) é a fonte de descoberta e compatibilidade; o `SKILL.md` de cada pacote é a fonte do procedimento.

Uma skill publicada precisa ter identidade estável, versão semântica, categoria, maturidade, compatibilidade, dependências explícitas, risco, contrato de entrada/saída, limites de autoridade e validação. O catálogo descreve o pacote sem substituir as regras do `AGENTS.md`, as aprovações nativas ou o OpenSpec do projeto consumidor.

## Ciclo de publicação

1. Criar ou alterar a skill em seu diretório, preservando o `SKILL.md` como entrada.
2. Atualizar o item correspondente em `catalog.yaml`, incrementando a versão de acordo com o impacto.
3. Descrever exemplos, evidências e limitações no `SKILL.md`.
4. Executar `python scripts/validate_skills.py` e a suíte do repositório.
5. Publicar por branch/PR, revisar segurança e compatibilidade e observar CI.
6. Promover `experimental` para `beta` ou `stable` somente com evidência de uso e sem findings críticos/altos pendentes.

O catálogo é um marketplace interno versionado. Ele não instala skills automaticamente, não concede permissões e não certifica que um agente seguirá o procedimento. Distribuições externas devem gerar um artefato imutável e manter checksum, licença e proveniência fora do prompt.

## Seleção

O Tech Lead deve selecionar somente skills que contribuam para o objetivo. A categoria facilita descoberta; `requires` e `composes_with` descrevem dependências operacionais, não uma obrigação de invocar toda a árvore. Skills de tecnologia são opcionais e só entram quando o repositório confirma aquela stack.
