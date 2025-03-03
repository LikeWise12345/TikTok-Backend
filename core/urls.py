from django.urls import path
from .views import VideoListView, UploadVideoView, add_comment, rate_video, UserSignupView, UserLoginView, csrf_token_view

urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('videos/upload/', UploadVideoView.as_view(), name='video-upload'),
    path('videos/<int:video_id>/comment/', add_comment, name='add-comment'),
    path('videos/<int:video_id>/rate/', rate_video, name='rate-video'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path("csrf/", csrf_token_view, name="csrf_token"),  # CSRF token endpoint
]
