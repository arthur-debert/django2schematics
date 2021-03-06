from django.db import models


class SampleModel(models.Model):
    char_field = models.CharField(max_length=200)
    required = models.CharField(max_length=200, null=False)
    default = models.CharField(max_length=200, default='yo!')
    int_field = models.IntegerField()
    bool_field = models.BooleanField()


class AnotherModel(models.Model):
    yo = models.CharField(max_length=20)
    linked = models.ForeignKey(SampleModel)

class Compound(models.Model):
    to_another = models.ManyToManyField(AnotherModel)
