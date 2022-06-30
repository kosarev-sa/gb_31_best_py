from django.urls import path

from .views import LastListView, RelationDetailView, RelationStatusView

app_name = 'relations'

urlpatterns = [
    path('last_list/', LastListView.as_view(), name='last_list'),
    path('relation_detail/<int:relation_id>/', RelationDetailView.as_view(), name='relation_detail'),
    path('relation_status/<int:relation_id>/<int:status_id>/', RelationStatusView.as_view(), name='relation_status'),
]