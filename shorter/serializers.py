from .models import UrlData
from rest_framework import serializers


class UrlDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UrlData
        fields = ['id', 'url']
