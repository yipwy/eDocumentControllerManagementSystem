from django import forms
from .models import Container
from generals.models import Warehouse


class ContainerForm(forms.ModelForm):
    warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all(), empty_label=None),
    container_serial_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter serial number'})),
    container_description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter description'}), max_length=100),
    is_active = forms.BooleanField(required=False,
                                   label='Available?')

    class Meta:
        model = Container
        fields = ['container_serial_number', 'container_description', 'is_active', 'warehouse']