from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [



    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^delete_book(?P<book_id>[\w-]+)', views.delete_book, name="delete_book"),
    #path('websocket/', views.websocket_page, name='websocket_page'),
    path('add_book/', views.add_book, name='add_book'),
    path('off/', views.off, name='off'),
    path('taken/', views.taken, name='taken'),
    path('', views.homepage, name='homepage'),
    path('basket/', views.basket, name='basket'),
    path('<str:book_title>/', views.detail, name='detail'),
    path('basket/map', views.map, name='map'),
    path('basket/map/leds/', views.leds, name='leds'),

    url(r'^leds_off(?P<book_id>[\w-]+)', views.leds_off, name="leds_off"),
    url(r'^update(?P<book_id>[\w-]+)', views.update_basket, name="update_basket"),
    url(r'^delete(?P<book_id>[\w-]+)', views.delete_basket, name="delete_basket"),


]

