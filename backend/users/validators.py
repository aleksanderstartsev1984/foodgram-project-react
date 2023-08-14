from re import findall

from django.conf import settings
from django.core.exceptions import ValidationError


def no_bad_symbols_validator(value):
    invalid_symbols = set(findall(settings.NO_INVALID_SYMBOLS_USERNAME, value))
    if invalid_symbols:
        invalid_symbols_str = ', '.join(invalid_symbols)
        raise ValidationError(
            f'Ник содержит недопустимые символы: {invalid_symbols_str}'
        )
    return value
