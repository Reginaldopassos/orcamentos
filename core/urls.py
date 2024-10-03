from django.urls import path
from .views import index, CreateOrcaView, UpdOrcaView, DelOrcaView, login_index, gerar_pdf

urlpatterns = [
    path('', login_index, name='login'),
    path('index/', index.as_view(), name='index'),
    path('orcamento/', CreateOrcaView.as_view(), name='orcamento'),
    path('<int:pk>/update/', UpdOrcaView.as_view(), name='upd_orcamento'),
    path('<int:pk>/Delete/', DelOrcaView.as_view(), name='del_orcamento'),
    path('os/<int:pk>/pdf/', gerar_pdf, name='gerar_pdf'),


]