from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Orcamento
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings

def login(request):
    return render(request, 'login.html')

class index(ListView):
    model = Orcamento
    template_name = 'index.html'
    context_object_name = 'orcamentos'
    paginate_by = 20
    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            busca = Orcamento.objects.filter(pk__icontains=search)
        else:
            busca = Orcamento.objects.all()
        return busca.order_by('pk')


class CreateOrcaView(CreateView):
    model = Orcamento
    template_name = 'orcamento.html'
    fields = ['cliente', 'endereco', 'servico', 'descricao', 'valor']
    success_url = reverse_lazy('index')


class UpdOrcaView(UpdateView):
    model = Orcamento
    template_name = 'update-orcamento.html'
    fields = ['cliente', 'endereco', 'servico', 'descricao', 'valor']
    success_url = reverse_lazy('index')


class DelOrcaView(DeleteView):
    model = Orcamento
    template_name = 'del_orcamento.html'
    success_url = reverse_lazy('index')


def gerar_pdf(request, pk):
    orc = get_object_or_404(Orcamento, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="orcamento_{orc.id}.pdf"'
    p = canvas.Canvas(response, pagesize=A4)

    # Tamanho da página A4 (em mm)
    PAGE_HEIGHT = A4[1]
    MARGIN_BOTTOM = 20 * mm  # Margem inferior
    LINE_HEIGHT = 10 * mm  # Espaço entre as linhas
    y = 250 * mm  # Posição inicial vertical

    # Configuração da fonte
    p.setFont("Helvetica-Bold", 12)
    p.drawString(20 * mm, y, "REGI REFORMAS")

    y -= 10 * mm
    p.setFont("Helvetica", 10)
    p.drawString(20 * mm, y, "ENDEREÇO: RUA BELO HORIZONTE 182")
    y -= 5 * mm
    p.drawString(20 * mm, y, "CNPJ: 35.453.960/0001-91")

    y -= 20 * mm
    p.setFont("Helvetica-Bold", 12)
    p.drawString(20 * mm, y, "ORÇAMENTO")

    y -= 10 * mm
    p.setFont("Helvetica", 12)
    p.drawString(20 * mm, y, f"Cliente: {orc.cliente}")
    y -= 10 * mm
    p.drawString(20 * mm, y, f"Rua: {orc.endereco}")
    y -= 10 * mm
    p.drawString(20 * mm, y, f"OS: {orc.id}")
    y -= 10 * mm
    p.drawString(20 * mm, y, f"Serviço: {orc.servico}")

    y -= 10 * mm
    p.drawString(20 * mm, y, "Descrição detalhada:")

    y -= 10 * mm

    # Iterar sobre os itens da descrição
    for item in orc.descricao.split(';'):
        item = item.strip()
        if item:
            if y <= MARGIN_BOTTOM:  # Verifica se estamos na margem inferior da página
                p.showPage()  # Cria uma nova página
                p.setFont("Helvetica", 12)
                y = PAGE_HEIGHT - 20 * mm  # Recomeça no topo da nova página

            p.drawString(30 * mm, y, f"- {item}")
            y -= LINE_HEIGHT  # Move para a próxima linha

    # Verifica novamente se temos espaço suficiente para o valor na página
    if y <= MARGIN_BOTTOM:
        p.showPage()
        p.setFont("Helvetica-Bold", 12)
        y = PAGE_HEIGHT - 20 * mm

    # Formatar o valor como moeda
    formatted_valor = f"R$ {orc.valor:,.2f}".replace('.', '.')
    p.drawString(20 * mm, y, f"Valor: {formatted_valor}")

    p.showPage()
    p.save()
    return response