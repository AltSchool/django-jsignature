"""
    Provides a django model field to store a signature captured
    with jSignature jQuery plugin
"""
import json
import yaml
import six

from django.db import models
from django.core.exceptions import ValidationError

from .forms import (
    JSignatureField as JSignatureFormField,
    JSIGNATURE_EMPTY_VALUES
)


class JSignatureField(models.TextField):
    """
    A model field handling a signature captured with jSignature
    """
    description = "A signature captured with jSignature"

    def from_db_value(self, value, *_unused):
        """
        Validates that the input can be red as a JSON object. Returns a Python
        datetime.date object.
        """
        if value in JSIGNATURE_EMPTY_VALUES:
            return None
        elif isinstance(value, list):
            return value
        try:
            return json.loads(value)
        except ValueError:
            raise ValidationError('Invalid JSON format.')

    def get_prep_value(self, value):
        if value in JSIGNATURE_EMPTY_VALUES:
            return None
        elif isinstance(value, six.string_types):
            # A little light parse assistance, to manage quirkiness in Django
            # forms.

            # 'u' should never appear as a proper value; just 'x', 'y' and
            # numbers. If it's here, it's bad unicode representations, so strip
            # it.
            safe_value = value.replace('u', '')

            # yaml can handle single-quotes better than JSON, so use it to
            # clear them out before saving.
            return json.dumps(yaml.load(safe_value))
        elif isinstance(value, list):
            return json.dumps(value)
        raise ValidationError('Invalid format.')

    def formfield(self, **kwargs):
        defaults = {'form_class': JSignatureFormField}
        defaults.update(kwargs)
        return super(JSignatureField, self).formfield(**defaults)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["jsignature.fields.JSignatureField"])
except ImportError:
    pass
