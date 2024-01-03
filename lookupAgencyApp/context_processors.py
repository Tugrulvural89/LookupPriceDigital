from .models import Tags, Post


def blog_pages(request):
    blog_content = Post.objects.filter(is_published=True, types='blog')[0:4]
    case_content = Post.objects.filter(is_published=True, types='case')[0:4]
    return {'blog_content': blog_content, 'case_content': case_content}
