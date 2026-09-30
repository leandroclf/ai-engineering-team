# Design: Dot-Native Engineering System

## Target architecture

```
Human Operator
      |
      v
Engineering Dot
persistent coordination / feedback / proactive work
      |
      +---- ai-engineering-team
      |     policy / OpenSpec / skills / gates / evidence
      |
      +---- Plugins / connected apps
      |     GitHub / docs / issue systems / CI / observability
      |
      +---- Codex
            repository implementation / tests / review
                |
                v
          Target Repository
          local AGENTS.md
          project adapter
          source + tests
                |
                v
          PR / Evidence / Report
                |
                v
        Approval where required
```

## Responsibilities

### Engineering Dot
- Maintain portfolio-level objectives and project context.
- Detect useful follow-up work within granted access.
- Decide whether work is conversational, Work-oriented or Codex-oriented.
- Start/manage Codex tasks when repository execution is needed.
- Apply ai-engineering-team governance before delegation.
- Track observable outcomes and operator feedback.
- Never treat learned preference as permission to bypass approvals.

### Codex
- Discover target repository instructions.
- Implement bounded engineering tasks.
- Run repository-native validation.
- Review diff and return evidence.
- Stop/escalate when authorization/context is missing.

### Repository framework
- Define engineering policy and reusable skills.
- Define R0-R3 risk vocabulary as an additional organizational layer.
- Define project adapters and evidence schemas.
- Supply OpenSpec changes and acceptance scenarios.
- Remain useful even when a specific Dot surface is unavailable.

## Native-safety composition
Native platform safeguards and plugin/provider permissions are authoritative. R0-R3 adds engineering governance but cannot weaken native controls. The strictest applicable rule wins.

## Delegation envelope
Every Dot -> Codex task SHOULD contain:
- objective and acceptance criteria;
- target repository/ref;
- relevant OpenSpec change;
- applicable local AGENTS.md;
- risk class;
- allowed side effects;
- required validation;
- expected evidence;
- stop/approval conditions.

## Project onboarding
Each target repository gets a project adapter generated from templates/PROJECT-AGENTS.md plus a portfolio registry entry. The Dot reads current repository state rather than relying solely on remembered context.

## Plugin model
Default to minimum access. Separate read/discovery from write/action permissions where the platform/provider allows. GitHub writes, deployment, infrastructure, credentials and external communications follow explicit policy and native approvals.

## Specialist evolution
V1 specialist roles remain reusable Skills. When specialized dots are available and beneficial, a role may become a specialized dot only if the same bounded delegation/evidence contract is preserved. Avoid one-dot-per-role fan-out without measured benefit.
