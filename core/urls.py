from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('galeria/', views.galeria, name='galeria'),
    path('sobre/', views.sobre, name='sobre'),
    path('estudio/', views.estúdio, name='estudio'),
    path('artistas/', views.artistas, name='artistas'),
    path('artista/<slug:slug>/', views.artista_detalhe, name='artista_detalhe'),
    path('contato/', views.contato, name='contato'),
    path('loja/', views.loja_home, name='loja'),
]

