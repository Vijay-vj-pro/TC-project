from django.urls import path
from . import views

urlpatterns = [
    path('imageUpload/',views.imageUpload,name='imageUpload'),
    path('',views.search_view,name='search_view'),
    path('image/<int:id>/',views.image_detail,name='image_detail'),
    path('upload_year/',views.year_fun,name='upload_year'),
    path('login/',views.login_fun,name='login'),
]

