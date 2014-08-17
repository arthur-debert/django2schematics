from __future__ import absolute_import
import os
import sys
from unittest2 import TestCase
from django2schematics.command_helpers import get_models_to_output, get_output
from django2schematics.test.sampleproject.appone.models import (
    SampleModel, AnotherModel
)
from django2schematics.test.sampleproject.apptwo.models import SampleModelTwo
sys.path.append(os.path.join(os.path.dirname(__file__), "sampleproject"))


def get_fixture_result(file_name):
    the_path =  os.path.join(os.path.dirname(__file__), file_name)
    return open(the_path, 'r').read().rstrip()

class ModelOnlyTest(TestCase):

    def test_one_model(self):
        data = get_models_to_output("appone.SampleModel")
        self.assertEquals(data.keys(), ['appone'])
        self.assertEquals(data['appone'], [SampleModel])

    def test_two_models(self):
        data = get_models_to_output("appone.SampleModel","appone.AnotherModel",
                                    'apptwo.SampleModelTwo')
        self.assertEquals(data.keys(), ['appone', 'apptwo'])
        self.assertEquals(data['appone'], [SampleModel, AnotherModel])
        self.assertEquals(data['apptwo'], [SampleModelTwo])

    def test_two_models_content(self):
        result = get_output( ["appone.SampleModel","appone.AnotherModel",
                                'apptwo.SampleModelTwo'],
                            to_file=None, auto_file_name=None)
        expected = get_fixture_result('both_apps_output.py')
        self.maxDiff = None
        self.assertMultiLineEqual(result, expected)


class AppNameTest(TestCase):
    def test_one_app(self):
        data = get_models_to_output('apptwo')
        self.assertEquals(data.keys(), [ 'apptwo'])
        self.assertEquals(data['apptwo'], [SampleModelTwo])

    def test_app_with_many(self):
        result = get_output( ["appone"],
                            to_file=None, auto_file_name=None)
        expected = get_fixture_result('one_app_output.py')
        self.assertMultiLineEqual(result, expected)



