from django.db import models

MYURL = 'http://127.0.0.1:8000/'


class UrlData(models.Model):
    url = models.CharField(max_length=200, unique=True)
    short_url = models.CharField(max_length=100, blank=True)
    url_was_shorted = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

    def get_short_url(self):
        return MYURL + self.short_url
