from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('off/', views.off, name='off'),
    path('login/', views.login, name='login'),
    path('select/', views.select, name='select'),
    path('taken/', views.taken, name='taken'),
    path('', views.homepage, name='homepage'),
  #  path('basket', views.basket, name='basket'),
    url(r'^basket(?P<book_id>[\w-]+)', views.basket, name="basket"),
    path('basket/', views.basket_direct, name='direct'),
    path('<str:book_title>/', views.detail, name='detail'),
    path('basket/map', views.map, name='map'),
]