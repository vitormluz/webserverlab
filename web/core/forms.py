from django import forms
from django.core.mail.message import EmailMessage
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

from .models import Produto


class ProdutoModelForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'estoque', 'imagem']


class ContatoForm(forms.Form):
    nome = forms.CharField(label='Seu nome')
    email = forms.CharField(label='Seu e-mail')
    assunto = forms.CharField(label='Assunto')
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea())

    def send_mail(self):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        assunto = self.cleaned_data['assunto']
        mensagem = self.cleaned_data['mensagem']

        conteudo = f'Nome: {nome}\E-mail: {email}\Assunto: {assunto}\nMensagem: {mensagem}'
        mail = EmailMessage(
            subject="E-mail enviado por zeroUm do BR",
            body=conteudo,
            from_email="contato@zeroum.com",
            to=['contato@zeroum.com',],
            headers={'Reply to': email}
        )
        mail.send


class CadastroUsuario(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].validators = []

    def clean_password2(self):
        password2 = self.cleaned_data.get("password2")
        return password2


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
