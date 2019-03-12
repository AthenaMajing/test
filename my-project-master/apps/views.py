import copy

# from django.db import models
# from django.forms import model_to_dict
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
from rest_framework.utils import json
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.views import ObtainJSONWebToken, jwt_response_payload_handler
# Create your views here.
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from datetime import datetime

from apps.models import User, Role, Permissions
from apps.serializers import CreateUserSerializer, CreatePermissionSerializer, UserShowSerializer, \
    AddPermissionSerializer, PermissionShowSerializer, AddRoleSerializer, RoleShowSerializer, UpdateUserInfoSerializer, \
    UpdatePermissionInfoSerializer


class LoginView(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # 校验成功，账户密码正确
            users = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, users, request)
            user = User.objects.get(username=request.data['username'])
            print(type(user))
            urll = []
            if not user.is_superuser:
                role_queryset = user.role.all()
                for role_obj in role_queryset:
                    p = dict(role_obj.__dict__)
                    role_obj =p['title']
                    role_obj =  Role.objects.get(title=role_obj)
                    permissions = role_obj.permission.all()
                    for permission in permissions:
                        permission = Permissions.objects.filter(feature=permission)
                        for permission_obj in permission:
                            urls = permission_obj.url
                            urll.append(urls)
                response_data['url'] = urll
                # print(user)
                response_data['user'] = users.username
                print(response_data)
                response =Response(response_data)
            else:
                response_data['url'] = 'all'
                response_data['user'] = users.username
                response = Response(response_data)

            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class UserView(CreateAPIView):
    """
    添加新用户
    传入参数：
        username, password
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = CreateUserSerializer
    def post(self, request, *args, **kwargs):

        print(request.data,'前端传递的参数')

        return self.create(self.request,*args, **kwargs)

class PermissionView(CreateAPIView):
    '''
    权限角色关系
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = CreatePermissionSerializer
    def post(self, request, *args, **kwargs):

        print(request.data,'前端传递的参数')

        return self.create(self.request,*args, **kwargs)


class UserInfoShow(ListAPIView,GenericAPIView):
    '''
    用户列表
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = User.objects.all()
    serializer_class = UserShowSerializer
    def get(self, request, select_name ,page):
        if select_name=='all':
            # print(type(request.user))
            user_info = self.get_queryset().order_by('id')
            paginator = Paginator(user_info, 20)
            posts = paginator.page(number=page)
            user_info_data = self.get_serializer(posts,many=True)
            # user_info_data.data['total'] = user_info.count()
            print(user_info_data.data)
            dict={}
            dict['data'] = user_info_data.data
            dict['total'] = user_info.count()
            return Response(dict)
        else:

            user_info = User.objects.get(username=select_name)
            print(user_info)
            user_info_json = self.get_serializer(instance=user_info)
            print(user_info_json.data)
            return Response(user_info_json.data)




class CreatPermissionView(CreateAPIView):
    '''
    添加新权限
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AddPermissionSerializer
    def post(self, request, *args, **kwargs):
        print(request.data,'前端传递的参数')

        return self.create(self.request)



class PermissionInfoShow(ListAPIView,GenericAPIView):
    '''
    权限列表
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = Permissions.objects.all()
    serializer_class = PermissionShowSerializer
    def get(self, request, select_name ,page):
        if select_name=='all':
            # print(type(request.user))
            permission_info = self.get_queryset().order_by('id')
            paginator = Paginator(permission_info, 20)
            posts = paginator.page(number=page)
            permission_info_data = self.get_serializer(posts,many=True)
            dict={}
            dict['data'] = permission_info_data.data
            dict['total'] = permission_info.count()
            print(dict)
            return Response(dict)
        else:

            permission_info = Permissions.objects.get(feature=select_name)
            print(permission_info)
            permission_info_json = self.get_serializer(instance=permission_info)

            return Response(permission_info_json.data)


class CreatRoleView(CreateAPIView):
    '''
    添加新角色
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AddRoleSerializer
    def post(self, request, *args, **kwargs):
        print(request.data,'前端传递的参数')

        return self.create(self.request)



class RoleInfoShow(ListAPIView,GenericAPIView):
    '''
    角色列表
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = Role.objects.all()
    serializer_class = RoleShowSerializer
    def get(self, request, select_name ,page):
        if select_name=='all':
            # print(type(request.user))
            permission_info = self.get_queryset().order_by('id')
            paginator = Paginator(permission_info, 20)
            posts = paginator.page(number=page)
            permission_info_data = self.get_serializer(posts,many=True)
            dict={}
            dict['data'] = permission_info_data.data
            dict['total'] = permission_info.count()
            print(dict)
            return Response(dict)
        else:

            permission_info = Permissions.objects.get(title=select_name)
            print(permission_info)
            permission_info_json = self.get_serializer(instance=permission_info)

            return Response(permission_info_json.data)



class UpdateInfoViewSet(ModelViewSet):
    '''
    修改用户信息
    '''
    queryset = User.objects.all()
    serializer_class = UpdateUserInfoSerializer
    def updates(self, request,pk, *args, **kwargs):
        print(self.update(self.request))

        return self.update(self.request)


    def retrieve(self, request, user_id,*args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateUserInfoSerializer(user)
        print(serializer.data)
        return Response(serializer.data)



class UpdatePermissionViewSet(ModelViewSet):
    '''
    修改权限信息
    '''
    queryset = Permissions.objects.all()
    serializer_class = UpdatePermissionInfoSerializer
    def updatespermission(self, request,pk, *args, **kwargs):
        print(self.update(self.request),'tfftyjuii')

        return self.update(self.request)


    def retrievepermission(self, request, permission_id,*args, **kwargs):
        try:
            permission = Permissions.objects.get(id=permission_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UpdatePermissionInfoSerializer(permission)
        # print(serializer.data)
        return Response(serializer.data)



