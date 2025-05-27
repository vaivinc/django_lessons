from ..models import Profile
from accounts.serializers.user_serializer import serializers, UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"

