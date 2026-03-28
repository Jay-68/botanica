from django.contrib import admin
from .models import Post, Category, Tag, Series


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'tone', 'published_at', 'reading_time']
    list_filter = ['status', 'tone', 'category', 'tags', 'series']
    search_fields = ['title', 'body', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags', 'referenced_plants']
    date_hierarchy = 'published_at'
    readonly_fields = ['reading_time']
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'tone', 'excerpt', 'body')
        }),
        ('Media', {
            'fields': ('featured_image', 'featured_image_caption')
        }),
        ('Classification', {
            'fields': ('category', 'tags', 'series', 'series_order')
        }),
        ('Grimoire Links', {
            'fields': ('referenced_plants',),
            'description': 'Link this post to plant entries in the Grimoire'
        }),
        ('Publishing', {
            'fields': ('status', 'published_at')
        }),
    )
