from rest_framework import serializers
from .models import User, Video, Comment, Rating
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_creator']

class VideoSerializer(serializers.ModelSerializer):
    video_file = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'creator', 'title', 'description', 'hashtags', 'video_file', 'uploaded_at']

    def get_video_file(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.video_file.url)
        return obj.video_file.url

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'video', 'user', 'text', 'created_at']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'video', 'user', 'rating', 'created_at']
        
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_creator']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_creator=validated_data.get('is_creator', False),
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")
