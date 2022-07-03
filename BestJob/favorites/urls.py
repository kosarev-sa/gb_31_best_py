from django.template.defaulttags import url
from django.urls import path, re_path

from .views import FavoritesWorkerListView, FavoritesEmployerListView, FavoritesWorkerDeleteView, \
    FavoritesEmployerDeleteView, fav_emp_add_remove, fav_work_add_remove

app_name = 'favorites'

urlpatterns = [

    # оставил себе регулярку, как передать url(link) в параметре c клиента.
    # re_path(r'^employer_add/(?P<cv_id>\d+)/(?P<search_url>[\w|\W]+)/$', fav_emp_create, name='employer_add'),
    # re_path(r'^worker_add/(?P<vacancy_id>\d+)/(?P<search_url>[\w|\W]+)/$', fav_work_create, name='worker_add'),

    path('employer_add_remove/<int:cv_id>/', fav_emp_add_remove, name='employer_add_remove'),
    path('worker_add_remove/<int:vacancy_id>/', fav_work_add_remove, name='worker_add_remove'),

    path('worker_delete/<int:pk>/', FavoritesWorkerDeleteView.as_view(), name='worker_delete'),
    path('employer_delete/<int:pk>/', FavoritesEmployerDeleteView.as_view(), name='employer_delete'),
    path('worker_list/', FavoritesWorkerListView.as_view(), name='worker_list'),
    path('employer_list/', FavoritesEmployerListView.as_view(), name='employer_list'),
]
