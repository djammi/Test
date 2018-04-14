from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

@shared_task
def send_active_email(token,username,email):
	subject = '尚硅谷异步通知激活'
	message = '欢迎您的注册'
	sender = settings.EMAIL_FROM
	receiver = [email]
	html_message = '<a href="http://47.98.204.57:80">500W立即前往</a>'
	send_mail(subject,message,sender,receiver,html_message=html_message)


