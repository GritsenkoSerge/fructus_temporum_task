import requests
from bs4 import BeautifulSoup

from bookmarks.models import Bookmark, LinkType

OG_FIELDS = {
    'title': ('og:title', 'title', None, ''),
    'description': ('og:description', 'description', None, ''),
    'link_type': ('og:type', None, LinkType.values, LinkType.WEBSITE),
    'image': ('og:image', None, None, ''),
}


def fill_bookmark_by_link(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    instance = Bookmark()
    for attr, (og_tag, reserved_tag, restriction, default_value) in OG_FIELDS.items():
        value = soup.find('meta', property=og_tag)
        if value is None:
            value = soup.find('meta', property=reserved_tag)
        if value:
            value = value.get('content')
        if value is None or restriction and value not in restriction:
            value = default_value
        setattr(instance, attr, value)
    return instance
