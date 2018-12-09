from django.forms import ModelForm, RadioSelect
from .models import Realization, Interruption, Order


class RealizationForm(ModelForm):
    class Meta:
        model = Realization
        fields = ['realization', 'waste']


class InterruptionForm(ModelForm):
    class Meta:
        model = Interruption
        fields = ['cause_1', 'cause_2', 'cause_3']
        widgets = {
            'cause_1': RadioSelect(),
            'cause_2': RadioSelect(),
            'cause_3': RadioSelect(),
        }


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['order_id', 'machine', 'planned']

