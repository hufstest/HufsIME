from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect

from users.models import Article, Comment, Answer, Like
from .forms import CustomUserCreationForm, ArticleForm, CommentForm, AnswerForm
from django.views.generic import TemplateView

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

# class HomePageView(TemplateView):
#     template_name = 'home.html'

def home(request):
    articles = Article.objects.all()
    return render(request, 'home.html', {'articles' : articles})

def show(request, id):
    the_article = Article.objects.get(id = id)
    comments = Comment.objects.filter(article__id = id)
    answers = Answer.objects.filter(article__id = id)
    commentform = CommentForm(request.POST or None)
    answerform = AnswerForm(request.POST or None)
    if commentform.is_valid():
        commentform.save()
        return redirect('/users/show/%d'%(id))
    if answerform.is_valid():
        answerform.save()
        return redirect('/users/show/%d'%(id))
    return render(request, 'single_article.html', {'article' : the_article, 'comments' : comments,
                                                     'commentform' : commentform, 'answers' : answers,
                                                     'answerform' : answerform,})

def create_article(request):
    form = ArticleForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        return redirect('home')
    
    return render(request, 'article_form.html', {'form' : form}) 


def update_article(request, id):
    the_article = Article.objects.get(id = id)
    form = ArticleForm(request.POST or None, instance = the_article)
    
    if form.is_valid():
        form.save()
        return redirect('/users/show/%d'%(id))
    
    return render(request, 'article_form.html', {'form' : form, 'article' : the_article}) 

def delete_article(request, id):
    the_article = Article.objects.get(id = id)
    
    if request.method == 'POST':
        the_article.delete()
        return redirect('home')
    
    return render(request, 'delete_confirm.html', {'article' : the_article})

def delete_comment(request, id):
    the_comment = Comment.objects.get(id = id)
    article_id = the_comment.article.id
    if request.method == 'POST':
        the_comment.delete()
        return redirect('/users/show/%d'%(article_id))
    
    return render(request, 'delete_confirm.html', {'comment' : the_comment})

def delete_answer(request, id):
    the_answer = Answer.objects.get(id = id)
    article_id = the_answer.article.id
    if request.method == 'POST':
        the_answer.delete()
        return redirect('/users/show/%d'%(article_id))
    
    return render(request, 'delete_confirm.html', {'answer' : the_answer})

