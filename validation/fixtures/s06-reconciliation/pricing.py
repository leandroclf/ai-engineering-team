import rates


def quote_order(lines):
    """lines: iterable of (amount, currency). Returns total in USD."""
    return round(sum(amount * rates.get_rate(cur) for amount, cur in lines), 2)
