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

from users.views import WorkerProfileView, EmployerProfileView, ModeratorProfileView, UserLoginView, UserRegisterView, \
    UserLogoutView, EmployersProfileView, EmployerDetailView, UserEmailVarifyView, UserVarifyStatusView, \
    PassResetView, \
    PassResetDoneView, PassResetConfirmView, PassResetCompletedView, ModerationAwaiting, ModeratorCompaniesList, \
    edit_comp_list, ModeratorCompanyUpdate, set_public_status

app_name = 'users'

urlpatterns = [
    path('worker_profile/<int:pk>/', WorkerProfileView.as_view(), name='worker_profile'),
    path('employers/', EmployersProfileView.as_view(), name='employers'),
    path('employer/<int:pk>', EmployerDetailView.as_view(), name='employers_detail'),
    path('employer_profile/<int:pk>/', EmployerProfileView.as_view(), name='employer_profile'),
    path('moderator_profile/<int:pk>/', ModeratorProfileView.as_view(), name='moderator_profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegisterView.as_view(), name='registration'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('verify/<str:username>/<str:email>/<str:activation_key>/', UserRegisterView.verify, name='verify'),
    path('verify_status', UserVarifyStatusView.as_view(), name='verify_status'),
    path('email_verify', UserEmailVarifyView.as_view(), name='email_verify'),
    path('password_reset/', PassResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PassResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', PassResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/', PassResetCompletedView.as_view(),
         name='password_reset_complete'),

    path('moderation_awaiting/', ModerationAwaiting.as_view(), name='moderation_awaiting'),

    path('moderator_company_approve/<int:pk>/', ModeratorCompanyUpdate.as_view(), name='moderator_company_approve'),
    path('moderator_companies_list/', ModeratorCompaniesList.as_view(), name='moderator_companies_list'),
    path('edit_comp_list/<str:stat>/', edit_comp_list, name='edit_comp_list'),
    path('distribute_company/<int:pk>/', set_public_status, name='distribute_company'),

]
