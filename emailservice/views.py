from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView

from blogs.services import get_articles_from_cache
from emailservice.forms import MailingForm, ClientForm
from emailservice.models import Mailing, Client, Log
from emailservice.services import get_mailings_from_cache
from users.models import User


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('emailservice:client_list')

    def form_valid(self, form):
        client_form = form.save()
        user = self.request.user
        client_form.owner = user
        client_form.save()
        return super().form_valid(form)


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client
    template_name = 'emailservice/client_detail.html'


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('emailservice:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('emailservice:client_list')


class EmailservicePageVeiw(TemplateView):
    template_name = 'emailservice/start.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['blogs'] = get_articles_from_cache().order_by('?')[:3]
        return context_data


class EmailserviceListView(ListView):
    model = Mailing
    template_name = 'emailservice/lk.html'

    def get_queryset(self):
        return get_mailings_from_cache()


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('emailservice:lk')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('emailservice:lk')


class MailingDetailView(DetailView):
    model = Mailing


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('emailservice:lk')


class LogListView(LoginRequiredMixin, ListView):
    model = Log