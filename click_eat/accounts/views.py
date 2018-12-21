from django.contrib.auth import login, logout
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms

class SignUp(CreateView):
    """
        A handle of the sign up

        **Context**

        **Template:**

        :template:`accounts/signup.html`
    """

    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

class Profile(TemplateView):
    """
        A hook to the profile page

        **Template:**

        :template:`profile.html`
    """

    template_name = 'profile.html'
