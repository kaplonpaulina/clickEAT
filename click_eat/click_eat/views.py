from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    """
        A hook to the home page

        **Context**

        **Template:**

        :template:`index.html`
    """


    template = 'index.html'
    return render(request,template)
