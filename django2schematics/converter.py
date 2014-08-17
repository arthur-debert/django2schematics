from djtypes import NullBooleanType
from schematics.types import IntType, StringType, FloatType, DecimalType, \
    DateTimeType, BooleanType, EmailType
from schematics.models import Model
from schematics.types.compound import ModelType, ListType
from django.db.models import AutoField, CharField, DateTimeField, \
    BooleanField, EmailField, NullBooleanField, ForeignKey, \
    IntegerField, FloatField, DecimalField, FileField, BigIntegerField
from django.db.models.fields import NOT_PROVIDED


class OptionModel(Model):
    name = StringType(required=False)
    value = StringType(required=True)
    is_string = BooleanType()

    def to_string(self):
        val = self.value if not self.is_string else "'%s'" % self.value
        if self.name:
            return "%s=%s" % (self.name, val)
        return "'%s'" % self.value


def get_option(field, attr_name, mapped_name, is_string, transformer=None):
    if attr_name == 'name':
        return
    if hasattr(field, attr_name) and getattr(field, attr_name) != NOT_PROVIDED:
        value = getattr(field, attr_name)
        return OptionModel({
            'name': mapped_name or attr_name,
            'value': value if not transformer else transformer(value),
            'is_string': is_string
        })


class FieldModel(Model):
    name = StringType(required=True)
    options = ListType(OptionModel)
    type = StringType()

    @classmethod
    def from_django(cls, field):
        the_cls = TYPE_MAP.get(
            get_schematics_type(type(field)), FieldModel)
        model = the_cls(the_cls.init_args(field))
        model.options = the_cls.get_options(field)
        return model

    @classmethod
    def init_args(cls, field):
        the_type = get_type(field)
        sh_type = get_schematics_type(the_type)
        return {
            'name': field.name,
            'type': sh_type.__name__,
            'options': [],
        }

    @classmethod
    def get_options(cls, field):
        options = [option for option in [
            get_option(field, name, mapped_name, is_string, transformer) for
            name, mapped_name, is_string, transformer in (
                ("null", 'required', False, lambda x: not x),
                ('default', 'default', True, None))] if option]
        return options

    def to_string(self):
        # foreign keys and related options always come first
        ordered_options = sorted(self.options, key=lambda x: bool(x.name))
        return "%s = %s(%s)" % (self.name, self.type,
                                ", ".join([option.to_string() for option in
                                           ordered_options]))


class CharFieldModel(FieldModel):
    @classmethod
    def get_options(cls, field):
        return [x for x in FieldModel.get_options(field) +
                [get_option(field, 'max_length', 'max_length', False)] if x]


class DecimalFieldModel(FieldModel):
    @classmethod
    def get_options(cls, field):
        return [x for x in FieldModel.get_options(field) +
                [get_option(field, name, mapped_name, is_string) for
                 name, mapped_name, is_string in [
                 ('decimal_places', 'decimal_places', False),
                 ('max_digits', 'max_digits', False)]] if x]


class ForeignKeyModel(FieldModel):
    @classmethod
    def get_options(cls, field):
        options = [x for x in FieldModel.get_options(field)]
        return options + [
            OptionModel({'value': field.rel.to})]


class IntegerFieldModel(FieldModel):
    pass


class SchematicsModel(Model):
    name = StringType(required=True)
    fields = ListType(FieldModel)

    @staticmethod
    def from_django(the_model):
        model = SchematicsModel({
            'name': the_model._meta.object_name,
            'fields': [],
        })
        for field in the_model._meta.fields:
            model.fields.append(FieldModel.from_django(field))
        return model

    def to_string(self):
        return 'class %s(%s):\n    %s' % (self.name, 'Model', "\n    ".join([
            field.to_string() for field in self.fields]))


class DjangoApp(Model):
    app_label = StringType()
    models = ListType(SchematicsModel)

    def to_string(self, context=None):
        return "\n\n".join([model.to_string(context=context)
                            for model in self.models])


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
        DecimalField: DecimalType,
        FloatField: FloatType,
        BigIntegerField: IntType,
    }.get(the_type, StringType)


def get_type(field):
    known_types = (
        AutoField, IntegerField, CharField, DateTimeField, BooleanField,
        EmailField, NullBooleanField, ForeignKey, DecimalField, FileField,
        BigIntegerField
    )
    if type(field) in known_types:
        if type(field) == AutoField:
            return IntegerField
        return type(field)
    for this_type in field.__class__.__mro__:
        if this_type in known_types:
            return this_type


TYPE_MAP = {
    StringType: CharFieldModel,
    DecimalType: DecimalFieldModel,
    ModelType: ForeignKeyModel,
    IntType: IntegerFieldModel,
}
