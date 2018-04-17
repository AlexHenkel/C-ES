def is_float(data):
    try:
        parsed_data = float(data)
        return parsed_data
    except ValueError:
        pass

    return False


def is_boolean(data):
    parsed_data = str(data).rstrip().lower()
    if parsed_data != 'verdadero' and parsed_data != 'falso':
        return False

    return parsed_data


def cast_bool(data):
    if data:
        return 'verdadero'
    return 'falso'


def cast_bool_inverse(data):
    if data == 'verdadero':
        return True
    return False
