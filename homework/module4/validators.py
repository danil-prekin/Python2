from wtforms.validators import ValidationError
from typing import Optional

def number_length(min_len: int, max_len: int, message: Optional[str] = None):
    def _number_length(form, field):
        value = str(field.data)
        if not (min_len <= len(value) <= max_len):
            msg = message or f'Длина числа должна быть от {min_len} до {max_len} цифр.'
            raise ValidationError(msg)
    return _number_length

class NumberLength:
    def __init__(self, min_len: int, max_len: int, message: Optional[str] = None):
        self.min_len = min_len
        self.max_len = max_len
        self.message = message

    def __call__(self, form, field):
        value = str(field.data)
        if not (self.min_len <= len(value) <= self.max_len):
            msg = self.message or f'Длина числа должна быть от {self.min_len} до {self.max_len} цифр.'
            raise ValidationError(msg)
