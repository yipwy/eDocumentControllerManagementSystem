from django import forms
from .models import Container, OrderHeader, OrderDetail
from generals.models import Warehouse, DocumentType, Location


class ContainerForm(forms.ModelForm):
    #  warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all(), empty_label=None)
    container_serial_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter serial number'}))
    container_description = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Enter description'}), max_length=100)
    status = forms.BooleanField(required=False, label='Status of container')

    class Meta:
        model = Container
        fields = ['container_serial_number', 'container_description', 'status', 'warehouse', 'location']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.none()

        if 'warehouse' in self.data:
            try:
                warehouse_id = int(self.data.get('warehouse'))
                self.fields['location'].queryset = Location.objects.filter(warehouse=warehouse_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['location'].queryset = self.instance.warehouse.location_set


class ContainerTransactionForm(forms.ModelForm):
    doc_type = forms.ModelChoiceField(queryset=DocumentType.objects.filter(is_active=True))

    class Meta:
        model = OrderHeader
        fields = ['doc_type', 'doc_serial_number', 'created_by', 'branch', 'department', 'created_date']
        labels = {
            'doc_type': 'Document Type',
            'created_by': 'User',
            'doc_serial_number': 'Document Code'
        }

    def __init__(self, *args, **kwargs):
        super(ContainerTransactionForm, self).__init__(*args, **kwargs)
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


# class FormWithFormattedDates(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         date_format = None
#         if 'date_format' in kwargs:
#             date_format = kwargs['date_format']
#             del kwargs['date_format']
#         super(FormWithFormattedDates, self).__init__(*args, **kwargs)
#         if date_format is not None:
#             for (field_name, field) in self.fields.items():
#                 if isinstance(field, forms.fields.DateField):
#                     field.input_format = [date_format]
#                     field.widget = forms.widgets.DateTimeInput(format=date_format)
