from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render

# Create your views here.

class Login(View):
    
    TEMPLATE = 'templates/login.html'

    def get(self, request):
        return render(request, template_name=self.TEMPLATE)