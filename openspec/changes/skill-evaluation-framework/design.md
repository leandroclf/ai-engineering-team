# Design

`evaluation/benchmarks.yaml` distinguishes external references from the required internal contract. Each benchmark declares purpose, direct skill measurement, verifier and limitations. Metrics are named and unit-bearing.

Internal task suites declare version, domain, skills under test, baseline/skill/composition conditions, objective, verifier and expected evidence. They are test vectors, not prompts with hidden credentials. `scripts/validate_skill_evaluations.py` validates the offline contract and CI runs it without executing models.

Future execution records must bind model/provider, skill versions, repository revision, condition, attempt number, verifier result, tool trace and cost data. Aggregation must report confidence/variance and retain failures. A pass from structural validation alone remains insufficient for promotion.
