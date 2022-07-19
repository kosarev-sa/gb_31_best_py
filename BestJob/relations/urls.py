from django.urls import path, re_path

from .views import RelationListView, RelationDetailView, RelationCreateFromFavoritesView, \
    RelationCreateFromRelationView, RelationCreateFromRelationDetailView

app_name = 'relations'

urlpatterns = [
    path('list/', RelationListView.as_view(), name='list'),
    path('detail/<int:relation_id>/', RelationDetailView.as_view(), name='detail'),
    # Создание из favorites
    re_path(r'^create_from_fav/(?P<magic_id>\d+)/(?P<select_picker_id>\d+)/(?P<letter>[\w|\W]+)/$',
            RelationCreateFromFavoritesView.as_view(), name='create_from_fav'),
    # Создание из relation
    re_path(r'^create_from_rel/(?P<magic_id>\d+)/(?P<select_picker_id>\d+)/(?P<letter>[\w|\W]+)/$',
            RelationCreateFromRelationView.as_view(), name='create_from_rel'),
    # Создание из relation detail
    re_path(r'^create_from_detail/(?P<magic_id>\d+)/(?P<select_picker_id>\d+)/(?P<letter>[\w|\W]+)/$',
            RelationCreateFromRelationDetailView.as_view(), name='create_from_detail'),
]
