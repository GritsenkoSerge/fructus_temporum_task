# Generated by Django 4.2.4 on 2023-08-15 22:52

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='created_at'),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='updated_at'),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name='id',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=50,
                        unique=True,
                        verbose_name='collection_name',
                    ),
                ),
                (
                    'description',
                    models.CharField(
                        blank=True,
                        max_length=200,
                        verbose_name='collection_description',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='collections',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='user',
                    ),
                ),
            ],
            options={
                'verbose_name': 'collection',
                'verbose_name_plural': 'collections',
                'db_table': 'bookmarks"."collection',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='created_at'),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='updated_at'),
                ),
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name='id',
                    ),
                ),
                (
                    'title',
                    models.CharField(
                        blank=True,
                        max_length=200,
                        verbose_name='bookmark_title',
                    ),
                ),
                (
                    'description',
                    models.CharField(
                        blank=True,
                        max_length=500,
                        verbose_name='bookmark_description',
                    ),
                ),
                ('link', models.URLField(verbose_name='bookmark_link')),
                (
                    'link_type',
                    models.CharField(
                        choices=[
                            ('website', 'website'),
                            ('book', 'book'),
                            ('article', 'article'),
                            ('music', 'music'),
                            ('video', 'video'),
                        ],
                        default='website',
                        max_length=20,
                        verbose_name='bookmark_link_type',
                    ),
                ),
                (
                    'image',
                    models.URLField(blank=True, verbose_name='bookmark_image'),
                ),
                (
                    'collection',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='bookmarks',
                        to='bookmarks.collection',
                        verbose_name='collection',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='bookmarks',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='user',
                    ),
                ),
            ],
            options={
                'verbose_name': 'bookmark',
                'verbose_name_plural': 'bookmarks',
                'db_table': 'bookmarks"."bookmark',
                'ordering': ['title', 'link'],
            },
        ),
    ]
