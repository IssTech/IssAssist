from django.shortcuts import render, redirect
from django.views import View

class HomeView(View):
    def get(self, request, *args, **kwargs):
        template_name = 'home.html'

        context = {
            'title' : 'IssTech IssBot site',
            'header' : 'IssBot Test Site',
            'exturl' : 'https://isstech.io',
        }

        return render(request, template_name, context)