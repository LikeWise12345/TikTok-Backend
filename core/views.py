from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Video, Comment, Rating
from .serializers import VideoSerializer, CommentSerializer, RatingSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSignupSerializer, UserLoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all().order_by('-uploaded_at')
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        print(serializer.data)
        return Response(serializer.data)

class UploadVideoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_creator:
            return Response({'error': 'Permission denied'}, status=403)
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, video_id):
    video = Video.objects.get(id=video_id)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, video=video)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_video(request, video_id):
    video = Video.objects.get(id=video_id)
    serializer = RatingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, video=video)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

class UserSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "Signup successful!"}, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"success": False, "errors": serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Get the username and password from the request
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user:
            # Create JWT token if the user is authenticated
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Return the token
            return Response({
                'access_token': access_token
            }, status=status.HTTP_200_OK)
        else:
            # Return error if credentials are wrong
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_400_BAD_REQUEST)

