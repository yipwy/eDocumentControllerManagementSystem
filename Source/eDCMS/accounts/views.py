from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegistrationForm, PasswordResetForm, ChangePasswordForm, CustomUserChangeForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from accounts.models import Profile
from .models import Profile
from generals.models import Branch, Department
from recordmgnts.models import Container
from pprint import pprint
import json
from django.db.models import Count, Q
from django.views import View


def mylogin(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active is None and user.is_superuser is None:
                messages.warning(request, f'Account is not activated.')
            else:
                # correct username and password login the user
                login(request, user)
                return redirect('accounts:home')

        else:
            messages.warning(request, f'Incorrect username or password.')

    return render(request, 'registration/login.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def load_department(request):
    branch_id = request.GET.get('branch')
    departments = Department.objects.filter(branch=branch_id)
    return render(request, 'accounts/dept_dropdown_list.html', {'departments': departments})


class MyPasswordResetView(auth_views.PasswordResetView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        return super(MyPasswordResetView, self).get(request, *args, **kwargs)


class MyPasswordConfirmView(auth_views.PasswordResetConfirmView):
    form_class = PasswordResetForm


class MyPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        return super(MyPasswordResetCompleteView, self).get(request, *args, **kwargs)


class MyPasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('accounts:profile_page')

    def get_success_message(self, cleaned_data):
        return 'Your password has been changed successfully.'


@login_required
def home(request):
    return render(request, 'accounts/home.html')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            fs = form.save()
            fs.modify_by = str(request.user)
            fs.save()
            messages.success(request, f'Your profile has been updated.')
            return redirect('accounts:profile_page')

    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/profile_update_form.html', {'form': form})


class dashboard_view(View):
    template_name = 'accounts/dashboard.html'

    def get(self, request, *args, **kwargs):
        dataset = Profile.objects \
            .values('is_active') \
            .annotate(is_active_count=Count('is_active', filter=Q(is_active=True)),
                      not_is_active_count=Count('is_active', filter=Q(is_active=False))) \
            .order_by('is_active')

        categories = list()
        is_active_series_data = list()
        not_is_active_series_data = list()

        for entry in dataset:
            categories.append('%s Active' % entry['is_active'])
            is_active_series_data.append(entry['is_active_count'])
            not_is_active_series_data.append(entry['not_is_active_count'])

        is_active_series = {
            'name': 'Active user',
            'data': is_active_series_data,
            'color': 'green'
        }

        not_is_active_series = {
            'name': 'Inactive user',
            'data': not_is_active_series_data,
            'color': 'red'
        }

        chart = {
            'chart': {'type': 'column'},
            'title': {'text': 'Active user on Current Platform'},
            'xAxis': {'categories': categories},
            'yAxis': {
                'title': {
                    'text': 'No.of users'},
                'tickInterval': 1
                    },
            'plotOptions': {
                'column': {
                    'pointPadding': 0.2,
                    'borderWidth': 0
                }
            },
            'series': [is_active_series, not_is_active_series]
        }

        dump = json.dumps(chart)

        return render(request, self.template_name, {'chart': dump})

    def post(self, request, *args, **kwargs):
        dataset = Department.objects \
            .values('department') \
            .annotate(IT_count=Count('department', filter=Q(department="IT")),
                      Sales_count=Count('department', filter=Q(department="Sales")),
                      Admin_count=Count('department', filter=Q(department="Admin")),
                      HR_count=Count('department', filter=Q(department="HR"))) \
            .order_by('department')

        categories = list()
        IT_series_data = list()
        Sales_series_data = list()
        Admin_series_data = list()
        HR_series_data = list()

        for entry in dataset:
            categories.append('%s Department' % entry['department'])
            IT_series_data.append(entry['IT_count'])
            Sales_series_data.append(entry['Sales_count'])
            Admin_series_data.append(entry['Admin_count'])
            HR_series_data.append(entry['HR_count'])

        IT_series = {
            'name': 'IT',
            'data': IT_series_data,
            'color': 'green'
        }

        Sales_series = {
            'name': 'Sales',
            'data': Sales_series_data,
            'color': 'yellow'
        }

        Admin_series = {
            'name': 'Admin',
            'data': Admin_series_data,
            'color': 'red'
        }

        HR_series = {
            'name': 'HR',
            'data': HR_series_data,
            'color': 'blue'
        }

        chart2 = {
            'chart': {'type': 'column'},
            'title': {'text': 'Containers per department'},
            'xAxis': {'categories': categories},
            'yAxis': {
                'title': {
                    'text': 'No.of containers'},
                'tickInterval': 1
                    },
            'plotOptions': {
                'column': {
                    'pointPadding': 0.2,
                    'borderWidth': 0
                }
            },
            'series': [IT_series, Sales_series, Admin_series, HR_series]
        }

        dump2 = json.dumps(chart2)

        return render(request, self.template_name, {'chart2': dump2})

# def json_chart(request):
#     return render(request, 'accounts/dashboard.html')
#
#
# def dashboard_viewDepartment(request):
#     dataset = Department.objects \
#         .values('department') \
#         .exclude(department='') \
#         .annotate(total=Count('department')) \
#         .order_by('department')
#
#     port_display_name = dict()
#     for port_tuple in Department.PORT_CHOICES:
#         port_display_name[port_tuple[0]] = port_tuple[1]
#
#     chart = {
#         'chart': {'type': 'pie'},
#         'title': {'text': 'Titanic Survivors by Ticket Class'},
#         'series': [{
#             'name': 'Department',
#             'data': list(map(lambda row: {'name': port_display_name[row['department']], 'y': row['total']}, dataset))
#         }]
#     }
#
#     return JsonResponse(chart)
