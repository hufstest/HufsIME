from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TagBase, TaggedItemBase
from django.template.defaultfilters import slugify as default_slugify
# Create your models here.
from django.contrib.auth.models import AbstractUser, UserManager
from datetime import timezone, datetime

class PostTag(TagBase):
    # NOTE: django-taggit does not allow unicode by default.
    slug = models.SlugField(
        verbose_name= 'slug',
        unique=True,
        max_length=100,
        allow_unicode=True,
    )

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def slugify(self, tag, i=None):
        return default_slugify(tag)


class TaggedPost(TaggedItemBase):
    content_object = models.ForeignKey(
        'Article',
        on_delete=models.CASCADE,
    )

    tag = models.ForeignKey(
        'PostTag',
        related_name="%(app_label)s_%(class)s_items",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "tagged post"
        verbose_name_plural = "tagged posts"

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    objects = CustomUserManager()

class Article(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    hits = models.IntegerField(default = 0)
    anonymity = models.BooleanField(default=True)
    @property #get 역할을 한다고 봐도 무방하다.
    def like_count(self):
      return self.like_user_set.count()
    like_user_set = models.ManyToManyField(
        CustomUser,
        null=True,
        blank=True,
        related_name='like_user_set',
        through='Like',
    )
    tags = TaggableManager(
        verbose_name= 'tags',
        help_text= 'A comma-separated list of tags.',
        blank=True,
        through=TaggedPost,
    )
    # comment_user_set = models.ManyToManyField(
    #     CustomUser,
    #     null=True,
    #     blank=True,
    #     related_name='comment_user_set',
    #     through= "comment"
    # )

    # answer_user_set = models.ManyToManyField(
    #     CustomUser,
    #     null=True,
    #     blank=True,
    #     related_name='answer_user_set',
    #     through='answer',
    # )
class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)
    class Meta:
      unique_together = (
          ('user', 'article')
      )

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    comment_text=models.CharField(max_length = 300)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)
    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.comment_text

class Answer(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,)
    answer_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)

class Hit(models.Model):
    ip = models.CharField(max_length=50,null = False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE,)
    date = models.CharField(max_length=30,null=True, blank=True)
    class Meta:
      unique_together = (
          ('ip', 'article', 'date')
      )

