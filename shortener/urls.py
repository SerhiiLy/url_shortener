from django.urls import include, path, re_path
from . import views
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from source.yasg import urlpatterns as doc_urls

urlpatterns = [

    # path("", views.url_short, name="home"),
    path("<str:short_url>", views.UrlRedirect.as_view(), name="redirect"),

    path('shorten_url/', views.ShortenerApiView.as_view()),
    path('shortened_urls_count/', views.ShortenedLinkApiView.as_view()),
    path('top_urls/', views.ShortenedTopLinkApiView.as_view()),
]
urlpatterns += doc_urls
