from django.conf.urls import include, url
from django.contrib import admin
from news_web_app import views as news_web_view

 
urlpatterns = [
    url(r'^$', news_web_view.login, name='login'),
    url(r'^index/$', news_web_view.index, name='index'),
    url(r'^logining', news_web_view.logining, name='logining'),
    url(r'^approval/$', news_web_view.approval, name='approval'),
    url(r'^userlist/$', news_web_view.userlist, name='userlist'),
    url(r'^adduser', news_web_view.adduser, name='adduser'),
    url(r'^deluser/$', news_web_view.deluser, name='deluser'),
    url(r'^logout/$', news_web_view.logout, name='logout'),
    url(r'^page/$', news_web_view.page, name='page'),
    url(r'^admin/', include(admin.site.urls)),
]