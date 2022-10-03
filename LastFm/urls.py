from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_top_artists, name='top_artists'),
]