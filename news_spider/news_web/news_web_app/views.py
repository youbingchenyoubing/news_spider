#coding=utf-8
#from user_dao import UserDAO
import sys
import os
import json  
from django.http import HttpResponse 
from django.views.decorators.csrf import csrf_exempt

mongodb_path = os.path.join(os.path.dirname(__file__),os.pardir,os.pardir )
sys.path.append(mongodb_path)
from news_mongodb.user_dao import UserDAO
from news_mongodb.article_dao import ArticleDAO
from news_mongodb.models.user import User


from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect

 

def login_interceptor(func):
    def login_wrapper(request):
        user = request.session.get('user',default=None)
	if user:
	    return func(request)
	else:
	    return render(request, 'login.html')
    return login_wrapper

def admin_interceptor(func):
    def wrapper(request):
	user = request.session.get('user',default=None)
	if user and user['role'] == '0':
	    return func(request)
	else:
	    return render(request, 'index.html')
    return wrapper

def login(request):
    return render(request, 'login.html')

@csrf_exempt
def logining(request):
    username = request.POST['username']
    password = request.POST['password']
    user = User()
    user.username = username
    user.password = password
    userDAO = UserDAO()
    user = userDAO.login(user)
    user['id'] = user['_id']
    if user:
    	request.session['user'] = user
        return HttpResponseRedirect("/index")
    return render(request, 'login.html')

@login_interceptor
def index(request):
    if 'current_page' in request.GET:
        current_page = int(request.GET['current_page'])

    else:
        current_page = 0

    if 'webs' in request.GET:
        webs = request.GET['webs']
        webs = ["新浪网","人民网", "中华网"]
    else:
        webs = ["新浪网","人民网", "中华网"]

    print "webs>>>>", webs

    label = 'articles_test'
    articleDAO = ArticleDAO(label)
    condition = {"article_source":webs, "article_db":"0", "article_label_state":0, "startTime":'2017-01-11',
         "endTime":'2017-02-01', "current_page":current_page , "page_size":10 }

    articleList = articleDAO.article_search_list(condition)
    return render(request, 'index.html', {"articleList": articleList,
     "current_page":current_page, "webs":webs})

@login_interceptor
def search(request):
    print "search******"
    if 'current_page' in request.GET:
        current_page = int(request.GET['current_page'])
        if current_page < 0:
            current_page = 0
    else:
        current_page = 0


    label = 'articles_test'
    articleDAO = ArticleDAO(label)
    condition = {"article_source": webs, "article_db":"0", "article_label_state":0, "startTime":'2017-01-11',
         "endTime":'2017-01-15', "current_page":current_page , "page_size":10 }

    articleList = articleDAO.article_search_list(condition)
    return HttpResponse(json.dumps(articleList), content_type="application/json")  

@login_interceptor
@admin_interceptor
def approval(request):
    return render(request, 'approval.html')


@login_interceptor
@admin_interceptor
def userlist(request):
    userDAO = UserDAO()
    userList = userDAO.userlist()
    return render(request, 'userList.html', {'userList':userList})



@csrf_exempt
@login_interceptor
@admin_interceptor
def adduser(request):
    username = request.POST['username']
    password = request.POST['password']

    role = request.POST['role']
    
   
    user = User()
    user.username = username
    user.password = password
    user.role = role
    userDAO = UserDAO()

    flag = userDAO.addUser(user)
    if flag:
    	message = "添加成功"
    else:
    	message = "添加失败"
    userList = userDAO.userlist()
    return render(request, 'userList.html', {"message": message,
    	'userList':userList})

@login_interceptor
@admin_interceptor
def deluser(request):
    userId = request.GET['userId']
    userDAO = UserDAO()
    flag = userDAO.deluser(userId)
    if flag:
    	message = "删除成功"
    else:
    	message = "删除失败"

    userList = userDAO.userlist()
    return render(request, 'userList.html', {"message": message,
    	'userList':userList})

@login_interceptor
def logout(request):
    del request.session['user']
    return render(request, 'login.html')

@login_interceptor
def page(request):
    article_id = request.GET["articleId"]
    label = 'articles_test'
    articleDAO = ArticleDAO(label)
    article = articleDAO.show_article(article_id)
    return render(request, 'page.html', {'article': article})





