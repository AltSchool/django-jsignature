from datetime import date
from django.test import SimpleTestCase

from jsignature.mixins import JSignatureFieldsMixin


class JSignatureTestModel(JSignatureFieldsMixin):
    pass


class JSignatureFieldsMixinTest(SimpleTestCase):
    def tearDown(self):
        settings.INSTALLED_APPS = self.old_installed_apps

    def test_save_create(self):
        # If an object is created signed, signature date must be set
        signature_value = [{"x": [1, 2], "y": [3, 4]}]
        i = JSignatureTestModel(signature=signature_value)
        i.save()
        i = JSignatureTestModel.objects.get(pk=i.pk)
        self.assertEqual(date.today(), i.signature_date.date())

    def test_save_no_change(self):
        # If signature doesn't change, signature date must not be updated
        signature_value = [{"x": [1, 2], "y": [3, 4]}]
        i = JSignatureTestModel(signature=signature_value)
        i.save()
        i.signature_date = date(2013, 1, 1)
        i.save()
        i = JSignatureTestModel.objects.get(pk=i.pk)
        self.assertEqual(date(2013, 1, 1), i.signature_date.date())

    def test_save_change(self):
        # If signature changes, signature date must be updated too
        signature_value = [{"x": [1, 2], "y": [3, 4]}]
        new_signature_value = [{"x": [5, 6], "y": [7, 8]}]
        i = JSignatureTestModel(signature=signature_value,
                                signature_date=date(2013, 1, 1))
        i.save()
        i.signature_date = date(2013, 1, 1)
        i.signature = new_signature_value
        i.save()
        i = JSignatureTestModel.objects.get(pk=i.pk)
        self.assertEqual(date.today(), i.signature_date.date())

    def test_save_none(self):
        # If sinature is set to None, it must be the same for signature_date
        signature_value = [{"x": [1, 2], "y": [3, 4]}]
        i = JSignatureTestModel(signature=signature_value)
        i.save()
        i.signature = None
        i.save()
        i = JSignatureTestModel.objects.get(pk=i.pk)
        self.assertIsNone(i.signature_date)
