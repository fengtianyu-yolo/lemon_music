from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect
import json

# Create your views here.

class Login(View):
    
    TEMPLATE = 'login.html'

    def get(self, request):
        return render(request, template_name=self.TEMPLATE)
    
    def post(self, request):
        username = request.POST.get('username')
        print(username)

        return redirect('dashboard')
    
class LoginAPI(View):

    def get(self, request):
        result = {
            'code': 0,
            'data': {
                'user_id': '123',
                'username': '小困子',
                'avatar': '',
                'token': '12312312312'
            }            
        }
        return HttpResponse(json.dumps(result))
    
class RefreshList(View):

    def get(self, request):
        result = {
            'code': 0,
            'data': {
                'list': []
            }
        }        
        return HttpResponse(json.dumps(result)) 
    
    def refresh(self): 
        # 拿到目录下的所有文件 
        path = '/Volumes/Elements SE/音乐库'
        pass