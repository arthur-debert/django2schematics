from __future__ import absolute_import
import os
os.environ['DJANGO_SETTINGS_MODULE'] = \
    'django2schematics.test.sampleproject.settings'

from unittest2 import TestCase

from schematics.types import (
    IntType, StringType, DateTimeType, EmailType,  BooleanType
)
from schematics.types.compound import ModelType

from django.db.models import (
    CharField, IntegerField, AutoField, DateTimeField,
    EmailField, BooleanField, NullBooleanField, ForeignKey
)

from django2schematics.djtypes import NullBooleanType
from django2schematics.exporter import get_type, get_schematics_type, FieldModel


class IntegerFieldTest(TestCase):

    def test_get_type(self):
        self.assertEqual(get_type(IntegerField()), IntegerField)

    def test_get_schematics_type(self):
        self.assertEqual(get_schematics_type(type(IntegerField())), IntType)

    def test_field_name(self):
        field = IntegerField(name='myint')
        field_model = FieldModel.from_django(field)
        self.assertEqual(field_model.name, 'myint')

    def test_output(self):
        field = IntegerField(name='myint')
        field_model = FieldModel.from_django(field)
        self.assertEqual(field_model.to_string(), 'myint = IntType()')


class CharFieldTest(TestCase):
    def test_get_type(self):
        self.assertEqual(get_type(CharField()), CharField)

    def test_get_schematic_type(self):
        self.assertEqual(get_schematics_type(type(CharField())), StringType)


class AutoFieldTypeTest(TestCase):

    def test_get_type(self):
        self.assertEqual(get_type(AutoField(primary_key=True)),
                         IntegerField)

    def test_get_schematic_type(self):
        self.assertEqual(get_schematics_type(type(AutoField(primary_key=True))),
                         IntType)


class DateTimeTypeTest(TestCase):

    def test_get_type(self):
        self.assertEqual(get_type(DateTimeField(primary_key=True)),
                         DateTimeField)

    def test_get_schematic_type(self):
        self.assertEqual(get_schematics_type(type(DateTimeField())),
                         DateTimeType)


class EmailTypeTest(TestCase):
    def test_get_type(self):
        self.assertEqual(get_type(EmailField()), EmailField)

    def test_get_schematic_type(self):
        self.assertEqual(get_schematics_type(type(EmailField())), EmailType)


class BooleanTypeTest(TestCase):
    def test_get_type(self):
        self.assertEqual(get_type(BooleanField()), BooleanField)

    def test_get_schematic_type(self):
        self.assertEqual(get_schematics_type(type(BooleanField())), BooleanType)


class NullBooleanTypeTest(TestCase):
    def test_get_type(self):
        self.assertEqual(get_type(NullBooleanField()), NullBooleanField)

    def test_get_schematic_type(self):
        self.assertEqual(get_schematics_type(type(NullBooleanField())),
                         NullBooleanType)


class ForeignKeyTypeTest(TestCase):
    def test_get_type(self):
        self.assertEqual(get_type(ForeignKey('self')), ForeignKey)

    def test_get_schematic_type(self):
        self.assertEqual(get_schematics_type(type(ForeignKey('self'))),
                         ModelType)
