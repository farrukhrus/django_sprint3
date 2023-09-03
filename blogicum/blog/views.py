from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category
from django.utils import timezone


def index(request):
    template = "blog/index.html"
    current_time = timezone.now()
    post_list = (
        Post.objects
        .select_related("author", "location", "category")
        .filter(
            pub_date__lte=current_time,
            is_published=True,
            category__is_published=True,
        )
        .order_by("pub_date")[:5]
    )
    context = {"post_list": post_list}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = "blog/category.html"
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    post_list = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category=category
    )
    context = {"category": category, "post_list": post_list}
    return render(request, template, context)


def post_detail(request, pk):
    template = "blog/detail.html"
    post = get_object_or_404(
        Post.objects.select_related().filter(
            pk=pk,
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )
    )
    context = {"post": post}
    return render(request, template, context)
