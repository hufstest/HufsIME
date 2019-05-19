from django.urls import path
from . import views

urlpatterns = [
    # path('', views.HomePageView.as_view(), name='home'),
    path('', views.home, name='home'),
    path('recommend/<int:id>/', views.recommend, name='recommend'),
    path('tagged/<int:id>/', views.taggedview, name='tagged'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('new/', views.create_article, name = 'add_article'),
    path('show/<int:id>/', views.show, name = 'show_article'),
    path('update/<int:id>/', views.update_article, name = 'update_article'),
    path('delete/<int:id>/', views.delete_article, name = 'delete_article'),
    path('comment_delete/<int:id>/', views.delete_comment, name = 'delete_comment'),
    path('answer_delete/<int:id>/', views.delete_answer, name = 'delete_answer'),
    path('show/<int:id>/like/',views.like,name='like'),
    path('search/', views.search, name="search_article"),
]