from django.db import models
from django.conf import settings
from datetime import *
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse
from django.views.generic  import *
from django.contrib.contenttypes.fields import GenericRelation
from UserProfile.models import Profile
import random
User = settings.AUTH_USER_MODEL

#  NOTE :
"""

from django.contrib.auth import get_user_model        # This is used to access the  user and data associated with it
User = get_user_model()
j = User.objects.first()

print(j.blogpost_set.all())       # this is used to list out all the blogposts associated with j user


"""

# https://docs.djangoproject.com/en/3.1/topics/db/queries/

class BlogPostQuerySet(models.QuerySet):        # customized  inbuilt    get_queryset()  function
    
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now)

    def search(self,query):

        lookup = (
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(slug__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)|
                Q(user__email__icontains=query)
                )

        return self.filter(lookup)


class BlogPostManager(models.Manager):

    def get_queryset(self):
        return BlogPostQuerySet(self.model , using = self._db)

    def published(self):
        return self.get_queryset().published()

    def search(self , query = None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)




class BlogPost(models.Model):  #bloglist_set ---> queryset
    # id = IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=1)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)  # hello world --> hello-world
    content = models.TextField(null = True, blank=True)
    publish_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User,related_name="blog_likes", null=True, blank=True)
    dislikes = models.ManyToManyField(User,related_name="blog_dislikes", null=True, blank=True)
    objects = BlogPostManager()

    class Meta:
        ordering = ['-pk' , '-publish_date', '-timestamp', '-updated']

    def total_likes(self):
        return self.likes.all().count()

    def total_dislikes(self):
        return self.dislikes.all().count()
    
    def get_absolute_url(self):
        return f"/blog/{self.slug}/"

    def getCommentUrl(self):
        return f"/blog/{self.slug}/ajax/post/"

    def getReplyUrl(self):
        return "/blog/ajax/post/"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}edit/"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}delete/"

    @property
    def comment(self):
        # print((self.comment_set.all().order_by('-comment_date')))
        return self.comment_set.all().order_by('-comment_date')

    @property
    def number_of_comments(self):
        return self.comment_set.all().count()

    @property
    def sendSlug(self):
        return self.slug

    @property
    def get_object(self):
        # print((self.comment_set.all().order_by('-comment_date')))
        return (self.comment_set.filter().order_by('-comment_date').first())

    @property
    def get_posts(self):
        qr = BlogPost.objects.all().filter(user = self.user)     
        return qr[: len(qr)//2]



class Comment(models.Model):
    post = models.ForeignKey( BlogPost,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length = 25,null=True)
    body = models.TextField()
    comment_date = models.DateTimeField(auto_now_add = True)
    c_user = models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    
    def __str__(self):
        return '%s - %s' %(self.post.title , self.name)

    @property
    def reply(self):
        return self.reply_set.all().order_by("-reply_date")
    @property
    def number_of_reply(self):
        return self.reply_set.all().count()

class Reply(models.Model):
    replyto = models.ForeignKey(Comment,on_delete = models.CASCADE,null=True, blank = True)
    name = models.CharField(max_length = 25,null = True)
    body = models.TextField()
    reply_date = models.DateTimeField(auto_now_add = True)
    r_user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    def __str__(self):
        return '%s reply to - %s'%(self.name,self.replyto.name)
