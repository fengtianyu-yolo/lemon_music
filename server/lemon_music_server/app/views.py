from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render, redirect

# Create your views here.

class Login(View):
    
    TEMPLATE = 'login.html'

    def get(self, request):
        return render(request, template_name=self.TEMPLATE)
    
    def post(self, request):
        username = request.POST.get('username')
        print(username)

        return redirect('dashboard')