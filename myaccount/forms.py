from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)
    phone = forms.CharField(
        max_length=12,
        min_length=12,  # Минимальная длина номера телефона
        validators=[MinLengthValidator(limit_value=12, message="Номер телефона введен не правильно")]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs.update({'value': '+7'})

    class Meta:
        model = User
        fields = ['username', 'company_name', 'phone', 'password1', 'password2']

class ChangeOrderStatusForm(forms.Form):
    order_id = forms.IntegerField()
    new_status = forms.IntegerField()
