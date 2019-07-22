from django.shortcuts import render, get_object_or_404, redirect
from .models import Container, OrderHeader, OrderDetail
from django.contrib.auth.decorators import login_required
from .forms import ContainerForm
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


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
            return render(request, 'recordmgnts/SuccessAdded.html')
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





