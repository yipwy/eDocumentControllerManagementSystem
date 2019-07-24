from django.shortcuts import render, get_object_or_404, redirect
from .models import Container, OrderHeader, OrderDetail
from django.contrib.auth.decorators import login_required
from .forms import ContainerForm, ContainerTransactionForm
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from generals.models import DocumentType


@login_required
def showContainer(request):

    allContainer = Container.objects.all()
    context = {'allContainer': allContainer}
    return render(request, 'recordmgnts/records.html', context)


def showHeader(request):

    allHeader = OrderHeader.objects.all()
    context = {'allHeader': allHeader}
    return render(request, 'recordmgnts/records.html', context)


def showDetail(request):

    allDetail = OrderDetail.objects.all()
    context = {'allDetail': allDetail}
    return render(request, 'recordmgnts/records.html', context)


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
        form = ContainerForm()
    return render(request, 'recordmgnts/new_container.html', {'form': form})


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
        return redirect('recordmgnts:records')

    return render(request,template_name, {'form':form})


@login_required
def transactionlog(request):
    initial_data ={
        'doc_serial_number': DocumentType.objects.get(pk=1).document_number_seriesId,
        'department': request.user.departmentId,
        'branch': request.user.branchId,
        'created_by': request.user.username,
    }

    if request.method == 'POST':
        form = ContainerTransactionForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContainerTransactionForm(initial=initial_data)

    return render(request,'recordmgnts/container_transaction.html', {'form': form})


