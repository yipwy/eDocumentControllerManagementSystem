from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm, PasswordChangeForm
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    username = forms.CharField(label="Username")
    contact = forms.CharField(label="Contact Number")
    email = forms.EmailField(label="Email Address")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput())
    departmentId = forms.CharField(label="Department")
    companyId = forms.CharField(label="Company")
    branchId = forms.CharField(label="Branch")

    class Meta(UserCreationForm):
        model = Profile
        fields = ('first_name', 'last_name', 'username', 'email', 'contact', 'password1', 'password2', 'departmentId', 'companyId', 'branchId')


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
    departmentId = forms.CharField(label="Department")
    companyId = forms.CharField(label="Company")
    branchId = forms.CharField(label="Branch")
    is_superuser = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'hidden'}))
    is_staff = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'hidden'}))

    class Meta(UserChangeForm):
        model = Profile
        fields = ('username', 'email', 'contact', 'departmentId', 'companyId', 'branchId', 'is_superuser', 'is_staff')
