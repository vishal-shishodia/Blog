from django.urls import path
from .views import *

urlpatterns = [
    path('', index,name='index'),
    path('blog/',Blog,name='blog'),
    path('search/',search,name='search'),
    path('create/',PostCreate,name='create'),
    path('detail/<str:pk>/',PostDetail,name='detail'),
    path('update/<str:pk>/',PostUpdate,name='update'),
    path('delete/<str:pk>/',PostDelete,name='delete'),
   ]