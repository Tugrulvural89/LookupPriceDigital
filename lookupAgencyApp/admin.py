from django.contrib import admin
from .models import Navigation, Tags, Author, Post, Works, Contact, StaticPages

# Modelinizi yönetim paneline kaydedin.
admin.site.register(Navigation)
admin.site.register(Tags)
admin.site.register(Author)


# Özelleştirilmiş bir admin sınıfı ile Post modelini kaydedin.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created', 'updated')
    list_filter = ('is_published', 'created')
    search_fields = ('title', 'content')
    date_hierarchy = 'created'
    ordering = ('-created',)


# Works modeli için basit bir kayıt.
admin.site.register(Works)


# Contact modeli için özelleştirilmiş admin sınıfı.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'company')
    search_fields = ('name', 'email', 'company')


@admin.register(StaticPages)
class StaticPagesAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created', 'updated')
    list_filter = ('is_published', 'created')
    search_fields = ('title', 'content')
    date_hierarchy = 'created'
    ordering = ('-created',)
