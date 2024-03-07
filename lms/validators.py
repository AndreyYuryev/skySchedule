import re
from rest_framework.serializers import ValidationError


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        regex = '^https?:\/\/\S{0,}(youtube.com)+\S{0,}$'
        field_value = dict(value).get(self.field)
        if not bool(re.match(regex, field_value)):
            raise ValidationError('Link should be on youtube.com')
