from django.shortcuts import render, redirect
from django.views import View
from core.models import CoreConfig
from isssys.models import IssSys

class HomeView(View):
    def get(self, request, *args, **kwargs):
        template_name = 'home.html'

        context = {
            'title' : 'IssTech IssAssist site',
            'header' : 'IssAssist Test Site',
            'exturl' : 'https://isstech.io',
        }

        return render(request, template_name, context)

class ResultView(View):
    def get(self, request, *args, **kwargs):
        template_name = 'result.html'
        core_information = CoreConfig.objects.all()
        print(core_information)
        context = {
            'title' : 'IssTech IssAssist site',
            'header' : 'IssAssist Result View',
            'exturl' : 'https://isstech.io',
        }

        return render(request, template_name, context)
