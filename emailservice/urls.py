from django.urls import path
from django.views.decorators.cache import cache_page

from emailservice.apps import EmailserviceConfig
from emailservice.views import EmailservicePageVeiw, EmailserviceListView, MailingCreateView, MailingUpdateView, \
    MailingDetailView, MailingDeleteView, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    ClientDetailView, LogListView

app_name = EmailserviceConfig.name

urlpatterns = [
    path('', EmailservicePageVeiw.as_view(), name='home'),
    path('lk', EmailserviceListView.as_view(), name='lk'),
    path('create/<int:pk>/', MailingCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', MailingUpdateView.as_view(), name='edit'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('delete/<int:pk>/', cache_page(60)(MailingDeleteView.as_view()), name='delete'),
    path('client_list', ClientListView.as_view(), name='client_list'),
    path('create_client/<int:pk>/', ClientCreateView.as_view(), name='create_client'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client_edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('logs_list/', LogListView.as_view(), name='logs_list'),

]
