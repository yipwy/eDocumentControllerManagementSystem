from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Container, OrderHeader, OrderDetail
from django.contrib.auth.decorators import login_required
from .forms import ContainerForm, ContainerTransactionForm
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.forms import modelformset_factory
from generals.models import DocumentType, SeriesNumber, Location
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from pprint import pprint


@login_required
def showContainer(request):

    allContainer = Container.objects.all()
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
        form = ContainerForm(request.POST)
        if form.is_valid():
            container = form.save()
            container.created_by = str(request.user)
            container.modify_by = str(request.user)
            container.save()
            return render(request, 'recordmgnts/success_added.html')
        else:
            messages.error(request, 'Adding unsuccessful')
    else:
        form = ContainerForm()
    return render(request, 'recordmgnts/new_container.html', {'form': form})


def load_locations(request):
    warehouse_id = request.GET.get('warehouse')
    locations = Location.objects.filter(warehouse=warehouse_id)
    return render(request, 'recordmgnts/location_dropdown.html', {'locations': locations})


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
            Q(container_serial_number__icontains=query) | Q(container_description__icontains=query)
        )
        return object_list


def containerUpdate(request, pk):
    template_name = 'recordmgnts/edit_records.html'
    container = get_object_or_404(Container, pk=pk)
    form = ContainerForm(request.POST or None, instance=container)
    if form.is_valid():
        container = form.save()
        container.modify_date = timezone.now()
        container.modify_by = str(request.user)
        container.save()
        messages.success(request, 'Successfully updated')
        return redirect('recordmgnts:records')

    return render(request, template_name, {'form': form})


@login_required
def transaction_log(request):
    now = datetime.now()
    initial_header_data = {
        'department': request.user.departmentId,
        'branch': request.user.branchId,
        'created_by': request.user.username,
        # 'created_date': now.strftime("%d/%m/%Y"),
    }
    DetailFormSet = modelformset_factory(OrderDetail, fields=['container'], extra=1)
    if request.method == 'POST':
        header_form = ContainerTransactionForm(request.POST)
        detail_form_set = DetailFormSet(request.POST)

        if header_form.is_valid():
            new_header = header_form.save(commit=False)

            if detail_form_set.is_valid():
                new_header.save()

                # calls function that takes a SeriesNumber object as parameter, returns instance of new SeriesNumber
                new_doc_series_number = create_new_doc_series_number(new_header.doc_type.document_number_seriesId)

                create_new_doctype(new_header.doc_type.document_code[0], new_header.doc_type.document_code[1:],
                                   new_doc_series_number)

                instances = detail_form_set.save(commit=False)
                for instance in instances:
                    instance.header = new_header
                    q = Container.objects.get(pk=instance.container.id)
                    instance.barcode = q.container_serial_number
                    q.is_active = False
                    q.save()
                    instance.save()
    else:
        header_form = ContainerTransactionForm(initial=initial_header_data)
        detail_form_set = DetailFormSet(queryset=OrderDetail.objects.none())

    return render(request, 'recordmgnts/container_transaction.html', {'header_form': header_form, 'detail_form': detail_form_set})


def load_series_number(request):
    document_id = request.GET.get('doc_type')
    document_series_number = DocumentType.objects.get(pk=document_id)
    return HttpResponse(document_series_number.document_number_seriesId)


def create_new_doc_series_number(doc_series_number):  # create a new SeriesNumber and returns the instance of it
    new_series_code = str("%04d" % doc_series_number.next_number)
    new_next_number = doc_series_number.next_number + 1
    new_doc_series_number = SeriesNumber(series_code=new_series_code, next_number=new_next_number, is_active=True)
    new_doc_series_number.save()
    return new_doc_series_number  # return an instance of the newly created SeriesNumber


def create_new_doctype(doctype, counter, new_doc_series_number): # create a new doctype when the current doctype is used
    if doctype is 'O':  # doctype == 'O' is a check out, doctype is the first letter of the current document_code
        counter = int(counter) + 1
        counter = "%04d" % counter  # returns a 4 digit counter e.g(0001 instead of 1)
        new_doc_code = 'O' + counter  # increments the counter and combine with letter 'O'
        new_doctype = DocumentType(document_code=new_doc_code, document_description="Document Check Out", is_active=True,
                                   document_number_seriesId=new_doc_series_number)
        new_doctype.save()
