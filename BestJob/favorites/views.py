from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, DeleteView, ListView

class FavoritesCreateView(CreateView):
    pass

class FavoritesDeleteView(DeleteView):
    pass

class FavoritesListView(ListView):
    pass
