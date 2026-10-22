from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from lookupAgencyApp.forms import ContactForm
from lookupAgencyApp.models import Post, Tags, StaticPages
from lookupAgencyApp.home_content import CONTENT
import json


# Create your views here.

BASE_URL = 'https://www.lookupprice.com'
HOME_URLS = {'en': '/', 'es': '/es/', 'tr': '/tr/'}
SHOT_IMGS = ['tryon', 'turntable', 'film', 'banner', 'living', 'scene']


def index(request, lang='en'):
    t = CONTENT[lang]
    home_url = HOME_URLS[lang]
    posted, error = {}, False
    if request.method == 'POST':
        posted = {k: request.POST.get(k, '').strip() for k in ('name', 'email', 'company', 'phone', 'msg')}
        if request.POST.get('website'):  # honeypot: bots fill every field
            return redirect(home_url + '?sent=1#contact')
        needs = request.POST.getlist('need')
        content = (('Needs: ' + ', '.join(needs) + '\n\n') if needs else '') + posted['msg']
        form = ContactForm({**posted, 'content': content or '-'})
        if form.is_valid():
            form.save()
            return redirect(home_url + '?sent=1#contact')
        error = True
    schema = {
        '@context': 'https://schema.org',
        '@type': 'ProfessionalService',
        'name': 'Lookup Price',
        'url': BASE_URL + '/',
        'image': BASE_URL + '/static/home/og.jpg',
        'logo': BASE_URL + '/static/logos/mylogo.png',
        'description': t['description'],
        'founder': {'@type': 'Person', 'name': 'Kasım Tuğrul Vural'},
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Barcelona', 'addressCountry': 'ES'},
        'areaServed': ['ES', 'TR', 'FR', 'EU'],
        'knowsLanguage': ['en', 'es', 'tr'],
        'knowsAbout': ['Google Ads', 'Meta Ads', 'ChatGPT ads', 'AI model deployment',
                       'Claude and OpenAI plugins', 'Product video production', 'Product photography', 'Shopify apps'],
        'sameAs': ['https://shoupapp.com'],
    }
    context = {
        't': t, 'lang': lang, 'home_url': home_url,
        'base_url': BASE_URL, 'canonical': BASE_URL + home_url,
        'alternates': [(code, BASE_URL + url) for code, url in HOME_URLS.items()],
        'lang_links': list(HOME_URLS.items()),
        'shots': [(*shot, 'home/%s.webp' % img) for shot, img in zip(t['shots'], SHOT_IMGS)],
        'stack_imgs': ['home/%s.webp' % i for i in ('tryon', 'turntable', 'film', 'banner', 'scene')],
        'schema': json.dumps(schema, ensure_ascii=False).replace('</', '<\\/'),
        'posted': posted, 'error': error, 'sent': request.GET.get('sent') == '1',
    }
    return render(request, 'home.html', context)


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
