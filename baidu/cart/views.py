from django.shortcuts import render
from django.http import JsonResponse
from books.models import Books
from utils.decorators import login_required
from django_redis import get_redis_connection
# Create your views here.

def cart_add(request):
	if not request.session.has_key('islogin'):
		return JsonResponse({'res':0,'errmsg':'请先登录'})

	books_id = request.POST.get('books_id')
	books_count = request.POST.get('books_count')

	if not all([books_id,books_count]):
		return JsonResponse({'res':1,'errmsg':'数据不完整'})

	books = Books.objects.get_books_by_id(books_id=books_id)

	if books is None:
		return JsonResponse({'res':2,'errmsg':'商品不存在'})

	try:
		count = int(books_count)
	except Exception as e:
		return JsonResponse({'res':3,'errmsg':'商品数量必须为数字'})

	conn = get_redis_connection('default')
	cart_key = 'cart_%d' % request.session.get('passport_id')

	res = conn.hget(cart_key,books_id)
	if res is None:
		res = count
	else:
		res = int(res) + count

	if res > books.stock:
		return JsonResponse({'res':4,'errmsg':'商品库存不足'})
	else:
		conn.hset(cart_key,books_id,res)

	return JsonResponse({'res':5})

def cart_count(request):
	'''获取用户购物车中商品的数目'''
	#判断用户是否登录
	if not request.session.has_key('islogin'):
		return JsonResponse({'res':0})

	#计算用户购物车商品的数量
	conn = get_redis_connection('default')
	cart_key = 'cart_%d' % request.session.get('passport_id')
	#res = conn.hlen(cart_key) 显示商品的条目数

	res = 0
	res_list = conn.hvals(cart_key)

	for i in res_list:
		res += int(i)
	return JsonResponse({'res':res})

@login_required
def cart_show(request):
	'''显示用户购物车页面'''
	passport_id = request.session.get('passport_id')
	conn = get_redis_connection('default')
	cart_key = 'cart_%d' % passport_id
	res_dict = conn.hgetall(cart_key)

	books_li = []

	total_count = 0

	total_price = 0

	for id,count in res_dict.items():
		books = Books.objects.get_books_by_id(books_id=id)
		print(books)
		books.count = count
		books.amount = int(count) * books.price

		books_li.append(books)

		total_count += int(count)
		total_price += int(count)* books.price

	context = {
		'books_li':books_li,
		'total_count':total_count,
		'total_price':total_price,
	}

	return render(request,'cart/cart.html',context)

def cart_del(request):
	if not request.session.has_key('islogin'):
		return  JsonResponse({'res':0,'errmsg':'请先登录'})

	books_id = request.POST.get('books_id')

	if not all([books_id]):
		return JsonResponse({'res':1,'errmsg':'数据不完整'})

	books = Books.objects.get_books_by_id(books_id=books_id)

	if books is None:
		return JsonResponse({'res':2,'errmsg':'商品不存在'})

	conn = get_redis_connection('default')
	cart_key = 'cart_%d' % request.session.get('passport_id')
	conn.hdel(cart_key,books_id)

	return JsonResponse({'res':3})

def cart_update(request):
	if not request.session.has_key('islogin'):
		return JsonResponse({'res':0,'errmsg':'请先登录'})

	books_id = request.POST.get('books_id')
	books_count = request.POST.get('books_count')

	if not all([books_id,books_count]):
		return JsonResponse({'res':1,'errmsg':'数据不完整'})

	books = Books.objects.get_books_by_id(books_id=books_id)

	if books is None:
		return JsonResponse({'res':2,'errmsg':'商品不存在'})

	try:
		books_count = int(books_count)
	except Exception as e:
		return JsonResponse({'res':3,'errmsg':'商品数目必须为数字'})

	conn = get_redis_connection('default')
	cart_key = 'cart_%d' % request.session.get('passport_id')

	if books_count > books.stock:
		return JsonResponse({'res':4,'errmsg':'商品库存不足'})

	conn.hset(cart_key,books_id,books_count)

	return JsonResponse({'res':5})















