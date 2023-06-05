from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostsList.as_view(), name='posts-list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('post/<int:post_id>/comments/', views.CommentListView.as_view(), name='comments'),
    path('post/<int:post_id>/comment/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('post/<int:post_id>/likes/', views.LikesView.as_view(), name='post_likes'),
    path('post/<int:post_id>/like/<int:pk>/', views.LikeView.as_view() , name='post_like'),
    path('post/<int:post_id>/retweets/', views.RetweetsView.as_view(), name='post_retweets'),
    path('post/<int:post_id>/retweet/<int:pk>/', views.RetweetView.as_view(), name='post_retweet'),
    path('userfollowing/user:<str:username>/', views.UserFollowingList.as_view(), name='userFollowing'),
    path('userfollowing/<int:pk>', views.UserFollowingDetail.as_view(), name='userFollowingDetail')
]