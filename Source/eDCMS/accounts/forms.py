from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm, PasswordChangeForm
from .models import Profile
from generals.models import Department, Branch, Company

# DEPARTMENT_CHOICES = [
#     ('HR', 'HR'),
#     ('Sales Admin', 'Sales Admin'),
#     ('Admin', 'Admin'),
#     ('IT', 'IT'),
#     ('Sales & Marketing', 'Sales & Marketing'),
#     ('Corporate Committee', 'Corporate Committee'),
#     ('Project Dept', 'Project Dept'),
#     ('Accounts', 'Accounts'),
# ]
#
# BRANCH_CHOICES = [
#     ('Kuala Lumpur', 'Kuala Lumpur'),
#     ('Perak', 'Perak'),
#     ('Johor', 'Johor'),
#     ('Penang', 'Penang'),
# ]
COMPANY_CHOICES = [
     ('Huayang', 'Huayang'),
     ('Agro-Mod Industries', 'Agro-Mod Industries'),
     ('Bison Holdings', 'Bison Holdings'),
     ('G Land Development', 'G Land Development'),
 ]


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    username = forms.CharField(label="Username")
    contact = forms.CharField(label="Contact Number")
    email = forms.EmailField(label="Email Address")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput())
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    company = forms.CharField(label="Company", widget=forms.Select(choices=COMPANY_CHOICES))
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=True)

    class Meta(UserCreationForm):
        model = Profile
        fields = ('first_name', 'last_name', 'username', 'email', 'contact', 'password1', 'password2', 'branch',
                  'department', 'company')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.none()

        if 'branch' in self.data:
            try:
                branch = int(self.data.get('branch'))
                self.fields['department'].queryset = Department.objects.filter(branch=branch)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['department'].queryset = self.instance.branch.department_set.order_by('department')


class PasswordResetForm(SetPasswordForm):
    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if self.user.is_superuser is not True and self.user.is_staff is not True:
            self.user.is_staff = False
            self.user.is_superuser = False
        if commit:
            self.user.save()

        return self.user


class ChangePasswordForm(PasswordChangeForm):
    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if self.user.is_superuser is not True and self.user.is_staff is not True:
            self.user.is_staff = False
            self.user.is_superuser = False
        if commit:
            self.user.save()

        return self.user


class CustomUserChangeForm(UserChangeForm):
    password = None
    username = forms.CharField(label="Username")
    contact = forms.CharField(label="Contact Number")
    email = forms.EmailField(label="Email Address")
    department = forms.ModelChoiceField(queryset=Department.objects.filter(), required=True)
    company = forms.CharField(label="Company", widget=forms.Select(choices=COMPANY_CHOICES))
    branch = forms.ModelChoiceField(queryset=Branch.objects.filter(), required=True)
    is_superuser = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'hidden'}))
    is_staff = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'hidden'}))

    class Meta(UserChangeForm):
        model = Profile
        fields = ('username', 'email', 'contact', 'company', 'branch', 'department', 'is_superuser', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.none()

        if 'branch' in self.data:
            try:
                branch = int(self.data.get('branch'))
                self.fields['department'].queryset = Department.objects.filter(branch=branch)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['department'].queryset = self.instance.branch.department_set.order_by('department')


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


