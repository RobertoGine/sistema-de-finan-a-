from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Transacao, ContaPagar
from .forms import TransacaoForm, ContaPagarForm
from io import BytesIO
from xhtml2pdf import pisa
from datetime import date
from .forms import CustomUserCreationForm
from django.contrib import messages

#teste envio de email
#from django.http import HttpResponse
#from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso.')
            return redirect('financas:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'financas/register.html', {'form': form})


# def login(request):
#     return render(request, 'financas/login.html')
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('financas:dashboard') 
        else:
            messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.')
    return render(request, 'financas/login.html')


@login_required
def dashboard(request):
    ultimas = Transacao.objects.filter(usuario=request.user).order_by('-data')[:5]
    # cálculo rápido do mês atual
    hoje = date.today()
    trans_mes = Transacao.objects.filter(usuario=request.user, data__year=hoje.year, data__month=hoje.month)
    total_receitas = trans_mes.filter(tipo='R').aggregate(total=Sum('valor'))['total'] or 0
    total_despesas = trans_mes.filter(tipo='D').aggregate(total=Sum('valor'))['total'] or 0
    saldo = total_receitas - total_despesas
    contexto = {
        'ultimas': ultimas,
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
    }
    return render(request, 'financas/dashboard.html', contexto)


@login_required
def lista_transacoes(request):
    transacoes = Transacao.objects.filter(usuario=request.user).order_by('-data')
    return render(request, 'financas/lista_transacoes.html', {'transacoes': transacoes})


@login_required
def criar_transacao(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            trans = form.save(commit=False)
            trans.usuario = request.user
            trans.save()
            messages.success(request, 'Transação criada com sucesso.')
            return redirect('financas:lista_transacoes')
    else:
        form = TransacaoForm()
    return render(request, 'financas/form_transacao.html', {'form': form})


@login_required
def editar_transacao(request, pk):
    trans = get_object_or_404(Transacao, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = TransacaoForm(request.POST, instance=trans)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transação atualizada.')
            return redirect('financas:lista_transacoes')
    else:
        form = TransacaoForm(instance=trans)
    return render(request, 'financas/form_transacao.html', {'form': form})


@login_required
def excluir_transacao(request, pk):
    trans = get_object_or_404(Transacao, pk=pk, usuario=request.user)
    if request.method == 'POST':
        trans.delete()
        messages.success(request, 'Transação excluída.')
        return redirect('financas:lista_transacoes')
    return render(request, 'financas/confirmar_exclusao.html', {'trans': trans})


@login_required
def relatorio_mensal(request):
    hoje = date.today()
    mes = int(request.GET.get('mes', hoje.month))
    ano = int(request.GET.get('ano', hoje.year))

    transacoes = Transacao.objects.filter(usuario=request.user, data__year=ano, data__month=mes)
    total_receitas = transacoes.filter(tipo='R').aggregate(total=Sum('valor'))['total'] or 0
    total_despesas = transacoes.filter(tipo='D').aggregate(total=Sum('valor'))['total'] or 0
    saldo = total_receitas - total_despesas

    contexto = {
        'transacoes': transacoes.order_by('-data'),
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
        'mes': mes,
        'ano': ano,
    }
    return render(request, 'financas/relatorio_mensal.html', contexto)


@login_required
def gerar_pdf_relatorio(request):
    hoje = date.today()
    mes = int(request.GET.get('mes', hoje.month))
    ano = int(request.GET.get('ano', hoje.year))

    transacoes = Transacao.objects.filter(usuario=request.user, data__year=ano, data__month=mes)
    total_receitas = transacoes.filter(tipo='R').aggregate(total=Sum('valor'))['total'] or 0
    total_despesas = transacoes.filter(tipo='D').aggregate(total=Sum('valor'))['total'] or 0
    saldo = total_receitas - total_despesas

    contexto = {
        'transacoes': transacoes.order_by('-data'),
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
        'mes': mes,
        'ano': ano,
        'usuario': request.user,
    }

    html = render_to_string('financas/relatorio_pdf.html', contexto)
    result = BytesIO()

    pisa_status = pisa.CreatePDF(src=html, dest=result)

    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_{ano}_{mes}.pdf"'
    return response 


#criar conta a pagar
@login_required
def cadastrar_conta(request):
    if request.method == "POST":
        form = ContaPagarForm(request.POST)
        if form.is_valid():
            conta = form.save(commit=False)
            conta.usuario = request.user
            conta.save()
            messages.success(request, "Conta cadastrada com sucesso!")
            return redirect("financas:listar_contas")
    else:
        form = ContaPagarForm()

    return render(request, 'financas/cadastrar_conta.html', {'form': form})

#verificar
'''@login_required
def listar_contas(request):
    contas = ContaPagar.objects.filter(usuario=request.user).order_by('data_vencimento')
    return render(request, 'listar_contas.html', {'contas': contas})
'''
@login_required
def listar_contas(request):
    contas = ContaPagar.objects.filter(usuario=request.user).order_by("data_vencimento")
    return render(request, "financas/listar_contas.html", {"contas": contas})


@login_required
def criar_conta(request):
    if request.method == "POST":
        form = ContaPagarForm(request.POST)
        if form.is_valid():
            conta = form.save(commit=False)
            conta.usuario = request.user
            conta.save()
            messages.success(request, "Conta cadastrada com sucesso!")
            return redirect("financas:listar_contas")
    else:
        form = ContaPagarForm()

    return render(request, "financas/form_conta.html", {"form": form})


@login_required
def editar_conta(request, pk):
    conta = get_object_or_404(ContaPagar, pk=pk, usuario=request.user)

    if request.method == "POST":
        form = ContaPagarForm(request.POST, instance=conta)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta atualizada com sucesso!")
            return redirect("financas:listar_contas")
    else:
        form = ContaPagarForm(instance=conta)

    return render(request, "financas/form_conta.html", {"form": form, "editar": True})


@login_required
def excluir_conta(request, pk):
    conta = get_object_or_404(ContaPagar, pk=pk, usuario=request.user)

    if request.method == "POST":
        conta.delete()
        messages.success(request, "Conta excluída com sucesso!")
        return redirect("financas:listar_contas")

    return render(request, "financas/confirmar_exclusao_conta.html", {"conta": conta})


@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')

#teste envio de email
'''def teste_email(request):
    try:
        send_mail(
            subject="Teste - Render + Brevo",
            message="Se você recebeu isso, o SMTP está funcionando!",
            from_email=None,  # usa DEFAULT_FROM_EMAIL
            recipient_list=["robertogine.dev@gmail.com"],
            fail_silently=False,
        )
        return HttpResponse("E-mail enviado com sucesso!")
    except Exception as e:
        return HttpResponse(f"Erro ao enviar: {e}")'''
