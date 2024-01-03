from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.


class Navigation(models.Model):
    title = models.CharField(max_length=100)
    href = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Tags(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Tags, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Post(models.Model):
    TYPE_CHOICES = (
        ('blog', 'Blog'),
        ('case', 'Case'),
    )
    title = models.CharField(max_length=200)
    content = RichTextField()
    is_published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tags, blank=True)
    image = models.ImageField(upload_to='images/')
    types = models.CharField(choices=TYPE_CHOICES, max_length=100, default='blog')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    # Author modeline ForeignKey olarak eklenen yeni alan
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        if self.types == 'blog':
            return reverse('blog_detail', kwargs={'slug': self.slug})
        else:
            return reverse('case_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Works(models.Model):
    title = models.CharField(max_length=200)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    phone = models.CharField(max_length=100)
    content = models.TextField()
    company = models.CharField(max_length=250)
    works = models.ManyToManyField(Works, blank=True)

    def __str__(self):
        return self.name


class StaticPages(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    is_published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=200, unique=True)

    def get_absolute_url(self):
        return reverse('static_pages', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(StaticPages, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
