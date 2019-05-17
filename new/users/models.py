from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    objects = CustomUserManager()

class Article(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    @property
    def like_count(self):
      return self.like_user_set.count()
    like_user_set = models.ManyToManyField(
        CustomUser,
        null=True,
        blank=True,
        related_name='like_user_set',
        through='Like',
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

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
      unique_together = (
          ('user', 'article')
      )
class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
    )
    comment_text=models.CharField(max_length = 300)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.comment_text
class Answer(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        CustomUser,on_delete=models.CASCADE,
    )
    answer_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

