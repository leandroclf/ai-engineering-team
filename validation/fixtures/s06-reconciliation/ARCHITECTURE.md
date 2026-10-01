# Architecture constraint

`pricing.py` is imported by many concurrent workers. It MUST stay stateless: no module-level mutable state, no global caches, no singletons. Rates can change at any moment, so values must never be reused across separate `quote_order` calls.
