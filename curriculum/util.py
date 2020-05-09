def int_or_false(val):
    if val == False:
        return False
    return int(val)

def all_equal(lst):
    """Returns true if all items in the list are equal."""
    return len(set(lst)) == 1

def all_in_or_all_not_in(keys, data):
    """Returns true if all keys are present, or no keys are present."""
    in_values = [
        key in data for key in keys
    ]
    return all_equal(in_values)

def all_same_length(keys, data):
    """Returns true when all keys index lists in data that share the same length."""
    lengths = [
        len(data.get(key, [])) for key in keys
    ]
    return all_equal(lengths)

def all_equally_present_with_same_length(keys, data):
    """Returns true when all keys are in data and they index lists that share the same length, or no keys are in data."""
    return all_in_or_all_not_in(keys, data) and all_same_length(keys, data)
