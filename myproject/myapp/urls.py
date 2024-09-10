from django.urls import path
from . import views

urlpatterns = [
    path('', views.imageUpload, name='imageUpload'),
    path('search/', views.search_view, name='search_view'),
    path('image/<int:id>/', views.image_detail, name='image_detail'),
]
