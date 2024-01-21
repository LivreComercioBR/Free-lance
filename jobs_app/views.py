from django.shortcuts import render, HttpResponse
from .models import Jobs
from datetime import datetime

# Create your views here.
def jobs(request):
    return HttpResponse("Página de jobs")


def encontrar_jobs(request):
    if request.method == "GET":
        jobs = Jobs.objects.filter(reservado=False)
        return render(request, 'encontrar_jobs.html', {'jobs': jobs})
    
    if request.method == "POST":

        preco_minimo = request.POST.get('preco_minimo')
        preco_maximo = request.POST.get('preco_maximo')
        prazo_minimo = request.POST.get('prazo_minimo')
        prazo_maximo = request.POST.get('prazo_maximo')
        categoria = request.POST.get('categoria')

        if preco_minimo or preco_maximo or prazo_minimo or prazo_maximo or categoria:

            if not preco_minimo:
                preco_minimo = 0
            if not preco_maximo:
                preco_maximo = 999999
            if not prazo_minimo:
                prazo_minimo = datetime(year=1900, month=1, day=1)
            if not prazo_maximo:
                prazo_maximo = datetime(year=3000, month=1, day=1)

            if categoria == "FE":
                categoria = ['FE', ]
            if categoria == "BE":
                categoria = ['BE', ]

            jobs = Jobs.objects.filter(
                preco__gte=preco_minimo).filter(preco__lte=preco_maximo).filter(prazo_entrega__gte=prazo_minimo).filter(prazo_entrega__lte=prazo_maximo).filter(categoria__in=categoria).filter(reservado=False)

        
        return render(request, 'encontrar_jobs.html', {'jobs': jobs})
    