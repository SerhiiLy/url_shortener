from hashids import Hashids

from shortener.models import UrlData

hashids = Hashids(min_length=2, salt='salt')


def url_shortener(url):
    new_url = UrlData(url=url)
    new_url.save()

    url_id = new_url.id
    hash_code = hashids.encrypt(url_id)

    new_url.short_url = hash_code
    new_url.save(update_fields=['short_url'])

    return hash_code
