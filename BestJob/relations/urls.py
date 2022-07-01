from django.urls import path

from .views import LastListView, RelationDetailView, RelationChangeStatusView, RelationCreateView

app_name = 'relations'

urlpatterns = [
    path('list/', LastListView.as_view(), name='list'),
    path('detail/<int:relation_id>/', RelationDetailView.as_view(), name='detail'),
    path('change/<int:relation_id>/<int:status_id>/', RelationChangeStatusView.as_view(), name='change'),
    path('create/<int:vacancy_id>/<int:cv_id>/', RelationCreateView.as_view(), name='create'),
]