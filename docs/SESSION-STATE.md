# Session / Persistence Abstraction
Persistent runtimes should store useful resumable state: objective, decisions, plan status, evidence, blockers and repository revision. Conversation history is not authoritative over current repository state. On resume, revalidate revision and instructions before mutation. Apply context budgets and compact stale detail.
