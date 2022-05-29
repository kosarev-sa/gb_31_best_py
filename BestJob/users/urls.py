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

from news.views import NewsCreate, NewsUpdate, NewsDelete, NewsModerateList
from users.views import EmployeeProfileView, EmployerProfileView, ModeratorProfileView, UserLoginView, UserRegisterView, \
    UserLogoutView

app_name = 'users'

urlpatterns = [
    path('employee_profile/<int:pk>/', EmployeeProfileView.as_view(), name='employee_profile'),
    path('employer_profile/<int:pk>/', EmployerProfileView.as_view(), name='employer_profile'),
    path('moderator_profile/<int:pk>/', ModeratorProfileView.as_view(), name='moderator_profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegisterView.as_view(), name='registration'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

]
