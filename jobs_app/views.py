from django.shortcuts import render, HttpResponse

# Create your views here.
def jobs(request):
    return HttpResponse("Página de jobs")