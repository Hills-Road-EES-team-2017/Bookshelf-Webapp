from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('select/', views.select, name='select'),
    path('taken/', views.taken, name='taken'),
    path('homepage/', views.homepage, name='homepage'),
    path('<str:book_title>/', views.detail, name='detail'),
    path('<str:book_title>/LEDs/', views.LEDs, name='LEDs'),
]