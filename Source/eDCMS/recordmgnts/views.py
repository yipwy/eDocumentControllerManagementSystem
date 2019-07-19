from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Container, OrderHeader, OrderDetail
from django.contrib.auth.decorators import login_required



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


class ContainerDetailView(DetailView):
    template_name = 'recordmgnts/records_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Container, id=id_)

