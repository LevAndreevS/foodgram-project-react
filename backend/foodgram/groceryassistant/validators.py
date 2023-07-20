
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


def validate_cooking_time(self, cooking_time):
    if cooking_time < settings.TIME_MIN_COOKING:
        raise ValidationError(
            'Время готовки должно быть не менее одной минуты')
    if cooking_time > settings.TIME_MAX_COOKING:
        raise ValidationError(
            'Время приготовления должно быть не более 10-ти часов')
    return cooking_time


def validate_amount(self, amount_digit):
    if amount_digit < settings.MIN_AMOUNT:
        MinValueValidator(
            settings.MIN_AMOUNT,
            f'Минимальное количество ингридиента должно быть больше '
            f'{settings.MIN_AMOUNT}'
        )
    return amount_digit
