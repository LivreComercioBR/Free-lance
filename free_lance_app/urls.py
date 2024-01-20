from django.urls import path
from free_lance_app import views


urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logar/', views.logar, name='logar'),
    path('sair/', views.sair, name='sair')
]
