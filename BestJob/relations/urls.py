from django.urls import path

from .views import RelationHistoryDetailView, LastListView, RelationDetailView

app_name = 'relations'

urlpatterns = [
    path('current/', RelationHistoryDetailView.as_view(), name='current'),
    # TODO: переделать на:
    path('last_list/', LastListView.as_view(), name='last_list'),
    path('relation_detail/<int:relation_id>/', RelationDetailView.as_view(), name='relation_detail'),
]