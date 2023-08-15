from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedMixin, UUIDMixin

User = get_user_model()


class Collection(TimeStampedMixin, UUIDMixin, models.Model):
    """Коллекция закладок."""

    name = models.CharField(_('collection_name'), max_length=50, unique=True)
    """Название коллекции."""

    description = models.CharField(
        _('collection_description'),
        max_length=200,
        blank=True,
    )
    """Краткое описание коллекции."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collections',
        verbose_name=_('user'),
    )
    """Пользователь."""

    class Meta:
        db_table = 'bookmarks"."collection'
        ordering = ['name']
        verbose_name = _('collection')
        verbose_name_plural = _('collections')

    def __str__(self):
        return self.name


class LinkType(models.TextChoices):
    """Тип закладки."""

    WEBSITE = 'website', _('website')
    BOOK = 'book', _('book')
    ARTICLE = 'article', _('article')
    MUSIC = 'music', _('music')
    VIDEO = 'video', _('video')


class Bookmark(TimeStampedMixin, UUIDMixin, models.Model):
    """Закладка."""

    title = models.CharField(
        _('bookmark_title'),
        max_length=200,
        blank=True,
    )
    """Заголовок страницы."""

    description = models.CharField(
        _('bookmark_description'),
        max_length=500,
        blank=True,
    )
    """Краткое описание."""

    link = models.URLField(_('bookmark_link'))
    """Ссылка на страницу."""

    link_type = models.CharField(
        _('bookmark_link_type'),
        max_length=20,
        choices=LinkType.choices,
        default=LinkType.WEBSITE,
    )
    """Тип ссылки."""

    image = models.URLField(
        _('bookmark_link'),
        blank=True,
    )
    """Ссылка на картинку превью."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name=_('user'),
    )
    """Пользователь."""

    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        related_name='bookmarks',
        verbose_name=_('collection'),
        blank=True,
        null=True,
    )
    """Коллекция закладок."""

    class Meta:
        db_table = 'bookmarks"."bookmark'
        ordering = ['title', 'link']
        verbose_name = _('bookmark')
        verbose_name_plural = _('bookmarks')

    def __str__(self):
        return self.link
