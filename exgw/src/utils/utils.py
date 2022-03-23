""" Utilities
"""
import json


# TODO(Alex) Replace with JSON, like below.
def str_to_bool(string: str) -> bool:
    """ Convert string representation of true/false to True/False.
    """
    if string.lower() == 'true':
        return True
    elif string.lower() == 'false':
        return False
    else:
        raise ValueError()


def string_to_value(input: dict) -> dict:
    """ Convert string values to appropriate types.

    Alternative to using eval().
    :param input: Dictionary with string values.
    :return: Dictionary with type-converted values.
    """
    output = {}
    for key, value in input.items():
        try:
            output[key] = json.loads(value)
        except json.decoder.JSONDecodeError:
            # Typically values that should not be converted, like 'some_string'
            output[key] = value
    return output
