"""
URL configuration for lookupAgency project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from lookupAgencyApp import views
from .sitemaps import PostsSitemap, PagesSitemap

sitemaps = {
    'blogposts': PostsSitemap,
    'categories': PagesSitemap,
}

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('case/', views.case, name='case'),
    path('case/<slug:slug>/', views.case_detail, name='case_detail'),
    path('<slug:slug>/', views.static_pages, name='static_pages'),
    path('search/', views.search, name='search'),
    path('tag/<slug:tag_slug>/', views.posts_by_tag, name='posts_by_tag'),
]
