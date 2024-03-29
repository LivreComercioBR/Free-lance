from django.shortcuts import redirect, render, HttpResponse
from free_lance_app.models import User
from .models import Jobs
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required


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


@login_required(login_url=('/autenticacao/logar'))
def aceitar_job(request, id):
    # if request.user.is_not
    job = Jobs.objects.get(id=id)
    job.profissional = request.user
    job.reservado = True
    job.save()
    return redirect('/jobs/encontrar_jobs')


@login_required(login_url=('/autenticacao/logar'))
def perfil(request):
    if request.method == "GET":
        jobs = Jobs.objects.filter(profissional=request.user)
        return render(request, 'perfil.html', {'jobs': jobs})
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')

        usuario = User.objects.filter(username=username).exclude(id=request.user.id)

        if usuario.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse Username')
            return redirect('/jobs/perfil')
        
        usuario = User.objects.filter(email=email).exclude(id=request.user.id)

        if usuario.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse E-mail')
            return redirect('/jobs/perfil')
        
        request.user.username = username
        request.user.email = email
        request.user.first_name = primeiro_nome
        request.user.last_name = ultimo_nome
        request.user.save()
        messages.add_message(request, constants.SUCCESS, 'Dados alterado com sucesso')
        return redirect('/jobs/perfil')
    

@login_required(login_url='/autenticacao/logar')
def enviar_projeto(request):
    arquivo = request.FILES.get('file')
    id_job = request.POST.get('id')
    job = Jobs.objects.get(id=id_job)
    job.arquivo_final = arquivo
    job.status = 'AA'
    job.save()
    return redirect('/jobs/perfil')    
