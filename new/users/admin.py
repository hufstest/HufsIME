from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Article, Like, Comment, Answer, TaggedPost, PostTag, Hit

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Article)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Answer)
admin.site.register(TaggedPost)
admin.site.register(PostTag)
admin.site.register(Hit)