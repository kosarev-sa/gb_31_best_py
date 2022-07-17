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

from cvs.views import CVList, CVCreate, CVUpdate, CVDelete, set_public_status, CVExperienceCreate, CVExperienceUpdate, \
    CVExperienceDelete, CVEducationCreate, CVEducationUpdate, CVEducationDelete, CVLanguageCreate, CVLanguageUpdate, \
    CVLanguageDelete, ModeratorCVList, ModeratorCVUpdate, CVDetailView, edit_cv_list, RecomendedCVList

app_name = 'cv'

urlpatterns = [
    path('all/', CVList.as_view(), name='cv_list'),
    path('create/', CVCreate.as_view(), name='create_cv'),
    path('update/<int:pk>/', CVUpdate.as_view(), name='update_cv'),
    path('delete/<int:pk>/', CVDelete.as_view(), name='delete_cv'),
    path('detail/<int:pk>/', CVDetailView.as_view(), name='detail_cv'),
    path('distribute/<int:pk>/', set_public_status, name='distribute_cv'),
    path('create_experience/<int:pk>', CVExperienceCreate.as_view(), name='create_experience'), # здесь pk - это cv.id
    path('update_experience/<int:pk>/', CVExperienceUpdate.as_view(), name='update_experience'), # а здесь pk - это experience.id
    path('delete_experience/<int:pk>/', CVExperienceDelete.as_view(), name='delete_experience'),
    path('create_education/<int:cv_id>/', CVEducationCreate.as_view(), name='create_education'),
    path('update_education/<int:pk>/', CVEducationUpdate.as_view(), name='update_education'),
    path('delete_education/<int:pk>/', CVEducationDelete.as_view(), name='delete_education'),
    path('create_language/<int:cv_id>/', CVLanguageCreate.as_view(), name='create_language'),
    path('update_language/<int:pk>/', CVLanguageUpdate.as_view(), name='update_language'),
    path('delete_language/<int:pk>/', CVLanguageDelete.as_view(), name='delete_language'),
    path('moderator_cvs/', ModeratorCVList.as_view(), name='moderator_cvs_list'),
    path('moderator_cvs_approve/<int:pk>/', ModeratorCVUpdate.as_view(), name='moderator_cvs_approve'),
    path('edit_cv_list/<str:stat>/', edit_cv_list, name='edit_cv_list'),
    path('cv_recommended/<int:pk>/', RecomendedCVList.as_view(), name='cv_recommended'),

]
