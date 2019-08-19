from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, reverse
from .models import Container, OrderHeader, OrderDetail, ContainerInstance
from django.contrib.auth.decorators import login_required
from .forms import ContainerForm, ContainerTransactionForm, RequiredFormSet, OrderDetailForm, TransactionFormView
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.forms import modelformset_factory
from generals.models import DocumentType, Bay
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import *
from dateutil.relativedelta import relativedelta
from pprint import pprint
from django.db.models.functions import Concat
from django.db.models import Value as V, CharField
import sys
from subprocess import run, PIPE


@login_required
def showContainer(request):

    allContainer = Container.objects.filter(department=request.user.department)
    paginator = Paginator(allContainer, 5)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        query_sets = paginator.page(1)
    except EmptyPage:
        query_sets = paginator.page(paginator.num_pages)
    context = {'allContainer': query_sets}
    return render(request, 'recordmgnts/records.html', context)


def showHeader(request):

    allHeader = OrderHeader.objects.all()
    context = {'allHeader': allHeader}
    return render(request, 'recordmgnts/transaction_log.html', context)


def showDetail(request):

    allDetail = OrderDetail.objects.all()
    context = {'allDetail': allDetail}
    return render(request, 'recordmgnts/transaction_log.html', context)


def addContainer(request):
    if request.method == 'POST':
        pprint('form is valid')
        form = ContainerForm(request.POST)
        if form.is_valid():
            container = form.save(commit=False)
            container.created_by = str(request.user)
            container.modify_by = str(request.user)
            container.department = request.user.department
            container.save()
            return render(request, 'recordmgnts/success_added.html')
        else:
            messages.error(request, 'Adding unsuccessful')
    else:
        form = ContainerForm()
    return render(request, 'recordmgnts/new_container.html', {'form': form})


def load_locations(request):
    warehouse_id = request.GET.get('warehouse')
    bays = Bay.objects.filter(warehouse=warehouse_id)
    return render(request, 'recordmgnts/location_dropdown.html', {'bays': bays})


class ContainerDetailView(LoginRequiredMixin, DetailView):
    template_name = 'recordmgnts/records_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Container, id=id_)


@login_required
def containerDelete(request,id):
    container = Container.objects.get(pk=id)
    container.delete()
    messages.success(request, f'Record has been deleted.')
    return redirect('recordmgnts:records')


class SearchContainerView(LoginRequiredMixin, ListView):
    model = Container
    template_name = 'recordmgnts/search_container_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Container.objects.filter(
            Q(container_serial_number__icontains=query) & Q(department=self.request.user.department.id) |
            Q(container_description__icontains=query) & Q(department=self.request.user.department.id)
        )
        return object_list

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SearchContainerView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


def containerUpdate(request, pk):
    template_name = 'recordmgnts/edit_records.html'
    container = get_object_or_404(Container, pk=pk)

    if container.status is not True:
        messages.warning(request, 'Please check in this container before updating')
        return redirect('recordmgnts:records')

    form = ContainerForm(request.POST or None, instance=container)
    if form.is_valid():
        container = form.save()
        container.modify_date = datetime.now()
        container.modify_by = str(request.user)
        container.save()
        messages.success(request, 'Successfully updated')
        return redirect('recordmgnts:records')

    return render(request, template_name, {'form': form})


@login_required
def transaction_log(request):
    now = date.today()
    initial_header_data = {
        'department': request.user.department,
        'branch': request.user.branch,
        'created_by': request.user.username,
        'created_date': now,
    }
    DetailFormSet = modelformset_factory(OrderDetail, form=OrderDetailForm, formset=RequiredFormSet, extra=3)
    if request.method == 'POST':
        header_form = ContainerTransactionForm(request.POST)
        detail_form_set = DetailFormSet(request.POST)

        if header_form.is_valid():
            new_header = header_form.save(commit=False)
            new_header.created_date = datetime.now()

            if detail_form_set.is_valid():
                current_doctype = new_header.doc_type
                current_doctype.is_active = False  # set used document type to inactive
                current_doctype.save()
                new_header.save()
                doc_type = new_header.doc_type.document_code[0]
                doc_num = new_header.doc_type.document_code[1:]
                #  create a new doctype with new doc_code
                create_new_doctype(doc_type, doc_num)

                instances = detail_form_set.save(commit=False)
                for instance in instances:
                    create_container_instance(doc_type, instance.container, request.user, new_header.created_date)
                    instance.header = new_header
                    q = Container.objects.get(pk=instance.container.id)
                    instance.barcode = q.container_serial_number
                    if doc_type is 'O':
                        q.status = False
                    elif doc_type is 'I':
                        q.status = True
                    q.save()
                    instance.save()
                messages.success(request, 'Transaction made successfully')
            elif detail_form_set.is_valid() is False:
                header_form = ContainerTransactionForm(initial=initial_header_data)
    else:
        header_form = ContainerTransactionForm(initial=initial_header_data)
        detail_form_set = DetailFormSet(queryset=OrderDetail.objects.none())

    return render(request, 'recordmgnts/container_transaction.html', {'header_form': header_form, 'detail_form': detail_form_set})


