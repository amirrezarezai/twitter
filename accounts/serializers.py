from rest_framework import serializers
from .models import User
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True,required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error': 'p1 and p2 should be same!'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email Already exists!'})

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()

        return account


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password','new_password')


class ChangeUsernameSerializers(serializers.Serializer):
    new_username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('new_username',)


class ProfileSerializers(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    age = serializers.IntegerField(source='user.age')
    gender = serializers.CharField(source='user.gender')
    phone = serializers.CharField(source='user.phone')
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['avatar','bio','first_name','last_name','age','gender','phone']