from rest_framework import serializers
from .models import Post,Comment,Like,UserFollowing,Retweet


class CommentSerializers(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('user','post',)


class RetweetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Retweet
        fields = '__all__'


class PostSerializers(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    like = LikeSerializers(many=True,read_only=True)
    retweet = RetweetSerializers(many=True,read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class UserFollowingSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = '__all__'