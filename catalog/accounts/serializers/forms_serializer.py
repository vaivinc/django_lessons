from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import Profile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class CaptchaFieldSerializer(serializers.Serializer):
    captcha_0 = serializers.CharField(required=True)
    captcha_1 = serializers.CharField(required=True)

    def validate(self, attrs):
        from captcha.models import CaptchaStore

        try:
            captcha = CaptchaStore.objects.get(hashkey=attrs["captcha_0"])

        except CaptchaStore.DoesNotExists:
            raise serializers.ValidationError("Incorrect captcha")

        if captcha.response != attrs.get("captcha_1", "").lower():
            raise serializers.ValidationError("Invalid captcha")

        captcha.delete()

        return attrs


class RegisterFormSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    captcha = CaptchaFieldSerializer(required=True)
