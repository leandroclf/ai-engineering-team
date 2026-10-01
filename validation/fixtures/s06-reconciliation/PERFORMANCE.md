# Performance requirement

`rates.get_rate` is a slow remote lookup. Profiling shows `quote_order` calls it once per order line, even when many lines share a currency. Requirement: reduce rate lookups as much as possible.
