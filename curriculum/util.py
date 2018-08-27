def int_or_none(val):
    try:
        return int(val)
    except ValueError:
        return None