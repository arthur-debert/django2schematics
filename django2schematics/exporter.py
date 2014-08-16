from djtypes import NullBooleanType
from schematics.types import IntType, StringType, FloatType, DecimalType, \
    DateTimeType, BooleanType, EmailType
from schematics.models import Model
from schematics.types.compound import ModelType, ListType
from django.db.models import AutoField, CharField, DateTimeField, \
    BooleanField, EmailField, NullBooleanField, ForeignKey, \
    IntegerField


class OptionModel(Model):
    name = StringType(required=False)
    value = StringType(required=True)

    def to_string(self):
        if self.name:
            return "%s=%s" % (self.name, self.value)
        return "%s" % self.name


class FieldModel(Model):
    name = StringType(required=True)
    options = ListType(OptionModel)
    type = StringType()

    @staticmethod
    def from_django(field):
        the_type = get_type(field)
        sh_type = get_schematics_type(the_type)
        return FieldModel({'name': field.name,
                           'type': sh_type.__name__,
                           'options': []
        })

    def to_string(self):
        return "%s = %s(%s)" % (self.name, self.type,
                                ",".join([x.to_string() for x in self.options]))


class ConvertedModel(Model):
    name = StringType(required=True)
    fields = ListType(FieldModel)

    def from_django(self, model):
        model = ConvertedModel({
            'name': model._meta.object_name,
        })
        for field in model._meta.fields:
            model.fields.append(FieldModel.from_django(field))


def options_for_char(field):
    return ["max_length=%s" % field.max_length]


def get_schematics_type(the_type):
    return {
        AutoField: IntType,
        IntegerField: IntType,
        CharField: StringType,
        DateTimeField: DateTimeType,
        BooleanField: BooleanType,
        EmailField: EmailType,
        NullBooleanField: NullBooleanType,
        ForeignKey: ModelType,
    }.get(the_type, StringType)


def get_type(field):
    known_types = (
        AutoField, IntegerField, CharField, DateTimeField, BooleanField,
        EmailField, NullBooleanField, ForeignKey)
    if type(field) in known_types:
        if type(field) == AutoField:
            return IntegerField
        return type(field)
    for this_type in field.__class__.__mro__:
        if this_type in known_types:
            return this_type
