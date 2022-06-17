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

from cvs.views import CVList, CVCreate, CVUpdate, CVDelete, CVDistribute, ModeratorCVList, ModeratorCVUpdate
from news.views import NewsCreate, NewsUpdate, NewsDelete, NewsModerateList

app_name = 'cv'

urlpatterns = [
    path('all/', CVList.as_view(), name='cv_list'),
    path('create/', CVCreate.as_view(), name='create_cv'),
    path('update/<int:pk>/', CVUpdate.as_view(), name='update_cv'),
    path('delete/<int:pk>/', CVDelete.as_view(), name='delete_cv'),
    path('distribute/<int:pk>/', CVDistribute.as_view(), name='distribute_cv'),

    path('moderator_cvs/', ModeratorCVList.as_view(), name='moderator_cvs_list'),
    path('moderator_vacancy_approve/<int:pk>/', ModeratorCVUpdate.as_view(), name='moderator_cvs_approve'),

]
