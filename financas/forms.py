from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transacao, ContaPagar


class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['tipo', 'categoria', 'valor', 'data', 'descricao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Digite um e-mail válido.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ContaPagarForm(forms.ModelForm):
    class Meta:
        model = ContaPagar
        fields = ["titulo", "valor", "data_vencimento", "descricao"]
    ''' widgets = {
            "data_vencimento": forms.DateInput(attrs={'type': 'date'}),
        }
'''