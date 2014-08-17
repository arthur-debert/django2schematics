from __future__ import absolute_import
import os
import sys
from unittest2 import TestCase
from django2schematics.command_helpers import get_models_to_output
from django2schematics.test.sampleproject.appone.models import (
    SampleModel, AnotherModel
)
from django2schematics.test.sampleproject.apptwo.models import SampleModelTwo
sys.path.append(os.path.join(os.path.dirname(__file__), "sampleproject"))


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


class AppNameTest(TestCase):
    def test_one_model(self):
        data = get_models_to_output('apptwo')
        self.assertEquals(data.keys(), [ 'apptwo'])
        self.assertEquals(data['apptwo'], [SampleModelTwo])

