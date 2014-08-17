

class SampleModel(Model):
    id = IntType(required=True)
    char_field = StringType(required=True, max_length=200)
    required = StringType(required=True, max_length=200)
    default = StringType(required=True, default='yo!', max_length=200)
    int_field = IntType(required=True)
    bool_field = BooleanType(required=True)


class AnotherModel(Model):
    id = IntType(required=True)
    yo = StringType(required=True, max_length=20)


class SampleModelTwo(Model):
    id = IntType(required=True)
    char_field = StringType(required=True, max_length=200)
    required = StringType(required=True, max_length=200)
    default = StringType(required=True, default='yo!', max_length=200)
    int_field = IntType(required=True)
    bool_field = BooleanType(required=True)

