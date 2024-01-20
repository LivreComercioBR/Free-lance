from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth
import re
from .models import User


def cadastro(request):
    
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if len(username.split()) == 0 or len(email.split()) == 0 or len(password.split()) == 0:
            messages.add_message(request, constants.ERROR, 'Por favor preencha todos os campos!')
            return redirect('/autenticacao/cadastro')
        
        usuario = User.objects.filter(username=username)

        if usuario.exists():
            messages.add_message(request, constants.ERROR, 'Ops! Já existe um usuário com este nome!')
            return redirect('/autenticacao/cadastro')
        
        email_user = User.objects.filter(email=email)

        if email_user.exists():
            messages.add_message(request, constants.ERROR, 'Ops! Já existe um usuário com este email!')
            return redirect('/autenticacao/cadastro')
        
        if len(password.strip()) < 8:
            messages.add_message(request, constants.ERROR, 'Sua senha deverá ter no mínimo 8 caracteres e deve conter pelo menos: 1 letra maiúscula, 1 letra minúscula e números!')
            return redirect('/autenticacao/cadastro')
        
        if not re.search('[A-Z]', password):
            messages.add_message(request, constants.ERROR, 'Sua senha deverá conter no mínimo uma letra maiúscula!')
            return redirect('/autenticacao/cadastro')
        
        if not re.search('[a-z]', password):
            messages.add_message(request, constants.ERROR, 'Sua senha deverá conter no mínimo uma letra minúscula!')
            return redirect('/autenticacao/cadastro')
        
        if not re.search('[1-9]', password):
            messages.add_message(request, constants.ERROR, 'Sua senha deverá conter no mínimo um número!')
            return redirect('/autenticacao/cadastro')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
            return redirect('/autenticacao/logar')
        
        except Exception as Error:
            messages.add_message(request, constants.ERROR, f'O erro encontrado foi: {Error.__class__}')
            return redirect('/authenticacao/cadastro')
        
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/authenticacao/cadastro')


def logar(request):
    if request.method == "GET":
        return render(request, 'logar.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if not user:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
            return redirect('/autenticacao/logar')
        else:
            auth.login(request, user)
            return redirect('/')

def sair(request):
    auth.logout(request)
    messages.add_message(request, constants.INFO, 'Você saiu do sistema!')
    return redirect('/autenticacao/logar')