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
