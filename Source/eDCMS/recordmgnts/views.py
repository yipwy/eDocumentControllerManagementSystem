from django.shortcuts import render
from .models import Container
from django.contrib.auth.decorators import login_required


@login_required
def showTable(request):

    allitem = Container.objects.all()
    context = {'allitem': allitem}
    return render(request, 'recordmgnts/records.html', context)
