from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

class UserRegisterForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)
    phone = forms.CharField(
        max_length=12,
        min_length=12,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].initial = '+7'

    class Meta:
        model = User
        fields = ['phone', 'company_name', 'password1', 'password2']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(username=phone).exists():
            raise forms.ValidationError('Пользователь с таким номером телефона уже зарегистрирован')
        return phone

    error_messages = {
        'password_mismatch': _('Пароли не совпадают'),
        'password_too_short': _('Пароль слишком короткий. Минимальная длина пароля - 6 символов.'),
        'password_entirely_numeric': _('Пароль не может состоять только из цифр.'),
    }


class ChangeOrderStatusForm(forms.Form):
    order_id = forms.IntegerField()
    new_status = forms.IntegerField()
