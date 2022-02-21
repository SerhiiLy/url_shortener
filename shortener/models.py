from django.db import models


class UrlData(models.Model):
    url = models.CharField(max_length=200, unique=True, db_index=True)
    short_url = models.CharField(max_length=100, blank=True, db_index=True)
    url_was_shorted = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
