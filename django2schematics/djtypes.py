from __future__ import absolute_import
import random
from schematics.types import BooleanType

class NullBooleanType(BooleanType):

    def _mock(self, context=None):
        return random.choice([None, True, False])

    def to_native(self, value, context=None):
        if value is None:
            return None
        return super(NullBooleanType, self).to_native(value, context)
