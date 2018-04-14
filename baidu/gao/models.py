from django.db import models
from db.base_model import BaseModel


from hashlib import sha1
def get_hash(str):
    '''取一个字符串的hash值'''
    sh = sha1()
    sh.update(str.encode('utf8'))
    return sh.hexdigest()
#
# from utils.get_hash import get_hash

class PassportManger(models.Manager):
    def add_one_passport(self, username, password, email):
        '''添加一个账户信息'''
        passport = self.create(username=username, password=get_hash(password), email=email)
        # 3.返回passport
        return passport

    def get_one_passport(self, username, password):
        '''根据用户名密码查找账户的信息'''
        try:
            passport = self.get(username=username, password=get_hash(password))
        except self.model.DoesNotExist:
            # 账户不存在
            passport = None
        return passport

    def check_passport(self,username):
        try:
            passport = self.get(username=username)
        except self.model.DoesNotExist:
            passport = None
        if passport:
            return True
        return False

class Passport(BaseModel):
    '''用户模型类'''
    username = models.CharField(max_length=20, verbose_name='用户名称')
    password = models.CharField(max_length=40, verbose_name='用户密码')
    email = models.EmailField(verbose_name='用户邮箱')
    is_active = models.BooleanField(default=False, verbose_name='激活状态')

    # 用户表的管理器
    objects = PassportManger()

    class Meta:
        db_table = 's_user_account'

class AddressManager(models.Manager):
    def get_default_address(self,passport_id):
        try:
            addr = self.get(passport_id = passport_id,is_default = True)
        except self.model.DoesNotExist:
            addr = None
        return addr

    def add_one_address(self,passport_id, recipient_name, recipient_addr, zip_code,recipient_phone):
        addr = self.get_default_address(passport_id=passport_id)

        if addr:
            is_default = False
        else:
            is_default = True

        addr = self.create(passport_id=passport_id,
                           recipient_name=recipient_name,
                           recipient_addr=recipient_addr,
                           zip_code=zip_code,
                           recipient_phone=recipient_phone,
                           is_default=is_default)

        return addr

class Address(BaseModel):
    recipient_name = models.CharField(max_length=20,verbose_name='收件人')
    recipient_addr = models.CharField(max_length=256,verbose_name='收件地址')
    zip_code = models.CharField(max_length=6,verbose_name='邮政棉麻')
    recipient_phone = models.CharField(max_length=11,verbose_name='联系电话')
    is_default = models.BooleanField(default=False,verbose_name='是否默认')
    passport = models.ForeignKey('Passport',verbose_name='账户')

    objects = AddressManager()

    class Meta:
        db_table = 's_user_address'