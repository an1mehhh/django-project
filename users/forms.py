from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div, HTML
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django import forms
from users.models import User


class UserRegisterForm(UserCreationForm):
    """Форма для регистрации пользователей"""
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Register')
        )


class UserProfileForm(UserChangeForm):
    """Форма для обновления профиля пользователя"""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'country', 'phone', 'avatar',)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('first_name', css_class='form-group col-md-4 mb-0'),
                Column('last_name', css_class='form-group col-md-2 mb-0'),
                Column('country', css_class='form-group col-md-4 mb-0'),
                Column('phone', css_class='form-group col-md-2 mb-0'),
                Column('avatar', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Update')
        )
        self.fields['password'].widget = forms.HiddenInput()


class CustomPasswordResetForm(PasswordResetForm):
    """Форма для сброса пароля пользователя"""
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            Submit('submit', 'Сбросить пароль', css_class='btn btn-primary')
        )

    class Meta:
        model = User
        fields = ['email']
