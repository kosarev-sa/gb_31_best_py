from django.urls import path, re_path

from .views import LastListView, RelationDetailView, RelationChangeStatusView, RelationCreateView, \
    RelationCreateFromValueView

app_name = 'relations'

urlpatterns = [
    path('list/', LastListView.as_view(), name='list'),
    path('detail/<int:relation_id>/', RelationDetailView.as_view(), name='detail'),
    path('change/<int:relation_id>/<int:status_id>/', RelationChangeStatusView.as_view(), name='change'),
    # path('create_from_val/<int:magic_id>/<int:select_picker_id>/<str:letter>/', RelationCreateFromValueView.as_view(), name='create_from_val'),
    re_path(r'^create_from_val/(?P<magic_id>\d+)/(?P<select_picker_id>\d+)/(?P<letter>[\w|\W]+)/$', RelationCreateFromValueView.as_view(), name='create_from_val'),
    path('create/', RelationCreateView.as_view(), name='create'),
]
