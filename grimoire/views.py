from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Plant, PlantProperty, PlantFamily, ObservationLog
import random


def plant_list(request):
    plants = Plant.objects.select_related('family').prefetch_related('properties')

    # Search
    q = request.GET.get('q', '')
    if q:
        plants = plants.filter(
            Q(scientific_name__icontains=q) |
            Q(common_names__icontains=q) |
            Q(overview__icontains=q)
        )

    # Filter by property
    prop_slug = request.GET.get('property', '')
    active_property = None
    if prop_slug:
        active_property = get_object_or_404(PlantProperty, slug=prop_slug)
        plants = plants.filter(properties=active_property)

    # Filter by habitat
    habitat_filter = request.GET.get('habitat', '')
    if habitat_filter:
        plants = plants.filter(habitat__icontains=habitat_filter)

    # Filter by edibility
    edibility_filter = request.GET.get('edibility', '')
    if edibility_filter:
        plants = plants.filter(edibility=edibility_filter)

    # Alphabetical grouping
    letter = request.GET.get('letter', '')
    if letter:
        plants = plants.filter(scientific_name__istartswith=letter)

    all_properties = PlantProperty.objects.all()
    all_families = PlantFamily.objects.all()
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    context = {
        'plants': plants,
        'all_properties': all_properties,
        'all_families': all_families,
        'search_query': q,
        'active_property': active_property,
        'alphabet': alphabet,
        'active_letter': letter,
        'edibility_choices': Plant.EDIBILITY_CHOICES,
        'active_edibility': edibility_filter,
    }
    return render(request, 'grimoire/plant_list.html', context)


def plant_detail(request, slug):
    plant = get_object_or_404(Plant, slug=slug)
    observations = plant.observations.all()
    images = plant.images.all()
    related_posts = plant.blog_posts.filter(status='published')[:4]
    related_plants = plant.related_plants.all()[:6]

    context = {
        'plant': plant,
        'observations': observations,
        'images': images,
        'related_posts': related_posts,
        'related_plants': related_plants,
        'has_practical': any([plant.uses_medicinal, plant.uses_culinary, plant.uses_other, plant.preparation_methods]),
        'has_observational': any([plant.field_notes, plant.locations_observed, plant.seasonal_patterns]),
        'has_symbolic': any([plant.symbolism, plant.energetic_qualities, plant.personal_reflections]),
    }
    return render(request, 'grimoire/plant_detail.html', context)


def property_detail(request, slug):
    prop = get_object_or_404(PlantProperty, slug=slug)
    plants = prop.plants.all()
    context = {'property': prop, 'plants': plants}
    return render(request, 'grimoire/property_detail.html', context)


def random_plant(request):
    """Redirect to a random plant entry."""
    from django.shortcuts import redirect
    pks = Plant.objects.values_list('pk', flat=True)
    if pks:
        pk = random.choice(list(pks))
        plant = Plant.objects.get(pk=pk)
        return redirect(plant.get_absolute_url())
    return redirect('grimoire:plant_list')
