from __future__ import absolute_import
from unittest2 import TestCase

from schematics.types import (
    IntType, StringType, DateTimeType, EmailType,  BooleanType,
    DecimalType)
from schematics.types.compound import ModelType

from django.db.models import (
    CharField, IntegerField, AutoField, DateTimeField,
    EmailField, BooleanField, NullBooleanField, ForeignKey,
    DecimalField)

from django2schematics.djtypes import NullBooleanType
from django2schematics.converter import get_type, get_schematics_type, FieldModel


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
        self.assertEqual(field_model.to_string(), 'myint = IntType(required=True)')

    def test_required(self):
        field = IntegerField(name='myint', null=True)
        field_model = FieldModel.from_django(field)
        option = field_model.options[0]
        self.assertEqual(option.name, 'required')
        self.assertEqual(option.value, 'False')
        field = IntegerField(name='myint', null=False)
        field_model = FieldModel.from_django(field)
        option = field_model.options[0]
        self.assertEqual(option.name, 'required')
        self.assertEqual(option.value, 'True')


class CharFieldTest(TestCase):
    def test_get_type(self):
        self.assertEqual(get_type(CharField()), CharField)

    def test_get_schematic_type(self):
        self.assertEqual(get_schematics_type(type(CharField())), StringType)

    def test_max_length(self):
        field = CharField(name='thestring', max_length=30)
        field_model = FieldModel.from_django(field)
        option = field_model.options[1]
        self.assertEqual(option.name, 'max_length')
        self.assertEqual(option.value, '30')


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

    def test_output(self):
        field = ForeignKey('self', name='myfk')
        field_model = FieldModel.from_django(field)
        self.assertEqual(field_model.to_string(),
                         "myfk = ModelType('self', required=True)")


class DecimalFieldTest(TestCase):
    def test_get_type(self):
        self.assertEqual(get_type(DecimalField()), DecimalField)

    def test_get_schematic_type(self):
        self.assertEqual(get_schematics_type(type(DecimalField())), DecimalType)

    def test_max_length(self):
        field = DecimalField(name='thestring', max_digits=5, decimal_places=2)
        field_model = FieldModel.from_django(field)
        option = field_model.options[2]
        self.assertEqual(option.name, 'max_digits')
        self.assertEqual(option.value, '5')
        option = field_model.options[1]
        self.assertEqual(option.name, 'decimal_places')
        self.assertEqual(option.value, '2')
