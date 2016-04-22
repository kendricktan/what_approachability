from django.shortcuts import render
from django.http import HttpResponse
from .forms import *

# Create your views here.
def index(request):
    form = DetailsForm()
    return render(request, 'faces/index.html', {'detailsForm' : form})

def analyze(request):
    return HttpResponse('analyze')
