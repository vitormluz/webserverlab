from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


from .forms import ContatoForm, ProdutoModelForm, CadastroUsuario
from .models import Produto


@login_required(login_url='cadastro')
def index(request):
    context = {
        "produtos": Produto.objects.all()
    }
    return render(request, 'core/index.html', context)


def contato(request):
    form = ContatoForm(request.POST or None)

    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail()

            messages.success(request, 'E-Mail enviado com sucesso!')
            form = ContatoForm()
        else:
            messages.error(request, 'Erro ao enviar o e-mail')

    context = {
        'form': form
    }
    return render(request, 'core/contato.html', context)


def produto(request):
    if str(request.method) == 'POST':
        form = ProdutoModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            messages.success(request, "Produto salvo com sucesso!") 
            form = ProdutoModelForm() 
        else:
            messages.error(request, 'Erro ao salvar o produto.')  
    else:
        form = ProdutoModelForm
    context = {
        'form': form
    }
    return render(request, 'core/produto.html', context)


def cadastro(request):
    form = CadastroUsuario(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('index')  

    context = {
        'form': form
    }
    return render(request, 'core/cadastro.html', context)


def login(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('index')
            else:
                messages.error(request, 'Nome de usuário ou senha inválidos.')

    context = {
        'form': form
    }
    return render(request, 'core/login.html', context)



def listar_usuarios(request):
    usuarios = User.objects.all()
    context = {
        'usuarios': usuarios
    }
    return render(request, 'core/usuarios.html', context)
