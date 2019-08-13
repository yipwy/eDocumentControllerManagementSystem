from django import forms
from .models import Container, OrderHeader, OrderDetail
from generals.models import Warehouse, DocumentType, Bay
from tinymce.widgets import TinyMCE
from pprint import pprint

ROW = (
    ('', '--------'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5')
)

COL = (
    ('', '--------'),
    ('1', '1'),
    ('2', '2')
)


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class ContainerForm(forms.ModelForm):
    #  warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all(), empty_label=None)
    container_serial_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter serial number'}))
    container_description = forms.CharField(required=False, widget=TinyMCEWidget(attrs={'placeholder': 'Enter description'}))
    # container_description = forms.CharField(required=False, widget=Textarea(attrs={'placeholder': 'Enter description'}), max_length=100)
    # status = forms.BooleanField(required=False, label='Status of container')
    row = forms.ChoiceField(choices=ROW)
    column = forms.ChoiceField(choices=COL)

    class Meta:
        model = Container
        fields = ['container_serial_number', 'container_description', 'warehouse', 'bay', 'row', 'column']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bay'].queryset = Bay.objects.none()

        if 'warehouse' in self.data:
            try:
                warehouse_id = int(self.data.get('warehouse'))
                self.fields['bay'].queryset = Bay.objects.filter(warehouse=warehouse_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['bay'].queryset = self.instance.warehouse.bay_set


class ContainerTransactionForm(forms.ModelForm):
    doc_type = forms.ModelChoiceField(queryset=DocumentType.objects.filter(is_active=True), label='<b>Document Type:</b>')

    class Meta:
        model = OrderHeader
        fields = ['doc_type', 'doc_serial_number', 'created_by', 'branch', 'department', 'created_date']
        labels = {
            'created_by': '<b>User:</b>',
            'doc_serial_number': '<b>Document Code:</b>',
            'branch': '<b>Branch:</b>',
            'department': '<b>Department:</b>',
            'created_date': '<b>Created Date:</b>',
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

class RequiredFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        self.forms[0].empty_permitted = False


class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return text_html + data_list


class OrderDetailForm(forms.ModelForm):
    my_default_errors = {
        'required': 'This field cannot be left empty.',
        'invalid': 'Enter a valid value.',
    }

    container = forms.ModelChoiceField(queryset=Container.objects.all(), error_messages=my_default_errors)

    # def __init__(self, *args, **kwargs):
    #     _data_list = kwargs.pop('data_list', None)
    #     super(OrderDetailForm, self).__init__(*args, **kwargs)
    #     self.fields['container'].widget = ListTextWidget(data_list=_data_list, name='container')

    class Meta:
        model = OrderDetail
        fields = ['container']


class TransactionFormView(forms.Form):
    doc_type = forms.CharField(label="<b>Document Type:</b>", widget=forms.TextInput(attrs={'readonly': True}))
    doc_serial_number = forms.CharField(label="<b>Document Code:</b>", widget=forms.TextInput(attrs={'readonly': True}))
    created_by = forms.CharField(label="<b>User:</b>", widget=forms.TextInput(attrs={'readonly': True}))
    branch = forms.CharField(label="<b>Branch:</b>", widget=forms.TextInput(attrs={'readonly': True}))
    department = forms.CharField(label="<b>Department:</b>", widget=forms.TextInput(attrs={'readonly': True}))
    created_date = forms.CharField(label="<b>Created Date:</b>", widget=forms.TextInput(attrs={'readonly': True}))
    container = forms.CharField(label="<b>Container:</b>", widget=forms.TextInput(attrs={'readonly': True}))

