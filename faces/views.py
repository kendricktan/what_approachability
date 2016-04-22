from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from .functions import *
import tanda_api

# Create your views here.
def index(request):
    form = DetailsForm()
    return render(request, 'faces/index.html', {'detailsForm' : form})

def analyze(request):
    if request.POST:
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

    # Gets dict for tanda users
    users = tanda_api.get_users(email, password)

    # Trys and download each image and give a confidence rating
    # if there is a picture
    user_list = []
    for user in users:
        cur_user_dict = {}

        user_photo_url = user['photo']
        user_name = user['name']
        user_approachability = get_approachability(user_photo_url)

        cur_user_dict['photo'] = user_photo_url
        cur_user_dict['name'] = user_name
        cur_user_dict['approachability'] = user_approachability

        user_list.append(cur_user_dict)

    return render(request, 'faces/analyze.html', {'user_list': user_list}) 
