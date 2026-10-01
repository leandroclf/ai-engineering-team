"""Stand-in for a slow remote rate service."""
RATES = {"USD": 1.0, "EUR": 1.1, "BRL": 0.2}
CALLS = []


def get_rate(currency):
    CALLS.append(currency)
    return RATES[currency]
