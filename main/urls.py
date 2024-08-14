from .import views
from django.urls import path
urlpatterns = [
    path('', views.search_view, name='search_view'),
]
