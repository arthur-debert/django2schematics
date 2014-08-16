from __future__ import absolute_import
import random
from schematics.types import BooleanType, BaseType


class NullBooleanType(BooleanType):
    def _mock(self, context=None):
        return random.choice([None, True, False])

    def to_native(self, value, context=None):
        if value is None:
            return None
        return super(NullBooleanType, self).to_native(value, context)


class PointType(BaseType):
    def __init__(self, srid, x, y):
        super(PointType, self).__init__()
        try:
            from django.contrib.gis.geos import Point
        except ImportError:
            raise Exception("No geojango support deceted")
        self.value = Point(x=x, y=y, srid=srid)

    def to_native(self, value, context=None):
        return value.coords if value else None
