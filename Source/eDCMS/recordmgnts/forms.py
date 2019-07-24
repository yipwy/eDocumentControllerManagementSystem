from django import forms
from .models import Container, OrderHeader
from generals.models import Warehouse
from accounts.models import Profile


class ContainerForm(forms.ModelForm):
    warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all(), empty_label=None)
    container_serial_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter serial number'}))
    container_description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter description'}), max_length=100)
    is_active = forms.BooleanField(required=False,
                                   label='Available?')

    class Meta:
        model = Container
        fields = ['container_serial_number', 'container_description', 'is_active', 'warehouse']


class ContainerTransactionForm(forms.ModelForm):

    class Meta:
        model = OrderHeader
        fields = ['doc_type', 'doc_serial_number', 'created_by', 'branch', 'department', 'created_date']
        labels = {
            'doc_serial_number': 'Document Serial Number',
            'doc_type': 'Document Type',
            'created_by': 'User',
        }

    def __init__(self, *args, **kwargs):
        super(ContainerTransactionForm,self).__init__(*args, **kwargs)
        # self.fields['doc_type'].widget = forms.TextInput(attrs={
        #     'readonly': True
        # })
        self.fields['created_by'].widget = forms.TextInput(attrs={
            'readonly': True,
        })
        self.fields['branch'].widget = forms.TextInput(attrs={
            'readonly': True
        })
        self.fields['department'].widget = forms.TextInput(attrs={
            'readonly': True,
        })
        self.fields['doc_serial_number'].widget = forms.TextInput(attrs={
            'readonly': True,
        })
        self.fields['created_date'].widget = forms.TextInput(attrs={
            'readonly': True,
        })
