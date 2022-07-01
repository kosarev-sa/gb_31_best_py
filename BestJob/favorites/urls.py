from django.urls import path

from .views import FavoritesCreateView, FavoritesDeleteView, FavoritesListView

app_name = 'favorites'

urlpatterns = [
    path('add/', FavoritesCreateView.as_view(), name='add'),
    path('delete/<int:pk>/', FavoritesDeleteView.as_view(), name='delete'),
    path('list/', FavoritesListView.as_view(), name='list'),
]