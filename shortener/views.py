from django.core.validators import URLValidator
from django.views import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# from hashids import Hashids
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
from .services import shortener_service
from .models import UrlData
from .serializers import UrlDataSerializer
from django.db.models import Sum

from .services.layer_service import get_client_ip

validate = URLValidator()


# hashids = Hashids(min_length=2, salt='salt')

# to do class
class UrlRedirect(View):
    def get(seld, request, short_url):
        data = UrlData.objects.get(short_url=short_url)
        return redirect(data.url)


class ShortenerApiView(APIView):
    serializer_class = UrlDataSerializer

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'url': openapi.Schema(type=openapi.TYPE_STRING, description='link'),
        })
    )
    def post(self, request):
        """Return a short url."""
        try:
            serializer = UrlDataSerializer(data=request.data)

            if serializer.is_valid() and validate(url := serializer.data.get('url')):
                hash_code = shortener_service.url_shortener(url)

                return Response({'shortened_url': request.build_absolute_uri('/') + hash_code})

            elif url := UrlData.objects.filter(url=serializer.data.get('url')):
                url.update(url_was_shorted=F('url_was_shorted') + 1)
                return Response({'shortened_url': request.build_absolute_uri('/') + str(url.first().short_url),
                                 'client': get_client_ip(request)})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            return Response({'shortened_url': 'String is not valid URL'})


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
