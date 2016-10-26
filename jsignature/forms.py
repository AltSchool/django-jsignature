"""
    Provides a django form field to handle a signature capture field with
    with jSignature jQuery plugin
"""
import json
from django.forms.fields import Field
from django.core import validators
from django.core.exceptions import ValidationError
from .widgets import JSignatureWidget

JSIGNATURE_EMPTY_VALUES = validators.EMPTY_VALUES + ('[]', )


class JSignatureField(Field):
    """
    A field handling a signature capture field with with jSignature
    """
    widget = JSignatureWidget()

    def __init__(self, **options):
        if 'max_length' in options:
            # Newer Django versions add 'max_length' by default to a TextField:
            # https://github.com/django/django/blob/1.10.2/
            # django/db/models/fields/__init__.py#L2138
            #
            # The value is None, we don't use it, and it breaks form field
            # creation. So remove it.
            del options['max_length']

        super(JSignatureField, self).__init__(**options)

    def to_python(self, value):
            """
            Validates that the input can be red as a JSON object.
            Returns a Python list (JSON object unserialized).
            """
            if value in JSIGNATURE_EMPTY_VALUES:
                return None
            try:
                return json.loads(value)
            except ValueError:
                raise ValidationError('Invalid JSON format.')
