import re

from rest_framework import serializers

from apps.models import User, Role, Permissions





class CreateUserSerializer(serializers.ModelSerializer):
    """
    添加新用户序列化器
    """
    password2 = serializers.CharField(label='重复密码', write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password','password2','role','email')
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate_username(self, value):
        """用户名不能全部为数字"""
        if re.match(r'^\d+$', value):
            raise serializers.ValidationError('用户名不能全部为数字')

        return value

    def validate(self, attrs):
        """两次密码是否一致，短信验证码是否正确"""
        # 两次密码是否一致
        password = attrs['password']
        password2 = attrs['password2']

        if password != password2:
            raise serializers.ValidationError('两次密码不一致')
        return attrs

    def create(self, validated_data):
        """
        创建用户
        """

        del validated_data['password2']
        roles = validated_data.pop('role')
        # 创建并保存新用户
        user = User.objects.create_user(**validated_data)
        for role in roles:
            print(role)
            user.role.add(role)

        # 由服务器生成jwt token数据，保存用户的身份信息
        from rest_framework_jwt.settings import api_settings

        # 组织payload的数据
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 生成jwt token
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 生成payload数据
        payload = jwt_payload_handler(user)
        # 生成jwt token数据
        token = jwt_encode_handler(payload)
        # print(token)

        # 给user对象增加属性token，保存jwt token数据
        user.token = token

        # 返回user
        return user





class CreatePermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'




    def create(self, validated_data):
        """
        创建权限
        """

        # 创建并保存角色
        permissions = validated_data.pop('permission')
        print('11111111111111111')
        print(validated_data['title'])
        roles = Role.objects.filter(title=validated_data['title'])
        print(roles)
        for role in roles:
            for permission in permissions:

                role.permission.add(permission)



        # 返回角色
        return role


class UserShowSerializer(serializers.ModelSerializer):
    '''
    用户列表
    '''

    class Meta:
        model = User
        fields = ('id', 'username','is_deleted')


class AddPermissionSerializer(serializers.ModelSerializer):
    """
    添加新权限序列化器
    """

    class Meta:
        model = Permissions
        fields = '__all__'


class PermissionShowSerializer(serializers.ModelSerializer):
    '''
    权限列表
    '''

    class Meta:
        model = Permissions
        fields = ('id','url','feature')


class AddRoleSerializer(serializers.ModelSerializer):
    """
    添加新角色序列化器
    """

    class Meta:
        model = Role
        fields = ('id','title')


class RoleShowSerializer(serializers.ModelSerializer):
    '''
    角色列表
    '''

    class Meta:
        model = Role
        fields = '__all__'




class UpdateUserInfoSerializer(serializers.ModelSerializer):

    '''
    更新用户信息
    '''

    class Meta:
        model = User
        fields = ('id','username','email','is_deleted')


class UpdatePermissionInfoSerializer(serializers.ModelSerializer):
    '''
    更新权限信息
    '''

    class Meta:
        model = Permissions
        fields = ('id', 'url', 'feature')

