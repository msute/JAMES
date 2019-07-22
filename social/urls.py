from django.urls import path
from social import apis


urlpatterns = [
    path('recommend', apis.recommend),
    path('like_someone', apis.like_someone),
    path('superlike', apis.superlike),
    path('dislike', apis.dislike),
    path('rewind', apis.rewind),
    path('liked-me', apis.liked_me),
]