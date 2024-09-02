from django.forms import ModelForm

from emailservice.models import Mailing, Client


class MailingForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(owner=self.request.user)

    class Meta:
        model = Mailing
        fields = ('name', 'message', 'clients', 'period_mail', 'start_mail', 'stop_mail', 'next_send_time')


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'last_name', 'email', 'comment')
