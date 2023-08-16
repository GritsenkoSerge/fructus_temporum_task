from django.contrib import admin

from bookmarks.models import Bookmark, Collection


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'link', 'user', 'collection')
    search_fields = ('title', 'description', 'id')
    list_filter = ('user',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user', 'collection')
        return queryset


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'user')
    search_fields = ('name', 'description', 'id')
    list_filter = ('user',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user')
        return queryset
