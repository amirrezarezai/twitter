from django.db import models
from accounts.models import User

# Create your models here.


class Post(models.Model):
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Post',null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='post')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} : {self.text}'


class Comment(models.Model):
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='comment',null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comment')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} -> {self.post.text}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')

    class Meta:
        unique_together = ('user','post')

    def __str__(self):
        return f'{self.user} liked this post -> {self.post.text}'


class Retweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='retweet')
    tweet = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='retweet')

    def __str__(self):
        return f'retweet {self.user} -> {self.tweet.text}'


class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, related_name="following" , on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user_id','following_user_id',]

    def __str__(self):
        return f'{self.user_id.username} following : {self.user_id.following.count()} followers:{self.user_id.followers.count()}'


