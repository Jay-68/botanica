from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Post, Category, Tag, Series


def post_list(request):
    posts = Post.objects.filter(status=Post.STATUS_PUBLISHED).select_related('author', 'category')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    series_list = Series.objects.all()

    # Search
    q = request.GET.get('q', '')
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(body__icontains=q) | Q(excerpt__icontains=q))

    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'series_list': series_list,
        'search_query': q,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.STATUS_PUBLISHED)
    related_posts = Post.objects.filter(
        status=Post.STATUS_PUBLISHED,
        category=post.category
    ).exclude(pk=post.pk)[:3]

    # Series navigation
    series_posts = None
    if post.series:
        series_posts = post.series.posts.filter(
            status=Post.STATUS_PUBLISHED
        ).order_by('series_order')

    context = {
        'post': post,
        'related_posts': related_posts,
        'series_posts': series_posts,
        'referenced_plants': post.referenced_plants.all(),
    }
    return render(request, 'blog/post_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status=Post.STATUS_PUBLISHED, category=category)
    context = {'category': category, 'posts': posts}
    return render(request, 'blog/category_detail.html', context)


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(status=Post.STATUS_PUBLISHED, tags=tag)
    context = {'tag': tag, 'posts': posts}
    return render(request, 'blog/tag_detail.html', context)


def series_detail(request, slug):
    series = get_object_or_404(Series, slug=slug)
    posts = series.posts.filter(status=Post.STATUS_PUBLISHED).order_by('series_order')
    context = {'series': series, 'posts': posts}
    return render(request, 'blog/series_detail.html', context)
