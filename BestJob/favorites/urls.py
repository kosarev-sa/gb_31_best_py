from django.urls import path

from .views import FavoritesCreateView, FavoritesWorkerListView, FavoritesEmployerListView, FavoritesWorkerDeleteView, \
    FavoritesEmployerDeleteView

app_name = 'favorites'

urlpatterns = [
    path('add/', FavoritesCreateView.as_view(), name='add'),
    path('worker_delete/<int:pk>/', FavoritesWorkerDeleteView.as_view(), name='worker_delete'),
    path('employer_delete/<int:pk>/', FavoritesEmployerDeleteView.as_view(), name='employer_delete'),
    path('worker_list/', FavoritesWorkerListView.as_view(), name='worker_list'),
    path('employer_list/', FavoritesEmployerListView.as_view(), name='employer_list'),
]