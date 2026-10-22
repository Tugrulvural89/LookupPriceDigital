from django.core.paginator import Paginator
from html import unescape

from django.db.models import Q
from django.utils.html import escape, strip_tags
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
    # The form lives at the end of the homepage now.
    return redirect('/#contact', permanent=True)


def _plain(html_text, limit=155):
    text = ' '.join(unescape(strip_tags(html_text)).split())
    return text if len(text) <= limit else text[:limit - 1].rsplit(' ', 1)[0] + '…'


def _page(request, queryset):
    return Paginator(queryset, 12).get_page(request.GET.get('page'))


def _post_list(request, posts, **ctx):
    return render(request, 'post_list.html', {'posts': _page(request, posts), **ctx})


def blog(request, *args, **kwargs):
    return _post_list(
        request, Post.objects.filter(is_published=True, types='blog').order_by('-created'),
        section='blog', eyebrow='Blog', heading='Notes on <span class="glow">ads, AI and growth.</span>',
        page_title='Blog: Ads, AI and E-commerce Growth | Lookup Price',
        page_description='Practical notes from Lookup Price on Google and Meta ads, AI product content, Shopify apps and e-commerce growth, written from client work.',
        lede='What we learn running ads, building AI tools and shipping our own products.',
        empty_text='No articles yet.')


def case(request, *args, **kwargs):
    return _post_list(
        request, Post.objects.filter(is_published=True, types='case').order_by('-created'),
        section='case', eyebrow='Cases', heading='Work we <span class="glow">shipped.</span>',
        page_title='Case Studies: Apps, Ads and AI Work | Lookup Price',
        page_description='Case studies from Lookup Price: mobile apps, ad campaigns, AI tooling and product content we designed, built and launched for clients and ourselves.',
        lede='Apps, campaigns and AI products, from brief to launch.',
        empty_text='No cases yet.')


def search(request):
    query = (request.GET.get('query') or '').strip()
    posts = Post.objects.none()
    if len(query) > 3:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query), is_published=True).order_by('-created')
    return _post_list(
        request, posts, query=query, noindex=True, eyebrow='Search',
        heading='Results for “%s”' % escape(query) if query else 'Search',
        page_title='Search | Lookup Price', page_description='Search Lookup Price articles and case studies.',
        empty_text='Nothing found. Try a longer or different word.' if query else 'Type at least four letters.')


def posts_by_tag(request, tag_slug):
    tag = get_object_or_404(Tags, slug=tag_slug)
    return _post_list(
        request, Post.objects.filter(tags=tag, is_published=True).order_by('-created'),
        noindex=True, eyebrow='Tag', heading=escape(tag.title),
        page_title='%s | Lookup Price' % tag.title, page_description='Lookup Price articles and cases about %s.' % tag.title,
        empty_text='Nothing tagged yet.')


def _post_detail(request, slug, types):
    post = get_object_or_404(Post, slug=slug, is_published=True, types=types)
    url = BASE_URL + post.get_absolute_url()
    list_name, list_path = ('Blog', '/blog/') if types == 'blog' else ('Cases', '/case/')
    schema = [{
        '@context': 'https://schema.org',
        '@type': 'BlogPosting' if types == 'blog' else 'Article',
        'headline': post.title[:110],
        'description': _plain(post.content),
        'image': [BASE_URL + post.image.url] if post.image else [],
        'datePublished': post.created.isoformat(),
        'dateModified': post.updated.isoformat(),
        'author': {'@type': 'Person', 'name': post.author.name if post.author else 'Kasım Tuğrul Vural'},
        'publisher': {'@type': 'Organization', 'name': 'Lookup Price', 'url': BASE_URL + '/',
                      'logo': {'@type': 'ImageObject', 'url': BASE_URL + '/static/logos/mylogo.png'}},
        'mainEntityOfPage': url,
    }, {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE_URL + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': list_name, 'item': BASE_URL + list_path},
            {'@type': 'ListItem', 'position': 3, 'name': post.title, 'item': url},
        ],
    }]
    if len(post.title) <= 45:
        seo_title = '%s | Lookup Price' % post.title
    else:  # long headlines keep their words and drop the brand
        seo_title = post.title if len(post.title) <= 60 else post.title[:60].rsplit(' ', 1)[0]
    return render(request, 'post_detail.html', {
        'post': post, 'section': types, 'list_name': list_name, 'list_url': list_path,
        'seo_title': seo_title, 'seo_description': _plain(post.content),
        'related': Post.objects.filter(is_published=True).exclude(pk=post.pk).order_by('-created')[:3],
        'schema': json.dumps(schema, ensure_ascii=False).replace('</', '<\\/'),
    })


def blog_detail(request, slug=None, *args, **kwargs):
    return _post_detail(request, slug, 'blog')


def case_detail(request, slug=None, *args, **kwargs):
    return _post_detail(request, slug, 'case')


def static_pages(request, slug=None, *args, **kwargs):
    post = get_object_or_404(StaticPages, slug=slug, is_published=True)
    return render(request, 'pages.html', {'post': post, 'seo_description': _plain(post.content)})
