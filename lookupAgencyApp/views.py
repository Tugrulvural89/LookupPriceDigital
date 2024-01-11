from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from lookupAgencyApp.forms import ContactForm
from lookupAgencyApp.models import Post, Tags, StaticPages


# Create your views here.

def index(request, *args, **kwargs):
    blogs = Post.objects.filter(is_published=True, types='blog')[0:3]
    cases = Post.objects.filter(is_published=True, types='case')[0:3]
    context = {
        'blogs': blogs,
        'cases': cases
    }
    return render(request, 'index.html', context)


def contact(request, *args, **kwargs):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        print(request.POST.dict())
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def blog(request, *args, **kwargs):
    posts = Post.objects.filter(is_published=True, types='blog').order_by('-created')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': page_obj
    }
    return render(request, 'blog.html', context)


def blog_detail(request, slug=None, *args, **kwargs):
    # Slug kullanarak postu getiriyoruz.
    post = get_object_or_404(Post, slug=slug, is_published=True, types='blog')
    # Context ile postu template'e gönderiyoruz.
    context = {
        'post': post
    }
    return render(request, 'blog_detail.html', context)


def case(request, *args, **kwargs):
    posts = Post.objects.filter(is_published=True, types='case').order_by('-created')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': page_obj
    }
    return render(request, 'case.html', context)


def case_detail(request, slug=None, *args, **kwargs):
    # Slug kullanarak postu getiriyoruz.
    post = get_object_or_404(Post, slug=slug, is_published=True, types='case')
    # Context ile postu template'e gönderiyoruz.
    context = {
        'post': post
    }
    return render(request, 'case_detail.html', context)


def search(request):
    post_query = request.GET.get('query')
    if post_query is not None:
        if len(post_query) > 3:
            posts = Post.objects.filter(title__icontains=post_query, content__icontains=post_query, is_published=True).order_by('-created')
            paginator = Paginator(posts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            page_obj = []
    else:
        page_obj = []
    return render(request, 'search_result.html', {'posts': page_obj, 'query': post_query})


def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tags, slug=tag_slug)
    posts = Post.objects.filter(tags=tag, is_published=True).order_by('-created')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'search_tags.html', {'posts': page_obj, 'tag': tag})


def static_pages(request, slug=None, *args, **kwargs):
    # Slug kullanarak postu getiriyoruz.
    post = get_object_or_404(StaticPages, slug=slug, is_published=True)
    # Context ile postu template'e gönderiyoruz.
    context = {
        'post': post
    }
    return render(request, 'pages.html', context)
