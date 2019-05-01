from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CreateUserForm(UserCreationForm): # 내장 회원가입 폼을 상속받아서 확장한다.
    hashtag= forms.CharField(required=True) # 이메일 필드 추가

    class Meta:
        model = User
        fields = ("username","password1", "password2","hashtag")

    def save(self, commit=True): # 저장하는 부분 오버라이딩
        user = super(CreateUserForm, self).save(commit=False) # 본인의 부모를 호출해서 저장하겠다.
        user.hashtag = self.cleaned_data["hashtag"]
        if commit:
            user.save()
        return user