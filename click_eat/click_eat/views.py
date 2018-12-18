from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    template = 'index.html'
    return render(request,template)
