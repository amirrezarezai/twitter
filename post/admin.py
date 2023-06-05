from django.contrib import admin
from .models import Post,Comment,Like,Retweet,UserFollowing
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Retweet)
admin.site.register(UserFollowing)
