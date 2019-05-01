from django.urls import path
from . import views

app_name= "project"

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    # /project 으로 접속시 (include 됨)
   ]