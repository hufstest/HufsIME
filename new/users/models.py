from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    objects = CustomUserManager()

class article(models.Model):
    content = models.TextField()

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)

    like_user_set = models.ManyToManyField(
        CustomUser,
        null=True,
        blank=True,
        related_name='like_user_set',
        through='Like',
    )

    comment_user_set = models.ManyToManyField(
        CustomUser,
        null=True,
        blank=True,
        related_name='comment_user_set',
        through= "comment"
    )

    answer_user_set = models.ManyToManyField(
        CustomUser,
        null=True,
        blank=True,
        related_name='answer_user_set',
        through='answer',
    )

class Like(models.Model):

    article = models.ForeignKey(
        article, on_delete=models.CASCADE,
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
class comment(models.Model):
    article = models.ForeignKey(
        article, on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
    )
    comment_text=models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )
class answer(models.Model):
    article = models.ForeignKey(
        article, on_delete=models.CASCADE,
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