def load_series_number(request):
    document_id = request.GET.get('doc_id')
    document_series_number = DocumentType.objects.get(pk=document_id)
    return HttpResponse(document_series_number.document_code)


# def create_new_doc_series_number(doc_series_number):  # create a new SeriesNumber and returns the instance of it
#     new_series_code = str("%04d" % doc_series_number.next_number)
#     new_next_number = doc_series_number.next_number + 1
#     new_doc_series_number = SeriesNumber(series_code=new_series_code, next_number=new_next_number, is_active=True)
#     new_doc_series_number.save()
#     return new_doc_series_number  # return an instance of the newly created SeriesNumber


def create_new_doctype(doctype, counter): #  new_doc_series_number): # create a new doctype when the current doctype is used
    if doctype is 'O':  # doctype == 'O' is a check out, doctype is the first letter of the current document_code
        counter = int(counter) + 1
        counter = "%04d" % counter  # returns a 4 digit counter e.g(0001 instead of 1)
        new_doc_code = 'O' + counter  # increments the counter and combine with letter 'O'
        new_doctype = DocumentType(document_code=new_doc_code, document_description="Document Check Out", is_active=True
                                   )
        new_doctype.save()

    if doctype is 'I':  # doctype == 'I' is a check in, doctype is the first letter of the current document_code
        counter = int(counter) + 1
        counter = "%04d" % counter  # returns a 4 digit counter e.g(0001 instead of 1)
        new_doc_code = 'I' + counter  # increments the counter and combine with letter 'O'
        new_doctype = DocumentType(document_code=new_doc_code, document_description="Document Check In", is_active=True
                                   )
        new_doctype.save()


def load_containers(request):
    document = request.GET.get('doc_type')
    doc_type = document[0]
    if doc_type is 'O':
        containers = Container.objects.filter(status=True, department=request.user.department)
    elif doc_type is 'I':
        container_instance = ContainerInstance.objects.values_list('container', flat=True).filter(status=False, user=request.user)
        containers = Container.objects.filter(id__in=container_instance, status=False)
    return render(request, 'recordmgnts/container_dropdown.html', {'containers': containers})


@login_required
def transaction_history_view(request):
    current_user = request.user.username
    order_header = OrderHeader.objects.filter(created_by=current_user).order_by('-created_date')
    paginator = Paginator(order_header, 5)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        query_sets = paginator.page(1)
    except EmptyPage:
        query_sets = paginator.page(paginator.num_pages)
    context = {'order_header': query_sets}
    return render(request, 'recordmgnts/transaction_history.html', context)


@login_required
def transaction_form_view(request, id):
    current_order_header = OrderHeader.objects.get(id=id)
    current_order_details = OrderDetail.objects.filter(header=current_order_header)
    display_data = {
        'doc_type': current_order_header.doc_type.document_description,
        'doc_serial_number': current_order_header.doc_type.document_code,
        'department': current_order_header.department,
        'branch': current_order_header.branch,
        'created_by': current_order_header.created_by,
        'created_date': current_order_header.created_date,
    }
    form = TransactionFormView(initial=display_data)
    context = {'form': form, 'details': current_order_details}
    return render(request, 'recordmgnts/transaction_form_view.html', context)


def create_container_instance(doctype, container, user, date):
    #  to record checked out document due date and return status
    if doctype is 'O':
        status = False
        due_date = date + relativedelta(months=+3)
        container_instance = ContainerInstance(container=container, user=user, due_date=due_date, status=status)
        container_instance.save()

    if doctype is 'I':
        container_instance_object = ContainerInstance.objects.get(container=container, status=False, user=user)
        previous_email_sent = container_instance_object.email_sent
        container_instance_object.status = True
        if previous_email_sent is not True:
            container_instance_object.email_sent = False
        else:
            container_instance_object.email_sent = True
        container_instance_object.save()


def concat_location(bay, row, column):
    return str(bay) + str(row) + str(column)


def barcode_scanner(request):
    out = run([sys.executable, 'C:\\Users\\pan_ch.DMHUAYANG\\PycharmProjects\\eDocumentControllerManagementSystem\\Source\\eDCMS\\barcode_capture.py'],
              shell=False, stdout=PIPE, text=True)
    barcode = out.stdout
    # barcode = barcode.decode('ascii')
    print(barcode)
    initial_data = {'container_serial_number': barcode}
    # if request.method == 'POST':
    #     form = ContainerForm(request.POST)
    #     if form.is_valid():
    #         container = form.save()
    #         container.created_by = str(request.user)
    #         container.modify_by = str(request.user)
    #         container.department = request.user.department
    #         container.save()
    #         return render(request, 'recordmgnts/success_added.html')
    #     else:
    #         messages.error(request, 'Adding unsuccessful')
    # else:
    #     form = ContainerForm(initial=initial_data)

    return HttpResponse(barcode)


