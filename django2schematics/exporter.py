from djtypes import NullBooleanType
from schematics.types import IntType, StringType, FloatType, DecimalType, \
    DateTimeType, BooleanType, EmailType
from schematics.models import Model
from schematics.types.compound import ModelType, ListType
from django.db.models import AutoField, CharField, DateTimeField, \
    BooleanField, EmailField, NullBooleanField, ForeignKey, \
    IntegerField
from django.db.models.fields import NOT_PROVIDED


class OptionModel(Model):
    name = StringType(required=False)
    value = StringType(required=True)

    def to_string(self):
        if self.name:
            return "%s=%s" % (self.name, self.value)
        return "%s" % self.name


def get_option(field, attr_name):
    if hasattr(field, attr_name) and getattr(field, attr_name) != NOT_PROVIDED:
        print field, attr_name, getattr(field, attr_name)
        return OptionModel({
            'name': attr_name,
            'value': getattr(field, attr_name)
        })


class FieldModel(Model):
    name = StringType(required=True)
    options = ListType(OptionModel)
    type = StringType()


    @classmethod
    def from_django(cls, field):
        the_cls =  TYPE_MAP.get(
            get_schematics_type(type(field)),  FieldModel)
        model =  the_cls(the_cls.init_args(field))
        model.options = the_cls.get_options(field)
        return model

    @classmethod
    def init_args(cls, field):
        the_type = get_type(field)
        sh_type = get_schematics_type(the_type)
        return {'name': field.name,
                           'type': sh_type.__name__,
                           'options': [],
        }

    @classmethod
    def get_options(cls, field):
        options = [option for option in
                   [get_option(field, name) for name in "required", 'default']
                   if option]
        return  options

    def to_string(self):
        return "%s = %s(%s)" % (self.name, self.type,
                                ",".join([x.to_string() for x in self.options]))


class CharFieldModel(FieldModel):
    @classmethod
    def get_options(cls, field):
        return [x for x in FieldModel.get_options(field) +
                   [get_option(field, 'max_length')] if x ]


class SchematicsModel(Model):
    name = StringType(required=True)
    fields = ListType(FieldModel)

    @staticmethod
    def from_django(model):
        model = SchematicsModel({
            'name': model._meta.object_name,
        })
        for field in model._meta.fields:
            model.fields.append(FieldModel.from_django(field))


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



TYPE_MAP = {
    StringType: CharFieldModel,
}
