from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

class SignupForm(ModelForm): #회원가입을 제공하는 class이다.
    password_check = forms.CharField(max_length=200, widget=forms.PasswordInput())
#아쉽게도 User 모델에서는 password_check 필드를 제공해주지 않는다.
#따라서 따로 password_check 필드를 직접 정의해줄 필요가 있다.
#입력 양식은 type은 기본이 text이다. 따라서 다르게 지정해주고 싶을 경우 widget을 이용한다.
#widget=forms.PasswordInput()은 입력 양식을 password로 지정해주겠다는 뜻이다.

    field_order=['username','password','password_check','last_name','first_name','email']
#field_order는 만들어지는 입력양식의 순서를 정해준다.
#여기서 사용한 이유는 password 바로 밑에 password_check 입력양식을 추가시키고 싶어서이다.
#만약 따로 field_order를 지정해주지않았다면, password_check는 맨 밑에 생성된다.

    class Meta:
        model=User
        widgets = {'password':forms.PasswordInput}
        fields = ['username','password','last_name','first_name','email']
#User model에 정의된 username, passwordm last_name, first_name, email을 입력양식으로

class SigninForm(ModelForm): #로그인을 제공하는 class이다.
    class Meta:
        model = User
        widgets = {'password':forms.PasswordInput}
        field = ['username','password']