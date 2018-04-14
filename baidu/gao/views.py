from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django_redis import get_redis_connection

from baidu import settings
from books.models import Books
from gao.models import Passport,Address
import re
from django.http import HttpResponse,JsonResponse
from utils.decorators import login_required
from order.models import OrderInfo,OrderGoods

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from gao.tasks import send_active_email

# Create your views here.
def register(request):
	return render(request,'users/register.html')
	# return redirect(reverse('books:index'))

def register_handle(request):
	'''进行用户注册处理'''
	# 接收数据
	username = request.POST.get('user_name')
	password = request.POST.get('pwd')
	email = request.POST.get('email')

	# 进行数据校验
	if not all([username, password, email]):
		# 有数据为空
		return render(request, 'users/register.html', {'errmsg':'参数不能为空!'})

# 判断邮箱是否合法
	if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
		# 邮箱不合法
		return render(request, 'users/register.html', {'errmsg':'邮箱不合法!'})

	# 进行业务处理:注册，向账户系统中添加账户
	# Passport.objects.create(username=username, password=password, email=email)
	passport = Passport.objects.add_one_passport(username=username, password=password, email=email)

	# 注册完，还是返回注册页。
	return redirect(reverse('books:index'))
	# print("注冊成功")

def login(request):
	'''顯示登錄頁面'''
	username = ''
	checked = ''

	context = {
		'username':username,
		'checked':checked,
	}
	return render(request,'users/login.html',context)




def login_check(request):
	'''进行用户登录校验'''
	# 1.获取数据
	username = request.POST.get('username')
	password = request.POST.get('password')
	remember = request.POST.get('remember')
	verifycode = request.POST.get('verifycode')
	# 2.数据校验
	if not all([username, password, remember,verifycode]):
		# 有数据为空
		return JsonResponse({'res': 2})

	if verifycode.upper() != request.session['verifycode']:
		return JsonResponse({'res':2})
	# 3.进行处理:根据用户名和密码查找账户信息
	passport = Passport.objects.get_one_passport(username=username, password=password)

	if passport:
		# 用户名密码正确
		# 获取session中的url_path
		# if request.session.has_key('url_path'):
		#     next_url = request.session.get('url_path')
		# else:
		#     next_url = reverse('books:index')
		next_url = request.session.get('url_path', reverse('books:index')) # /user/
		jres = JsonResponse({'res': 1, 'next_url': next_url})

		# 判断是否需要记住用户名
		if remember == 'true':
			# 记住用户名
			jres.set_cookie('username', username, max_age=7*24*3600)
		else:
			# 不要记住用户名
			jres.delete_cookie('username')

		# 记住用户的登录状态
		request.session['islogin'] = True
		request.session['username'] = username
		request.session['passport_id'] = passport.id
		return jres
	else:
		# 用户名或密码错误
		return JsonResponse({'res': 0})

def logout(request):
	request.session.flush()
	return redirect(reverse('books:index'))

@login_required
def user(request):
	passport_id = request.session.get('passport_id')
	addr = Address.objects.get_default_address(passport_id=passport_id)

	con = get_redis_connection('default')
	key = 'history_%d'%passport_id
	history_li = con.lrange(key,0,4)

	books_li = []

	for id in history_li:
		books = Books.objects.get_books_by_id(books_id=id)
		books_li.append(books)
	context = {
		'addr':addr,
		'page':'user',
		'books_li':books_li
	}

	return render(request,'users/user_center_info.html',context)

@login_required
def address(request):
	passport_id = request.session.get('passport_id')

	if request.method == 'GET':
		addr = Address.objects.get_default_address(passport_id=passport_id)

		return render(request,'users/user_center_site.html',{'addr':addr,'page':'address'})
	else:
		recipient_name = request.POST.get('username')
		recipient_addr = request.POST.get('addr')
		zip_code = request.POST.get('zip_code')

		recipient_phone = request.POST.get('phone')

		if not all([recipient_name,recipient_addr,zip_code,recipient_phone]):
			return render(request,'users/user_center_site.html',{'errmsg':'参数不能为空'})

		Address.objects.add_one_address(passport_id=passport_id,
										recipient_name=recipient_name,
										recipient_addr=recipient_addr,
										zip_code=zip_code,
										recipient_phone=recipient_phone)

		return redirect(reverse('user:address'))


@login_required
def order(request):
	passport_id = request.session.get('passport_id')

	order_li = OrderInfo.objects.filter(passport_id=passport_id)

	for order in order_li:
		order_id = order.order_id
		order_books_li = OrderGoods.objects.filter(order_id=order_id)

		for order_books in order_books_li:
			count = order_books.count
			price = order_books.price

			amount = count * price

			order_books.amount = amount

		order.order_books_li = order_books_li

		context = {
			'order_li':order_li,
			'page':'order'
		}

	return  render(request,'users/user_center_order.html',context)



def register_handle(request):
	username = request.POST.get('user_name')
	password = request.POST.get('pwd')
	email = request.POST.get('email')

	if not all([username,password,email]):
		return  render(request,'users/register.html',{'errmsg':'参数不能为空'})

	if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
			# 邮箱不合法
		return render(request, 'users/register.html', {'errmsg':'邮箱不合法!'})

	p = Passport.objects.check_passport(username=username)

	if p:
		return render(request,'users/register.html',{'errmsg':'用户名已存在'})

	passport = Passport.objects.add_one_passport(username=username,password=password,email=email)

	serializer = Serializer(settings.SECRET_KEY, 3600)

	token = serializer.dumps({'confirm':passport.id})

	token = token.decode()

	#send_mail('尚硅谷书城用户激活', '', settings.EMAIL_FROM, [email],html_message='<a href="http://127.0.0.1:8000/user/active/%s/">http://127.0.0.1:8000/user/active/</a>' % token)

	send_active_email.delay(token,username,email)
	return redirect(reverse('books:index'))

def verifycode(request):
	from PIL import Image,ImageDraw,ImageFont

	import random

	bgcolor = (random.randrange(20,100),random.randrange(20,100),255)

	width = 100
	height = 25

	im = Image.new('RGB',(width,height),bgcolor)

	draw = ImageDraw.Draw(im)

	for i in range(0,100):
		xy = (random.randrange(0,width),random.randrange(0,height))
		fill = (random.randrange(0,255),255,random.randrange(0,255))
		draw.point(xy,fill=fill)
	str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
	rand_str=''
	for i in range(0,4):
		rand_str += str1[random.randrange(0,len(str1))]
	font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-RI.ttf",15)

	fontcolor = (255,random.randrange(0,255),random.randrange(0,255))

	draw.text((5,2),rand_str[0],font=font,fill=fontcolor)
	draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
	draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
	draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)

	del draw

	request.session['verifycode'] = rand_str

	import io
	buf = io.BytesIO()

	im.save(buf,'png')

	print(buf.getvalue())
	return HttpResponse(buf.getvalue(),'image/png')


def register_active(request,token):
	serializer = Serializer(settings.SECRET_KEY,3600)
	try:
		info = serializer.loads(token)
		passport_id = info['confirm']
		passport = Passport.objects.get(id=passport_id)
		passport.is_active = True
		passport.save()
		return redirect(reverse('user:login'))
	except SignatureExpired:
		return HttpResponse('激活链接已过期')