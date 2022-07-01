from django.urls import path

from .views import FavoritesCreateView, FavoritesDeleteView, FavoritesWorkerListView, FavoritesEmployerListView

app_name = 'favorites'

urlpatterns = [
    path('add/', FavoritesCreateView.as_view(), name='add'),
    path('delete/<int:pk>/', FavoritesDeleteView.as_view(), name='delete'),
    path('worker_list/', FavoritesWorkerListView.as_view(), name='worker_list'),
    path('employer_list/', FavoritesEmployerListView.as_view(), name='employer_list'),
]