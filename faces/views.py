from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import *
from .functions import *
import tanda_api

EMAIL = None
PASSWORD = None
URL = None

# Create your views here.
def index(request):
    form = DetailsForm()
    return render(request, 'faces/index.html', {'detailsForm' : form})

def get_users(request):
    global EMAIL, PASSWORD, URL
    print(EMAIL, PASSWORD)
    users_json = tanda_api.get_users_json(email=EMAIL, password=PASSWORD)    
    return HttpResponse(users_json)

def analyze(request):  
    global EMAIL, PASSWORD, URL  
    if request.POST:
        EMAIL = request.POST.get('email', '')
        PASSWORD = request.POST.get('password', '')
        URL = request.POST.get('url', '')

    return render(request, 'faces/analyze.html', {'email': EMAIL, 'password': PASSWORD, 'url': URL})

def custom_url(request):
    urlForm = URLForm() 
    return render(request, 'faces/custom_url.html', {'urlForm': urlForm})

def dump_json(request, url):
    user_dict = {}
    user_approachability, dorminant_emotion = get_approachability(url)

    if user_approachability is not None:
        user_dict['approachability'] = user_approachability
        user_dict['dorminant_emotion'] = dorminant_emotion

    else:
        user_dict['error'] = 'no picture in url found'

    #json_return = json.dumps(user_dict)
    return JsonResponse(user_dict)
