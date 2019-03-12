from django.contrib.auth.models import AbstractUser
# from django.db import models

# Create your models here.


from django.db import models


# class User(models.Model):
#     """用户表
#     普通字段:
#         id, username, password
#     关联字段:
#         roles(多对多)
#     """
#
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=16, verbose_name='用户名')
#     password = models.CharField(max_length=32, verbose_name='登录密码')
#
#     roles = models.ManyToManyField(to='Role', verbose_name='用户拥有的角色')
#
#     def __str__(self):
#         return self.username
#
#     class Meta:
#         verbose_name_plural = '用户表'
from django.utils import timezone


class Role(models.Model):
    """角色表
    普通字段:
        id, title
    关联字段:
        permissions(多对多)
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='角色名')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')
    permission = models.ManyToManyField(to='Permissions', verbose_name='角色拥有的权限')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '角色表'



class Permissions(models.Model):
    """权限表
    普通字段:
        id, url, feature

    """

    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=64, verbose_name='权限url路径')
    feature = models.CharField(max_length=16, verbose_name='权限名')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')
    # create = models.CharField(max_length=64,verbose_name='权限创建时间',default=timezone.now)
    # modify = models.CharField(max_length=64,verbose_name='权限修改时间 ',default=timezone.now)

    def __str__(self):
        return self.feature

    class Meta:
        verbose_name_plural = '权限表'





class User(AbstractUser):
    """用户模型类"""

    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    role = models.ManyToManyField(to='Role')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

