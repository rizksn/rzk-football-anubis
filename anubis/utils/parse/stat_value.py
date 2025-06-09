def convert_stat_value(key, value, int_fields=None, float_fields=None, string_fields=None):
    if value in ("", "--"):
        return None

    int_fields = int_fields or set()
    float_fields = float_fields or set()
    string_fields = string_fields or set()

    try:
        if key in int_fields:
            return int(value.replace(",", ""))
        elif key in float_fields:
            return float(value.replace("%", "").replace(",", ""))
        elif key in string_fields:
            return value.strip()
    except ValueError:
        return value

    return value
