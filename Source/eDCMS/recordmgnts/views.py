from django.shortcuts import render
from .models import Container
# Create your views here.


def showtable(request):

    allitem = Container.objects.all()
    context = {'allitem': allitem}
    return render(request, 'recordmgnts/Records.html', context)
