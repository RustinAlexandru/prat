from django.http import HttpResponse
from django.shortcuts import render, redirect

def index(request):
    context = {
        "user": "",
        "tasks": ["1", "2", "3"]
    }

    return render(request, 'index.html', context)
