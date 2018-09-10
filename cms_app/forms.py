from django.forms import ModelForm
from .models import Realization


class RealizationForm(ModelForm):
    class Meta:
        model = Realization
        fields = ['realization', 'waste']