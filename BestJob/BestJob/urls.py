"""BestJob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import news.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', news.views.NewsView.as_view(), name='index'),
    path('news/', include('news.urls', namespace='news')),
    path('users/', include('users.urls', namespace='users')),
    path('cvs/', include('cvs.urls', namespace='cvs')),
    path('vacancies/', include('vacancies.urls', namespace='vacancies')),
    path('search/', include('haystack.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
