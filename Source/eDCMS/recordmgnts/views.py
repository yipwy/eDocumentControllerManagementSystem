from django.shortcuts import render, redirect
from .models import Container, OrderHeader, OrderDetail
from django.contrib.auth.decorators import login_required
from .forms import ContainerForm


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
            return redirect('new_container/SuccessAdded.html')
    else:
        form = ContainerForm()
    return render(request, 'recordmgnts/new_container.html', {'form': form})






