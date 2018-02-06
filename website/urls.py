from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('select/', views.select, name='select'),
    path('taken/', views.taken, name='taken'),
    path('', views.homepage, name='homepage'),
    path('<str:book_title>/', views.detail, name='detail'),
    path('<str:book_title>/take/', views.take, name='take'),
    path('<str:book_title>/return/', views.return_, name='return'),
    path('<str:book_title>/off/', views.off, name='off'),
]