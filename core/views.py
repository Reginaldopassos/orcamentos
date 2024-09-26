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
    template_name = 'orcamento.html'
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

    # Configuração da fonte
    p.setFont("Helvetica-Bold", 12)
    p.drawString(20 * mm, 250 * mm, "REGI REFORMAS")

    p.setFont("Helvetica", 10)
    p.drawString(20 * mm, 240 * mm, "ENDEREÇO: RUA BELO HORIZONTE 182")
    p.drawString(20 * mm, 235 * mm, "CNPJ: 35.453.960/0001-91")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(20 * mm, 220 * mm, "ORÇAMENTO")

    p.setFont("Helvetica", 12)
    p.drawString(20 * mm, 210 * mm, f"Cliente: {orc.cliente}")
    p.drawString(20 * mm, 200 * mm, f"Rua: {orc.endereco}")
    p.drawString(20 * mm, 190 * mm, f"OS: {orc.id}")
    p.drawString(20 * mm, 180 * mm, f"Serviço: {orc.servico}")

    p.drawString(20 * mm, 170 * mm, "Descrição detalhada:")
    y = 160 * mm
    for item in orc.descricao.split(';'):
        item = item.strip()
        if item:
            p.drawString(30 * mm, y, f"- {item}")
            y -= 10 * mm

    # Formatar o valor como moeda
    formatted_valor = f"R$ {orc.valor:,.2f}".replace('.', '.')  # Exemplo: R$ 1.234,56
    p.setFont("Helvetica-Bold", 12)
    p.drawString(20 * mm, y - 10 * mm, f"Valor: {formatted_valor}")

    p.showPage()
    p.save()
    return response