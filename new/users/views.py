from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.db.models import Count
from datetime import timezone, datetime

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from .models import Article, Comment, Answer, Like, TaggedPost, Hit, PostTag
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
    try:
        # ip주소와 게시글 번호로 기록을 조회함
        hits = Hit.objects.get(ip=get_client_ip(request), article=the_article)
    except Exception as e:
        # 처음 게시글을 조회한 경우엔 조회 기록이 없음
        print(e)
        hits = Hit(ip=get_client_ip(request), article=the_article, date=str(datetime.now().date()))
        Article.objects.filter(id=id).update(hits=the_article.hits + 1)
        hits.save()
    else:
        # 조회 기록은 있으나, 날짜가 다른 경우
        if not hits.date == str(datetime.now().date()):
            Article.objects.filter(id=id).update(hits=the_article.hits + 1)
            hits.date = str(datetime.now().date())
            hits.save()
        # 날짜가 같은 경우
        else:
            print(str(get_client_ip(request)) + ' has already hit this post.\n\n')
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

def recommend(request, id):
    ordered = Article.objects.filter(user_id = id).values_list('tags').annotate(tags_count=Count('tags')).order_by('-tags_count')
    num = min(3,ordered.count())
    prefer_tag_id = []
    for i in range(num) :
        prefer_tag_id.append(ordered[i][0])
    prefer_article_id = TaggedPost.objects.filter(tag_id__in = prefer_tag_id).values('content_object_id').distinct()
    articles = Article.objects.filter(id__in = prefer_article_id)
    recommend = True
    return render(request, 'home.html', {'articles' : articles, 'recommend' : recommend})

def taggedview(request, id):
    tagged_articles_id = TaggedPost.objects.filter(tag_id = id).values('content_object_id')
    articles = Article.objects.filter(id__in = tagged_articles_id)
    tag_name = PostTag.objects.get(id = id).name
    return render(request, 'home.html', {'articles' : articles, 'tag_name' : tag_name})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
@require_POST
@csrf_exempt
def like(request,id):
    if request.method == 'POST':
        user = request.user  # 로그인한 유저를 가져온다.
        article_id = request.POST.get('pk', None)
        article = Article.objects.get(pk=article_id)  # 해당 메모 오브젝트를 가져온다.

        if article.like_user_set.filter(id=user.id).exists():  # 이미 해당 유저가 likes컬럼에 존재하면
            user.like_set.filter(article_id=article.id).delete()  # likes 컬럼에서 해당 유저를 지운다.
            message = 'You disliked this'
        else:
            user.like_set.create(article_id=article_id)
            message = 'You liked this'

    context = {'likes_count': article.like_count, 'message': message}
    return HttpResponse(json.dumps(context), content_type='application/json')
    # dic 형식을 json 형식으로 바꾸어 전달한다.