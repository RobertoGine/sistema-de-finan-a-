from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Transacao
from .forms import TransacaoForm
from io import BytesIO
from xhtml2pdf import pisa
from datetime import date


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso.')
            return redirect('financas:dashboard')
    else:
        form = UserCreationForm()
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

    # 🔥 A correção está aqui:
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_{ano}_{mes}.pdf"'
    return response

@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')