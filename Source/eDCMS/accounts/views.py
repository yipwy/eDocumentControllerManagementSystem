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
from pprint import pprint
import json
from django.db.models import Count, Q
from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView
from recordmgnts.models import Container


def mylogin(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active is None and user.is_superuser is None:
                messages.warning(request, f'Account is not activated')
            else:
                # correct username and password login the user
                login(request, user)
                return redirect('accounts:home')

        else:
            messages.warning(request, f'Incorrect username or password')

    return render(request, 'registration/login.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        email = form.data['email']
        email += "@huayang.com.my"
        username = str(form.data['first_name']) + " " + str(form.data['last_name'])
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.created_by = username
            new_form.modify_by = username
            new_form.email = email
            new_form.save()
            messages.success(request, f'Your account has been created')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def load_department(request):
    branch_id = request.GET.get('branch')
    departments = Department.objects.filter(branch=branch_id)
    if request.user.is_authenticated:
        current_department = request.user.department
        return render(request, 'accounts/dept_dropdown_list.html', {'departments': departments, 'curr_dept': current_department})
    else:
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
        return 'Your password has been changed successfully'


@login_required
def home(request):
    return render(request, 'accounts/home.html')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def update_profile(request):
    email_name = request.user.email.split('@', 1)[0]
    initial_data = {
        'username': request.user.username,
        'contact': request.user.contact,
        'email': email_name,
        'department': request.user.department,
        'company': request.user.company,
        'branch': request.user.branch,
        'is_superuser': request.user.is_superuser,
        'is_staff': request.user.is_staff,
        'is_documentcontroller': request.user.is_documentcontroller
    }
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        email = form.data['email']
        email += "@huayang.com.my"
        if form.is_valid():
            fs = form.save(commit=False)
            fs.email = email
            fs.modify_by = str(request.user)
            fs.save()
            messages.success(request, f'Your profile has been updated')
            return redirect('accounts:profile_page')

    else:
        form = CustomUserChangeForm(initial=initial_data)
    return render(request, 'accounts/profile_update_form.html', {'form': form})


# class dashboard_view(View):
#     template_name = 'accounts/dashboard.html'
class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_dept(self):
        dataset = Container.objects \
            .values('department') \
            .annotate(IT_count=Count('department', filter=Q(department='IT') & Q(is_deleted=False)),
                      Ceo_count=Count('department', filter=Q(department='CEO') & Q(is_deleted=False)),
                      Corp_comm_count=Count('department', filter=Q(department='Corp Comm') & Q(is_deleted=False)),
                      Management_count=Count('department', filter=Q(department='Management') & Q(is_deleted=False)),
                      Sales_marketing_count=Count('department', filter=Q(department='Sales & Marketing') & Q(is_deleted=False)),
                      Admin_count=Count('department', filter=Q(department='Admin') & Q(is_deleted=False)),
                      Project_count=Count('department', filter=Q(department='Project') & Q(status=False) & Q(is_deleted=False)),
                      Accounts_count=Count('department', filter=Q(department='Accounts & Finance') & Q(is_deleted=False)),
                      Sales_admin_count=Count('department', filter=Q(department='Sales Admin') & Q(is_deleted=False)),
                      HR_count=Count('department', filter=Q(department='HR') & Q(is_deleted=False))) \
            .order_by('department')

        categories = list()
        IT_series_data = list()
        Sales_marketing_series_data = list()
        Sales_admin_series_data = list()
        Ceo_series_data = list()
        Corp_comm_series_data = list()
        Management_series_data = list()
        Admin_series_data = list()
        Accounts_series_data = list()
        Project_series_data = list()
        HR_series_data = list()

        for entry in dataset:
            if entry['department'] == 'CEO':
                categories.append('CEO')
            else:
                categories.append('%s Department' % entry['department'])
            IT_series_data.append(entry['IT_count'])
            Sales_marketing_series_data.append(entry['Sales_marketing_count'])
            Admin_series_data.append(entry['Admin_count'])
            Sales_admin_series_data.append((entry['Sales_admin_count']))
            Accounts_series_data.append(entry['Accounts_count'])
            Ceo_series_data.append(entry['Ceo_count'])
            Corp_comm_series_data.append(entry['Corp_comm_count'])
            Management_series_data.append(entry['Management_count'])
            Project_series_data.append(entry['Project_count'])
            HR_series_data.append(entry['HR_count'])

        IT_series = {
            'name': 'IT',
            'data': IT_series_data,
            'color': 'green'
        }

        Sales_marketing_series = {
            'name': 'Sales & Marketing',
            'data': Sales_marketing_series_data,
            'color': 'yellow'
        }

        Sales_admin_series = {
            'name': 'Sales Admin',
            'data': Sales_admin_series_data,
            'color': 'purple'
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

        Accounts_series = {
            'name': 'Accounts & Finance',
            'data': Accounts_series_data,
            'color': 'black'
        }

        Ceo_series = {
            'name': 'CEO',
            'data': Ceo_series_data,
            'color': 'grey'
        }

        Corp_comm_series = {
            'name': 'Corp Comm',
            'data': Corp_comm_series_data,
            'color': 'pink'
        }

        Management_series = {
            'name': 'Management',
            'data': Management_series_data,
            'color': 'brown'
        }

        Project_series = {
            'name': 'Project',
            'data': Project_series_data,
            'color': 'orange'
        }

        chart2 = {
            'chart': {
                'type': 'column',
                'backgroundColor': '#E3F0E6',
                'option3d': {
                    'enabled': "true",
                    'alpha': 10,
                    'beta': 15,
                    'depth': 50,
                }
            },
            'title': {'text': 'Containers per Department'},
            'xAxis': {'categories': categories},
            'yAxis': {
                'title': {
                    'text': 'No.of containers'},
                'tickInterval': 1
            },
            'plotOptions': {
                'column': {
                    'stacking': 'normal',
                    'groupPadding': 0.3,
                    'pointPadding': 0.3,
                    'depth': 60,
                }
            },
            'series': [Ceo_series, Project_series, IT_series, Sales_marketing_series, Admin_series,
                       Sales_admin_series, HR_series, Accounts_series, Corp_comm_series, Management_series],
            'colorByPoint': "true",
        }

        dump2 = json.dumps(chart2)

        return dump2

    def get_profile(self):
        dataset = Profile.objects \
            .values('is_active') \
            .annotate(is_active_count=Count('is_active', filter=Q(is_active=True)),
                      not_is_active_count=Count('is_active', filter=Q(is_active=False))) \
 \
            # categories = list('User')
        is_active_series_data = list()
        not_is_active_series_data = list()

        for entry in dataset:
            # categories.append('User')
            if entry['is_active_count'] >= 0 :
                is_active_series_data.append(entry['is_active_count'])
            if entry['not_is_active_count'] >= 0 :
                not_is_active_series_data.append(entry['not_is_active_count'])

        is_active_series = {
            'name': 'Active user',
            'data': is_active_series_data,
            'color': '#23CE3F'
        }

        not_is_active_series = {
            'name': 'Inactive user',
            'data': not_is_active_series_data,
            'color': '#FB3A3A'
        }

        chart = {
            'chart': {
                'type': 'column',
                'backgroundColor': '#E3F0E6',
                'options3d': {
                    'enabled': "true",
                    'alpha': 10,
                    'beta': 15,
                    'depth': 50,
                }
            },
            'title': {'text': 'Active Users on Current Platform'},
            'xAxis': {'categories': ['']},
            'yAxis': {
                'title': {
                    'text': 'No.of users'},
                'tickInterval': 1
            },
            'plotOptions': {
                'column': {
                    'pointPadding': 0.2,
                    'borderWidth': 0,
                    'depth': 60,
                }
            },
            'series': [is_active_series, not_is_active_series]
        }

        dump = json.dumps(chart)

        return dump

    def get_containers(self):
        dataset = Container.objects \
            .values('department') \
            .annotate(IT_count=Count('department', filter=Q(department='IT') & Q(status=False) & Q(is_deleted=False)),
                      Ceo_count=Count('department', filter=Q(department='CEO') & Q(status=False) & Q(is_deleted=False)),
                      Corp_comm_count=Count('department', filter=Q(department='Corp Comm') & Q(status=False) & Q(is_deleted=False)),
                      Management_count=Count('department', filter=Q(department='Management') & Q(status=False) & Q(is_deleted=False)),
                      Admin_count=Count('department', filter=Q(department='Admin') & Q(status=False) & Q(is_deleted=False)),
                      Sales_admin_count=Count('department', filter=Q(department='Sales Admin') & Q(status=False) & Q(is_deleted=False)),
                      Sales_marketing_count=Count('department', filter=Q(department='Sales & Marketing') & Q(status=False)& Q(is_deleted=False)),
                      Project_count=Count('department', filter=Q(department='Project') & Q(status=False) & Q(is_deleted=False)),
                      Accounts_count=Count('department', filter=Q(department='Accounts & Finance') & Q(status=False) & Q(is_deleted=False)),
                      HR_count=Count('department', filter=Q(department='HR') & Q(status=False) & Q(is_deleted=False))) \
            .order_by('department')

        categories = list()
        IT_series_data = list()
        Sales_marketing_series_data = list()
        Sales_admin_series_data = list()
        Project_series_data = list()
        Admin_series_data = list()
        Accounts_series_data = list()
        HR_series_data = list()
        Ceo_series_data = list()
        Corp_comm_series_data = list()
        Management_series_data = list()

        for entry in dataset:
            if entry['department'] == 'CEO':
                categories.append('CEO')
            else:
                categories.append('%s Department' % entry['department'])
            IT_series_data.append(entry['IT_count'])
            Sales_marketing_series_data.append(entry['Sales_marketing_count'])
            Admin_series_data.append(entry['Admin_count'])
            Sales_admin_series_data.append((entry['Sales_admin_count']))
            Accounts_series_data.append(entry['Accounts_count'])
            Ceo_series_data.append(entry['Ceo_count'])
            Corp_comm_series_data.append(entry['Corp_comm_count'])
            Management_series_data.append(entry['Management_count'])
            Project_series_data.append(entry['Project_count'])
            HR_series_data.append(entry['HR_count'])

        IT_series = {
            'name': 'IT',
            'data': IT_series_data,
            'color': 'green'
        }

        Sales_marketing_series = {
            'name': 'Sales & Marketing',
            'data': Sales_marketing_series_data,
            'color': 'yellow'
        }

        Sales_admin_series = {
            'name': 'Sales Admin',
            'data': Sales_admin_series_data,
            'color': 'purple'
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

        Accounts_series = {
            'name': 'Accounts & Finance',
            'data': Accounts_series_data,
            'color': 'black'
        }

        Ceo_series = {
            'name': 'CEO',
            'data': Ceo_series_data,
            'color': 'grey'
        }

        Corp_comm_series = {
            'name': 'Corp Comm',
            'data': Corp_comm_series_data,
            'color': 'pink'
        }

        Management_series = {
            'name': 'Management',
            'data': Management_series_data,
            'color': 'brown'
        }

        Project_series = {
            'name': 'Project',
            'data': Project_series_data,
            'color': 'orange'
        }

        chart3 = {
            'chart': {
                'type': 'column',
                'backgroundColor': '#E3F0E6',
                'option3d': {
                    'enabled': "true",
                    'alpha': 10,
                    'beta': 15,
                    'depth': 50,
                }
            },
            'title': {'text': 'Checked Out Containers per Department'},
            'xAxis': {'categories': categories},
            'yAxis': {
                'title': {
                    'text': 'No.of containers'},
                'tickInterval': 1
            },
            'plotOptions': {
                'column': {
                    'stacking': 'normal',
                    'groupPadding': 0.3,
                    'pointPadding': 0.3,
                    'depth': 60,
                }
            },
            'series': [Ceo_series, Project_series, IT_series, Sales_marketing_series, Admin_series,
                       Sales_admin_series, HR_series, Accounts_series, Corp_comm_series, Management_series],
            'colorByPoint': "true",
        }

        dump3 = json.dumps(chart3)

        return dump3

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chart'] = self.get_profile()
        context['chart2'] = self.get_dept()
        context['chart3'] = self.get_containers()
        return context

    # def post(self, request, *args, **kwargs):
    #     dataset = Department.objects \
    #         .values('department') \
    #         .annotate(IT_count=Count('department', filter=Q(department="IT")),
    #                   Sales_count=Count('department', filter=Q(department="Sales")),
    #                   Admin_count=Count('department', filter=Q(department="Admin")),
    #                   HR_count=Count('department', filter=Q(department="HR"))) \
    #         .order_by('department')
    #
    #     categories = list()
    #     IT_series_data = list()
    #     Sales_series_data = list()
    #     Admin_series_data = list()
    #     HR_series_data = list()
    #
    #     for entry in dataset:
    #         categories.append('%s Department' % entry['department'])
    #         IT_series_data.append(entry['IT_count'])
    #         Sales_series_data.append(entry['Sales_count'])
    #         Admin_series_data.append(entry['Admin_count'])
    #         HR_series_data.append(entry['HR_count'])
    #
    #     IT_series = {
    #         'name': 'IT',
    #         'data': IT_series_data,
    #         'color': 'green'
    #     }
    #
    #     Sales_series = {
    #         'name': 'Sales',
    #         'data': Sales_series_data,
    #         'color': 'yellow'
    #     }
    #
    #     Admin_series = {
    #         'name': 'Admin',
    #         'data': Admin_series_data,
    #         'color': 'red'
    #     }
    #
    #     HR_series = {
    #         'name': 'HR',
    #         'data': HR_series_data,
    #         'color': 'blue'
    #     }
    #
    #     chart2 = {
    #         'chart': {
    #             'type': 'column',
    #             'backgroundColor': '#E3F0E6',
    #             'option3d': {
    #                 'enabled': "true",
    #                 'alpha': 10,
    #                 'beta': 15,
    #                 'depth': 50,
    #             }
    #         },
    #         'title': {'text': 'Containers per department'},
    #         'xAxis': {'categories': categories},
    #         'yAxis': {
    #             'title': {
    #                 'text': 'No.of containers'},
    #             'tickInterval': 1
    #                 },
    #         'plotOptions': {
    #             'column': {
    #                 'pointPadding': 0.2,
    #                 'borderWidth': 0,
    #                 'depth': 60,
    #             }
    #         },
    #         'series': [IT_series, Sales_series, Admin_series, HR_series],
    #         'colorByPoint': "true",
    #     }
    #
    #     dump2 = json.dumps(chart2)
    #
    #     return render(request, self.template_name, {'chart2': dump2})

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
