from django.db import models

class SampleModel(models.Model):
    char_field = models.CharField(max_length=200)
    required = models.CharField(max_length=200, required=False)
    default = models.CharField(max_length=200, default='yo!')
    int_field = models.IntegerField()
    bool_field = models.BooleanField()
