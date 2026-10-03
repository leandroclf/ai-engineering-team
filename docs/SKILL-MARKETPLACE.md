# Skill marketplace para produção

O marketplace atual é um catálogo versionado no próprio repositório. Ele organiza descoberta e composição sem criar um serviço adicional. Cada skill continua sendo carregada sob demanda e o Tech Lead escolhe apenas as capacidades úteis à tarefa.

## Contrato de publicação

| Campo | Finalidade |
| --- | --- |
| `id` e `path` | Identidade estável e localização do pacote |
| `version` | Evolução SemVer do comportamento/documentação |
| `status` | `experimental`, `beta`, `stable` ou `deprecated` |
| `category` e `tags` | Descoberta semântica |
| `requires` e `composes_with` | Dependências e colaboração explícitas |
| `supported_surfaces` | Codex, Dot ou `local-ai-team` compatíveis |
| `risk` | Risco operacional máximo esperado |
| `inputs` e `outputs` | Contrato de uso e evidência produzida |
| `quality_gates` | Critérios mínimos para aceitar o resultado |

O `SKILL.md` precisa conter as seções `Inputs`, `Outputs`, `Boundaries` e `Validation`. O catálogo não substitui AGENTS, OpenSpec, permissões nativas ou aprovação R3. Uma skill pode orientar um processo, mas não prova que o agente o executou.

## Maturidade e promoção

- `experimental`: contrato incompleto ou evidência inicial; uso controlado.
- `beta`: contrato validado e testado em cenários limitados; riscos conhecidos registrados.
- `stable`: uso repetido, revisão de segurança, compatibilidade documentada e ausência de findings críticos/altos abertos.
- `deprecated`: não usar em novos trabalhos; manter migração e motivo.

Toda publicação passa por branch/PR, `python scripts/validate_skills.py`, testes pertinentes, revisão de segurança e CI. Mudanças incompatíveis incrementam a versão major. Mudanças de orientação que alteram resultados incrementam minor; correções textuais sem alteração de contrato incrementam patch.

## Produção e futuro registry

Para distribuição externa, o artefato precisa ser imutável, ter proveniência, checksum, licença compatível, compatibilidade de superfície, política de revogação e instalação com menor privilégio. A implementação atual não instala pacotes automaticamente e não concede acesso a ferramentas. Essa contenção é necessária porque um marketplace de skills pode distribuir instruções com efeitos sobre código, dados e credenciais.
