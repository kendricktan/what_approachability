from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
import tanda_api

# Create your views here.
def index(request):
    form = DetailsForm()
    return render(request, 'faces/index.html', {'detailsForm' : form})

def analyze(request):
    if request.POST:
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
    tanda_api.get_users(email, password)
    return HttpResponse('analyze')
