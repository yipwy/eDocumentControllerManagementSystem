from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm, PasswordChangeForm
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'class': 'row col form-group'}))
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'class': 'row col form-group'}))
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact = forms.CharField(label="Contact Number", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    departmentId = forms.CharField(label="Department", widget=forms.TextInput(attrs={'class': 'form-control'}))
    companyId = forms.CharField(label="Company", widget=forms.TextInput(attrs={'class': 'form-control'}))
    branchId = forms.CharField(label="Branch", widget=forms.TextInput(attrs={'class': 'form-control'}))

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


# class CustomUserChangeForm(UserChangeForm):
#
#     class Meta(UserChangeForm):
#         model = Profile
#         fields = ('username', 'email')