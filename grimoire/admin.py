from django.contrib import admin
from .models import Plant, PlantFamily, PlantProperty, PlantImage, ObservationLog


class PlantImageInline(admin.TabularInline):
    model = PlantImage
    extra = 1
    fields = ['image', 'caption', 'credit', 'order']


class ObservationLogInline(admin.TabularInline):
    model = ObservationLog
    extra = 0
    fields = ['date', 'location', 'coordinates', 'notes', 'image']


@admin.register(PlantFamily)
class PlantFamilyAdmin(admin.ModelAdmin):
    list_display = ['name', 'common_name']
    search_fields = ['name', 'common_name']


@admin.register(PlantProperty)
class PlantPropertyAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug']
    list_filter = ['category']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['scientific_name', 'primary_common_name', 'family', 'edibility', 'updated_at']
    list_filter = ['edibility', 'family', 'properties']
    search_fields = ['scientific_name', 'common_names', 'overview']
    prepopulated_fields = {'slug': ('scientific_name',)}
    filter_horizontal = ['properties', 'related_plants']
    inlines = [PlantImageInline, ObservationLogInline]
    fieldsets = (
        ('🌿 Identity', {
            'fields': ('scientific_name', 'slug', 'common_names', 'family', 'primary_image', 'created_by')
        }),
        ('🔬 Taxonomy', {
            'fields': ('kingdom', 'order', 'genus', 'species'),
            'classes': ('collapse',),
        }),
        ('📖 Overview', {
            'fields': ('overview',)
        }),
        ('🌱 Morphology & Habitat', {
            'fields': ('morphology', 'habitat', 'distribution', 'bloom_season'),
        }),
        ('⚗️ Practical Knowledge', {
            'fields': ('edibility', 'uses_medicinal', 'uses_culinary', 'uses_other',
                       'preparation_methods', 'warnings'),
        }),
        ('🗺️ Observations', {
            'fields': ('field_notes', 'locations_observed', 'seasonal_patterns'),
        }),
        ('✨ Symbolic Layer', {
            'fields': ('symbolism', 'energetic_qualities', 'personal_reflections'),
            'classes': ('collapse',),
        }),
        ('🔗 Relations', {
            'fields': ('properties', 'related_plants'),
        }),
    )


@admin.register(ObservationLog)
class ObservationLogAdmin(admin.ModelAdmin):
    list_display = ['plant', 'date', 'location', 'author']
    list_filter = ['date', 'author']
    search_fields = ['plant__scientific_name', 'location', 'notes']
    date_hierarchy = 'date'
