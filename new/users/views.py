from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.db.models import Count
import operator
from datetime import timezone, datetime
from collections import Counter
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from .models import Article, Comment, Answer, Like, TaggedPost, Hit, PostTag, CustomUser
from .forms import CustomUserCreationForm, ArticleForm, CommentForm, AnswerForm
from django.views.generic import TemplateView
from urllib.request import urlopen
from bs4 import BeautifulSoup

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

# class HomePageView(TemplateView):
#     template_name = 'home.html'

def home(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 10)
    page = request.POST.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    html = urlopen("http://builder.hufs.ac.kr/user/indexSub.action?framePath=unknownboard&siteId=ime&dum=dum&boardId=69047159&page=1&command=list")
    bsObject = BeautifulSoup(html, "html.parser")
    bsObject = bsObject.find("form", {"name": "frm"})
    num = 0
    notices = []
    for link in bsObject.find_all('a'):
        if num > 2 :
            break
        base = "http://builder.hufs.ac.kr/user/"
        # print(link.text.strip(), base+link.get('href'))
        notices.append([link.text.strip(), base+link.get('href')])
        num += 1
    return render(request, 'home.html', {'articles' : articles, 'notices' : notices, 'paginator':paginator, 'today': datetime.now().strftime("%x")})

@csrf_exempt
def scroll(request):  # Ajax 로 호출하는 함수
    articles = Article.objects.all()
    paginator = Paginator(articles, 10)
    page = request.POST.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles= paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    html = urlopen(
        "http://builder.hufs.ac.kr/user/indexSub.action?framePath=unknownboard&siteId=ime&dum=dum&boardId=69047159&page=1&command=list")
    bsObject = BeautifulSoup(html, "html.parser")
    bsObject = bsObject.find("form", {"name": "frm"})
    num = 0
    notices = []
    for link in bsObject.find_all('a'):
        if num > 2:
            break
        base = "http://builder.hufs.ac.kr/user/"
        # print(link.text.strip(), base+link.get('href'))
        notices.append([link.text.strip(), base + link.get('href')])
        num += 1
        # total_page=[]
        # total_page.append(articles)



    return render(request, 'scroll.html', {'articles': articles, 'notices': notices, 'paginator':paginator ,'today' : datetime.now().strftime("%x") })



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
    article_related_tag_ordered = Article.objects.filter(user_id = id).values_list('tags').annotate(tags_count=Count('tags')).order_by('-tags_count')
    article_related_tag_ordered_weight = dict((i[0],i[1]*5) for i in article_related_tag_ordered)
    comment_related_tag_ordered = recommend_by_comment(id)
    answer_related_tag_ordered = recommend_by_answer(id)
    merged_tag = merge_dict(article_related_tag_ordered_weight, comment_related_tag_ordered)
    merged_tag = merge_dict(merged_tag,answer_related_tag_ordered)
    merged_tag_sorted = sorted(merged_tag.items(), key=operator.itemgetter(1),reverse=True)
    num = min(3,len(merged_tag_sorted))
    prefer_tag_id = []
    for i in range(num) :
        prefer_tag_id.append(merged_tag_sorted[i][0])
    prefer_article_id = TaggedPost.objects.filter(tag_id__in = prefer_tag_id).values('content_object_id').distinct()
    articles = Article.objects.filter(id__in = prefer_article_id)
    recommend = True
    return render(request, 'home.html', {'articles' : articles, 'recommend' : recommend})

def recommend_by_comment(id):
    comment_related_tag = []
    u = CustomUser.objects.get(id = id)
    comments = u.comment_set.values("id")
    for comment in comments :
        article_id = Comment.objects.get(id = comment['id']).article_id
        a = Article.objects.get(id = article_id).tags.values('id')
        for i in a :
            comment_related_tag.append(i['id'])
    result = dict((i, comment_related_tag.count(i)) for i in comment_related_tag)
    return result

def recommend_by_answer(id):
    answer_related_tag = []
    u = CustomUser.objects.get(id = id)
    answers = u.answer_set.values("id")
    for answer in answers :
        article_id = Answer.objects.get(id = answer['id']).article_id
        a = Article.objects.get(id = article_id).tags.values('id')
        for i in a :
            answer_related_tag.append(i['id'])
    result = dict((i, answer_related_tag.count(i)) for i in answer_related_tag)
    return result

def merge_dict(x,y):
    return { k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y) }

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
        user = request.user
        article_id = request.POST.get('pk', None)
        article = Article.objects.get(pk=article_id)

        if article.like_user_set.filter(id=user.id).exists():
            user.like_set.filter(article_id=article.id).delete()
            message = 'You disliked this'
        else:
            user.like_set.create(article_id=article_id)
            message = 'You liked this'

    context = {'likes_count': article.like_count, 'message': message}
    return HttpResponse(json.dumps(context), content_type='application/json')
    # dic 형식을 json 형식으로 바꾸어 전달한다.


def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        message = 'You searched for: %r' % request.GET['q']
        articles = (Article.objects.filter(title__icontains=q )) | (Article.objects.filter( content__icontains=q))
    else:
        message = 'You submitted an empty form.'
    return render(request, 'home.html', {'message': message, 'articles': articles})

def mypage(request):
    id = request.user.id
    article_related_tag_ordered = Article.objects.filter(user_id = id).values_list('tags').annotate(tags_count=Count('tags')).order_by('-tags_count')
    article_related_tag_ordered = dict(article_related_tag_ordered)
    comment_related_tag_ordered = recommend_by_comment(id)
    answer_related_tag_ordered = recommend_by_answer(id)
    merged_tag = merge_dict(article_related_tag_ordered, comment_related_tag_ordered)
    merged_tag = merge_dict(merged_tag, answer_related_tag_ordered)
    if None in merged_tag:
        del merged_tag[None]
    tags_info = []
    for i in merged_tag :
        p = str(PostTag.objects.get(id = i))
        tags_info.append([p,merged_tag[i]])
    return render(request, 'mypage.html', {'tag_info':merged_tag, 'tags' : tags_info})