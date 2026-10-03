# Benchmarks para skills e agentes

## Situação da pesquisa

Não existe ainda um padrão único de mercado para medir uma skill isoladamente. Os benchmarks mais úteis medem camadas diferentes: impacto de conhecimento procedural, resolução de engenharia, uso de ferramentas e falhas de execução. Comparar seus números diretamente seria incorreto.

## Matriz de referência

| Benchmark | O que mede | Uso no marketplace | Limitação |
| --- | --- | --- | --- |
| [SkillsBench](https://arxiv.org/abs/2602.12670) | Ganho de tarefas com skill curada, sem skill ou skill gerada | Benchmark primário para ablação de skills e granularidade de módulos | Tarefas/domínios e protocolo externo; requer adaptação para nossas skills |
| [SWE-bench](https://www.swebench.com/) | Correção de issues reais de software por testes do repositório | Mede resultado de skills de engenharia em tarefas reais | Avalia o agente completo, modelo, ferramentas e ambiente, não a skill isolada |
| [GTA](https://arxiv.org/abs/2407.08713) | Seleção e execução de cadeias de ferramentas em tarefas reais | Mede se a skill escolhe, encadeia e interpreta ferramentas | Não é específico para engenharia e possui custo operacional maior |
| [ToolFailBench](https://arxiv.org/abs/2607.04686) | Omissão, uso indevido, fabricação e uso desnecessário de ferramentas | Diagnóstico de falhas de skills com ferramentas | Benchmark recente; resultados dependem dos juízes e ambientes |
| [General AgentBench](https://arxiv.org/abs/2602.18998) | Agentes gerais em busca, código, raciocínio e ferramentas | Mede composição de várias skills e degradação por contexto | Não identifica sozinho qual skill causou a falha |
| `internal-contract-v1` | Tarefas determinísticas do catálogo com baseline e skill | Gate obrigatório e barato no CI | Mede contratos definidos por nós; não substitui validação externa |

## Métricas adotadas

Cada experimento deve registrar a condição `baseline`, `skill` ou `skill-composition`, o modelo/provedor, a versão da skill, a revisão do repositório, o número de tentativas e o custo observável. Os indicadores mínimos são:

- taxa de conclusão verificável;
- delta contra baseline sem skill;
- regressão e variação entre repetições;
- chamadas de ferramentas necessárias, desnecessárias e ignoradas;
- falhas de contrato e de segurança;
- tempo, tokens e custo quando o provedor expuser esses dados;
- qualidade da evidência produzida e manutenção após mudança de versão.

Uma skill não pode ser promovida por uma única taxa de sucesso. A promoção exige ganho repetido, ausência de regressão crítica, limites conhecidos e revisão de segurança. Resultados sem verificador determinístico são `INCONCLUSIVE`.

## Execução no projeto

O catálogo executável está em [`evaluation/benchmarks.yaml`](../evaluation/benchmarks.yaml) e as tarefas internas em [`evaluation/tasks/`](../evaluation/tasks/). O validador verifica contratos e referências offline. A execução real de modelos e benchmarks externos exige o ambiente do provedor, suas licenças e evidência preservada; CI estrutural não pode declarar desempenho de modelo.
