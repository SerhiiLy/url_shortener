import random
import string

from django.core.validators import URLValidator
from drf_yasg import openapi
from drf_yasg.openapi import Schema, TYPE_ARRAY, TYPE_OBJECT
from drf_yasg.utils import swagger_auto_schema
from hashids import Hashids
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F

from .forms import UrlShortenFrom
from .models import UrlData
from .serializers import UrlDataSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from django.db.models import Sum
from django.core import serializers

validate = URLValidator()
hashids = Hashids(min_length=2, salt='salt')


# def url_short(request):
#     if request.method == 'POST':
#         form = UrlShortenFrom(request.POST)
#         if form.is_valid():
#             url = form.cleaned_data['url']
#
#             new_url = UrlData(url=url)
#             new_url.save()
#
#             url_id = new_url.id
#             hashid = hashids.encrypt(url_id)
#             short_url = request.build_absolute_uri('/') + hashid
#             new_url.short_url = hashid
#             new_url.save(update_fields=['short_url'])
#             return render(request, 'shorter/index.html', {'short_url': short_url, 'form': form})
#         elif UrlData.objects.filter(url=form['url'].value()).exists():
#             return render(request, 'shorter/index.html',
#                           {'short_url': request.build_absolute_uri('/') + UrlData.objects.get(
#                               url=form['url'].value()).short_url,
#                            'form': form})

    # else:
    #     form = UrlShortenFrom()
    # # data = UrlData.objects.all()
    # context = {
    #     'form': form,
    #     # 'data': data
    # }
    # return render(request, 'shorter/index.html', context)


def url_redirect(request, short_url):
    data = UrlData.objects.get(short_url=short_url)
    return redirect(data.url)


class ShortenerApiView(APIView):
    serializer_class = UrlDataSerializer
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'shorter/index.html'

    # def get(self, request):
    #     """Return a list of APIView features."""
    #
    #     an_apiview = ['Uses HTTP methods as function (get, post, patch, put, delete)']
    #
    #     return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'url': openapi.Schema(type=openapi.TYPE_STRING, description='link'),
        })
    )
    def post(self, request):
        """Return a short url."""

        serializer = UrlDataSerializer(data=request.data)
        if serializer.is_valid():
            try:
                validate(url := serializer.data.get('url'))
                new_url = UrlData(url=url)
                new_url.save()

                url_id = new_url.id
                hashid = hashids.encrypt(url_id)
                short_url = request.build_absolute_uri('/') + hashid
                new_url.short_url = hashid
                new_url.save(update_fields=['short_url'])

                return Response({'shortened_url': short_url})

            except ValidationError as e:
                return Response({'shortened_url': 'String is not valid URL'})

        elif UrlData.objects.filter(url=serializer.data.get('url')).exists():
            UrlData.objects.filter(url=serializer.data.get('url')).update(url_was_shorted=F('url_was_shorted')+1)
            return Response({'shortened_url': request.build_absolute_uri('/') + str(
                UrlData.objects.get(url=serializer.data.get('url')).short_url)})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShortenedLinkApiView(APIView):
    serializer_class = UrlDataSerializer

    def get(self, request):
        """Return a count how many url was shorted."""

        an_apiview = UrlData.objects.aggregate(Sum('url_was_shorted'))

        return Response(an_apiview)


class ShortenedTopLinkApiView(APIView):
    serializer_class = UrlDataSerializer

    def get(self, request):
        """Return top-10 link which are often shorted"""

        last_ten_urls = UrlData.objects.order_by('-url_was_shorted').values('url')
        return Response({'top_link': last_ten_urls[:10]})
