"""GB_concept URL Configuration

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
from django.urls import path

from news.views import NewsCreate, NewsUpdate, NewsDelete, NewsModerateList, NewsListView, NewsDetailView

app_name = 'news'

urlpatterns = [
    path('all/', NewsModerateList.as_view(), name='moderate_news'),
    path('list/', NewsListView.as_view(), name='list_news'),
    path('detail/<int:pk>/', NewsDetailView.as_view(), name='detail_news'),
    path('create/', NewsCreate.as_view(), name='create_news'),
    path('update/<int:pk>/', NewsUpdate.as_view(), name='update_news'),
    path('delete/<int:pk>/', NewsDelete.as_view(), name='delete_news'),

]
