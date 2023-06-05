from django.shortcuts import render
from rest_framework.views import APIView
from .models import Post,Comment,Like,UserFollowing,Retweet
from .serializers import PostSerializers,CommentSerializers,LikeSerializers,RetweetSerializers,UserFollowingSerializers
from rest_framework.response import Response
from rest_framework import status,generics
from django.http import Http404
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from accounts.permission import IsObjectOwner
from django.shortcuts import get_object_or_404
# Create your views here.


class PostsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializers(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    permission_classes = [IsObjectOwner,IsAuthenticated,]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializers(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializers(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    search_fields = ('author_comment','post',)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.kwargs.get('post_id'):
            return self.queryset.filter(post_id=self.kwargs.get('post_id'))
        return self.queryset.all()


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = (IsObjectOwner,)

    def get_object(self):
        if self.kwargs.get('post_id'):
            return get_object_or_404(
                self.get_queryset(), post_id=self.kwargs.get('post_id'),
                pk=self.kwargs.get('pk')
            )
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))


class LikesView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers
    search_fields = ('user', 'post',)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.kwargs.get('post_id'):
            return self.queryset.filter(post_id=self.kwargs.get('post_id'))
        return self.queryset.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Customize the response data
        data = {
            'count': queryset.count(),
            'my_data': serializer.data
        }

        return Response(data)


class LikeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers
    permission_classes = (IsObjectOwner,IsAuthenticated,)

    def get_object(self):
        if self.kwargs.get('post_id'):
            return get_object_or_404(
                self.get_queryset(), post_id=self.kwargs.get('post_id'),
                pk=self.kwargs.get('pk')
            )
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))


class RetweetsView(generics.ListCreateAPIView):
    queryset = Retweet.objects.all()
    serializer_class = RetweetSerializers
    search_fields = ('user', 'post',)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.kwargs.get('post_id'):
            return self.queryset.filter(tweet_id=self.kwargs.get('post_id'))
        return self.queryset.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Customize the response data
        data = {
            'count': queryset.count(),
            'my_data': serializer.data
        }

        return Response(data)


class RetweetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Retweet.objects.all()
    serializer_class = RetweetSerializers
    permission_classes = (IsObjectOwner,IsAuthenticated,)

    def get_object(self):
        if self.kwargs.get('post_id'):
            return get_object_or_404(
                self.get_queryset(), tweet_id=self.kwargs.get('post_id'),
                pk=self.kwargs.get('pk')
            )
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))


class UserFollowingList(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, username):
        try:
            return UserFollowing.objects.filter(user_id__username=username)
        except UserFollowing.DoesNotExist:
            raise Http404

    def get(self, request,username, format=None):
        snippets = UserFollowing.objects.filter(user_id__username=username)
        serializer = UserFollowingSerializers(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserFollowingSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFollowingDetail(APIView):
    permission_classes = [IsObjectOwner,IsAuthenticated,]
    def get_object(self, pk):
        try:
            return UserFollowing.objects.get(pk=pk)
        except UserFollowing.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UserFollowingSerializers(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UserFollowingSerializers(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


