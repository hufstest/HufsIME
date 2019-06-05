from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Article, Comment, Answer

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # fields = '__all__'
        fields = ['title', 'content', 'user', 'tags', 'anonymity']
        widgets = {
            'title': forms.TextInput(
				attrs={
					'class': 'form-control'
					}
				),
            'content': forms.Textarea(
				attrs={
					'class': 'form-control'
					}
				),
            'tags': forms.TextInput(
				attrs={
					'class': 'form-control'
                    }
                ),
            }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {
            'comment_text': forms.TextInput(
				attrs={
					'class': 'form-control'
					}
				),
			}


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'
        widgets = {
            'answer_text': forms.Textarea(
				attrs={
					'class': 'form-control'
					}
				),
			}