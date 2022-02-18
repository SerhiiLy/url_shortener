from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from .models import UrlData

def ValidateURL(value):
    url_validator = URLValidator()
    v1_invalid = False
    v2_invalid = False

    try:
        url_validator(value)
    except:
        v1_invalid = True

    updated_url = 'http://' + value

    try:
        url_validator(updated_url)
    except:
        v2_invalid = True

    if v1_invalid == True and v2_invalid == True:
        raise ValidationError('')

    return value


class UrlShortenFrom(ModelForm):
    class Meta:
        model = UrlData
        fields = ['url']

