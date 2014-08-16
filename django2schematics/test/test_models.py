from __future__ import absolute_import
from unittest2 import TestCase


from django.db.models import (
    CharField, IntegerField, Model
)

from django2schematics.converter import (
    SchematicsModel, CharFieldModel, IntegerFieldModel
)


class AModel(Model):
    label = CharField(max_length=20)
    count = IntegerField()


class ModelFieldListTest(TestCase):
    def test_field_count(self):

        the_model = SchematicsModel.from_django(AModel)
        # id comes by default
        self.assertEqual(len(the_model.fields), 3)

    def test_field_labels(self):
        the_model = SchematicsModel.from_django(AModel)
        self.assertEqual(the_model.fields[0].name, 'id')
        self.assertEqual(the_model.fields[1].name, 'label')
        self.assertEqual(the_model.fields[2].name, 'count')

    def test_field_types(self):
        the_model = SchematicsModel.from_django(AModel)
        self.assertEqual(type(the_model.fields[0]), IntegerFieldModel)
        self.assertEqual(type(the_model.fields[1]), CharFieldModel)
        self.assertEqual(type(the_model.fields[0]), IntegerFieldModel)


class ModelOutputTest(TestCase):
    def test_simple_output(self):
        the_model = SchematicsModel.from_django(AModel)
        output = """class AModel(Model):
    id = IntType(required=True)
    label = StringType(required=True, max_length=20)
    count = IntType(required=True)"""

        self.assertEqual(the_model.to_string(), output)
