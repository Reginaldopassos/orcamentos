from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Orcamento
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import datetime
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
    ano_atual = datetime.now().year
    # Tamanho da página A4 (em mm)
    PAGE_WIDTH, PAGE_HEIGHT = A4
    MARGIN_LEFT = 13 * mm  # Margem externa esquerda
    MARGIN_RIGHT = PAGE_WIDTH - 13 * mm  # Margem externa direita
    MARGIN_TOP = PAGE_HEIGHT - 13 * mm  # Margem externa superior
    MARGIN_BOTTOM = 13 * mm  # Margem externa inferior

    PADDING = 10 * mm  # Espaçamento entre o conteúdo e as margens
    LINE_HEIGHT = 12 * mm  # Espaço entre as linhas
    y = MARGIN_TOP - PADDING  # Posicionamento inicial logo abaixo do topo da margem

    # Função para desenhar as margens
    def desenhar_margens():
        p.setStrokeColorRGB(0, 0, 0)  # Cor preta para as bordas
        p.setLineWidth(1)
        p.rect(MARGIN_LEFT, MARGIN_BOTTOM, MARGIN_RIGHT - MARGIN_LEFT, MARGIN_TOP - MARGIN_BOTTOM)

    # Desenhar as margens da primeira página
    desenhar_margens()

    # Configuração da fonte
    p.setFont("Helvetica-Bold", 12)
    p.drawString(MARGIN_LEFT + PADDING, y, "REGI REFORMAS")

    y -= 12 * mm
    p.setFont("Helvetica", 10)
    p.drawString(MARGIN_LEFT + PADDING, y, "ENDEREÇO: RUA BELO HORIZONTE 182")
    y -= 6 * mm
    p.drawString(MARGIN_LEFT + PADDING, y, "CNPJ: 35.453.960/0001-91")

    y -= 25 * mm  # Espaço extra antes do título "ORÇAMENTO"
    p.setFont("Helvetica-Bold", 12)
    p.drawString(MARGIN_LEFT + PADDING, y, "ORÇAMENTO")

    y -= 12 * mm
    p.setFont("Helvetica", 12)
    p.drawString(MARGIN_LEFT + PADDING, y, f"Cliente: {orc.cliente}")
    y -= 12 * mm
    p.drawString(MARGIN_LEFT + PADDING, y, f"Rua: {orc.endereco}")
    y -= 12 * mm
    p.drawString(MARGIN_LEFT + PADDING, y, f"OS: {ano_atual}{orc.id}")
    y -= 12 * mm
    p.drawString(MARGIN_LEFT + PADDING, y, f"Serviço: {orc.servico}")

    y -= 12 * mm
    p.drawString(MARGIN_LEFT + PADDING, y, "Descrição detalhada:")

    y -= 12 * mm

    # Iterar sobre os itens da descrição
    for item in orc.descricao.split(';'):
        item = item.strip()
        if item:
            if y <= MARGIN_BOTTOM + PADDING:  # Verifica se estamos próximo da margem inferior
                p.showPage()  # Cria uma nova página
                desenhar_margens()  # Desenha margens na nova página
                p.setFont("Helvetica", 12)
                y = MARGIN_TOP - PADDING  # Recomeça abaixo do topo da nova página

            p.drawString(MARGIN_LEFT + PADDING + 10 * mm, y, f"- {item}")
            y -= LINE_HEIGHT  # Move para a próxima linha

    # Verifica novamente se temos espaço suficiente para o valor na página
    if y <= MARGIN_BOTTOM + PADDING:
        p.showPage()
        desenhar_margens()
        p.setFont("Helvetica-Bold", 12)
        y = MARGIN_TOP - PADDING

    # Formatar o valor como moeda
    formatted_valor = f"R$ {orc.valor:,.2f}".replace('.', ',')
    p.drawString(MARGIN_LEFT + PADDING, y, f"Valor: {formatted_valor}")

    p.showPage()
    p.save()
    return response