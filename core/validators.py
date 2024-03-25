from django.core.exceptions import ValidationError


def validate_result(result):
    if type(result) is not int:
        result = int(result)
    if result not in range(1, 11):
        raise ValidationError(
            'Результат должен быть целым числом от 1 до 10',
            params={'result': result}
        )
