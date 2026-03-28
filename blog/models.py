from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
import math


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})


class Series(models.Model):
    """Groups of related posts (e.g. 'Field Reflections', 'Plant Studies')"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='series/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Series'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:series', kwargs={'slug': self.slug})


class Post(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
    ]

    TONE_ESSAY = 'essay'
    TONE_JOURNAL = 'journal'
    TONE_ARTICLE = 'article'
    TONE_CHOICES = [
        (TONE_ESSAY, 'Essay'),
        (TONE_JOURNAL, 'Journal'),
        (TONE_ARTICLE, 'Article'),
    ]

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True, max_length=320)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    series_order = models.PositiveIntegerField(null=True, blank=True)

    featured_image = models.ImageField(upload_to='blog/featured/', blank=True, null=True)
    featured_image_caption = models.CharField(max_length=300, blank=True)

    excerpt = models.TextField(max_length=500, blank=True, help_text='Short preview shown on list pages')
    body = models.TextField()

    tone = models.CharField(max_length=20, choices=TONE_CHOICES, default=TONE_ARTICLE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)

    # Blog–Grimoire connection
    referenced_plants = models.ManyToManyField(
        'grimoire.Plant',
        blank=True,
        related_name='blog_posts',
        help_text='Plants mentioned or featured in this post'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    @property
    def reading_time(self):
        """Estimated reading time in minutes (avg 200 wpm)."""
        word_count = len(self.body.split())
        minutes = math.ceil(word_count / 200)
        return max(1, minutes)

    @property
    def is_published(self):
        return self.status == self.STATUS_PUBLISHED
