from bookmarks.models import Bookmark, LinkType


def fill_bookmark_by_link(link):
    instance = Bookmark()
    instance.title = 'title'
    instance.link_type = LinkType.WEBSITE
    return instance
