from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

from .forms import CreateUserForm
from .models import Blog
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy # generic vi

def home(request) :
    blogs = Blog.objects #쿼리셋 #메소드
    return render(request, 'home.html', {'blogs' : blogs})


class IndexView(TemplateView): # TemplateView를 상속 받는다.
    template_name = 'project/index.html'

class CreateUserView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CreateUserForm
    # form_class = UserCreationForm  #내장 회원가입 폼 사용하는 경우
    success_url = reverse_lazy('create_user_done')

class RegisteredView(TemplateView):
    template_name = 'registration/signup_done.html'