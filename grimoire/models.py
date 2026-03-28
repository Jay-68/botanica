from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class PlantFamily(models.Model):
    name = models.CharField(max_length=200, help_text='e.g. Lamiaceae')
    common_name = models.CharField(max_length=200, blank=True, help_text='e.g. Mint family')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Plant Families'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.common_name})" if self.common_name else self.name


class PlantProperty(models.Model):
    """Tag-like attributes: medicinal, edible, toxic, aromatic, dye, etc."""
    CATEGORY_CHOICES = [
        ('use', 'Use'),
        ('habitat', 'Habitat'),
        ('quality', 'Quality'),
        ('season', 'Season'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='use')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Plant Properties'
        ordering = ['category', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} [{self.get_category_display()}]"

    def get_absolute_url(self):
        return reverse('grimoire:property', kwargs={'slug': self.slug})


class Plant(models.Model):
    """Core grimoire entity — each plant is a complete, self-contained page of knowledge."""

    # ── Layer 1: Scientific Foundation ──────────────────────────────────────
    scientific_name = models.CharField(max_length=300, unique=True)
    common_names = models.CharField(max_length=500, help_text='Comma-separated common names')
    slug = models.SlugField(unique=True, blank=True, max_length=320)
    family = models.ForeignKey(PlantFamily, on_delete=models.SET_NULL, null=True, blank=True, related_name='plants')

    # Taxonomy
    kingdom = models.CharField(max_length=100, default='Plantae')
    order = models.CharField(max_length=100, blank=True)
    genus = models.CharField(max_length=100, blank=True)
    species = models.CharField(max_length=100, blank=True)

    overview = models.TextField(help_text='General description and significance')

    # ── Layer 2: Scientific Description ─────────────────────────────────────
    morphology = models.TextField(blank=True, help_text='Physical description: leaves, stems, flowers, roots')
    habitat = models.TextField(blank=True, help_text='Where it grows, soil, climate, altitude')
    distribution = models.TextField(blank=True, help_text='Geographic range')
    bloom_season = models.CharField(max_length=200, blank=True)

    # ── Layer 3: Practical Knowledge ────────────────────────────────────────
    EDIBILITY_CHOICES = [
        ('edible', 'Edible'),
        ('medicinal', 'Medicinal'),
        ('toxic', 'Toxic'),
        ('caution', 'Use with Caution'),
        ('unknown', 'Unknown'),
    ]
    edibility = models.CharField(max_length=20, choices=EDIBILITY_CHOICES, default='unknown')

    uses_medicinal = models.TextField(blank=True, help_text='Medicinal uses and traditional applications')
    uses_culinary = models.TextField(blank=True, help_text='Culinary and edible uses')
    uses_other = models.TextField(blank=True, help_text='Dye, craft, ecological, spiritual, etc.')
    preparation_methods = models.TextField(blank=True, help_text='How to prepare: teas, tinctures, poultices, etc.')
    warnings = models.TextField(blank=True, help_text='Toxicity, contraindications, look-alikes')

    # ── Layer 4: Observational / Personal ───────────────────────────────────
    field_notes = models.TextField(blank=True, help_text='Personal observations in the field')
    locations_observed = models.TextField(blank=True, help_text='Where you have personally seen this plant')
    seasonal_patterns = models.TextField(blank=True, help_text='When it appears, peaks, and fades')

    # ── Layer 5: Symbolic / Energetic (Optional but powerful) ───────────────
    symbolism = models.TextField(blank=True, help_text='Cultural and historical symbolism')
    energetic_qualities = models.TextField(blank=True, help_text='Traditional energetic or elemental associations')
    personal_reflections = models.TextField(blank=True, help_text='Your personal relationship with this plant')

    # ── Properties & Relations ──────────────────────────────────────────────
    properties = models.ManyToManyField(PlantProperty, blank=True, related_name='plants')
    related_plants = models.ManyToManyField('self', blank=True, symmetrical=True)

    # ── Media ────────────────────────────────────────────────────────────────
    primary_image = models.ImageField(upload_to='grimoire/plants/', blank=True, null=True)

    # ── Meta ─────────────────────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['scientific_name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.scientific_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.scientific_name

    def get_absolute_url(self):
        return reverse('grimoire:plant_detail', kwargs={'slug': self.slug})

    @property
    def primary_common_name(self):
        names = [n.strip() for n in self.common_names.split(',') if n.strip()]
        return names[0] if names else self.scientific_name

    @property
    def all_common_names(self):
        return [n.strip() for n in self.common_names.split(',') if n.strip()]


class PlantImage(models.Model):
    """Additional images for the gallery on a plant page."""
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='grimoire/gallery/')
    caption = models.CharField(max_length=300, blank=True)
    credit = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.plant.scientific_name} — image {self.order}"


class ObservationLog(models.Model):
    """Dated field observations — the living diary of encounters."""
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='observations')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    location = models.CharField(max_length=300)
    coordinates = models.CharField(max_length=100, blank=True, help_text='lat,lon e.g. -1.2921,36.8219')
    notes = models.TextField()
    image = models.ImageField(upload_to='grimoire/observations/', blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.plant} observed on {self.date} at {self.location}"

    @property
    def lat(self):
        if self.coordinates:
            try:
                return float(self.coordinates.split(',')[0])
            except Exception:
                return None

    @property
    def lon(self):
        if self.coordinates:
            try:
                return float(self.coordinates.split(',')[1])
            except Exception:
                return None
