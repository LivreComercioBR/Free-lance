from django.urls import path
from .import views

urlpatterns = [
    path('home/', views.jobs, name='home'),
    path('encontrar_jobs/', views.encontrar_jobs, name="encontrar_jobs"),
]
