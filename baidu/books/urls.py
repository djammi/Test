from django.conf.urls import url
from books import views


urlpatterns=[
	url(r'^$',views.index,name='index'), #首頁
	url(r'books/(?P<books_id>\d+)/$',views.detail,name='detail'),#詳情頁



]