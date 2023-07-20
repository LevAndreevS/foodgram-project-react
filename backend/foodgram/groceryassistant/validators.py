
import re

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from foodgram import settings


def validate_forbidden_characters(value):
    if not re.match(settings.REGEX_FOR_USER_LOGIN, value) and \
            re.fullmatch(settings.REGEX_FOR_TAG_SLUG, value):
        raise ValidationError(
            "Cодержаться запрещённые символы!"
        )
    if value == settings.FORBIDDEN_LOGIN:
        raise ValidationError(
            "Недопустимое имя для регистрации логина!"
        )
    return value


def validate_cooking_time(digit):
    if digit < settings.TIME_MIN_COOKING:
        MinValueValidator(
            settings.TIME_MIN_COOKING,
            f'Минимальное время от {settings.TIME_MIN_COOKING} минуты'
        )
    return digit
