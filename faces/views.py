from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import *
from .functions import *
import tanda_api

# Create your views here.
def index(request):
    form = DetailsForm()
    return render(request, 'faces/index.html', {'detailsForm' : form})

def get_users(request):
    users_json = tanda_api.get_users_json()
    return HttpResponse(users_json)

def analyze(request):
    if request.POST:
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        url = request.POST.get('url', '')

    # User list to be put into webpage
    user_list = []
    if len(email) > 0 and len(password) > 0:
        # Gets dict for tanda users
        users = tanda_api.get_users(email, password)

        if 'error' in users:
            return HttpResponse('Login details are most likely incorrect')

        # Trys and download each image and give a confidence rating
        # if there is a picture
        for user in users:
            cur_user_dict = {}

            user_photo_url = user['photo']
            user_name = user['name']
            user_approachability, dorminant_emotion = get_approachability(user_photo_url)
            if user_approachability is None:
                user_approachability = 'image/face not found.'

            cur_user_dict['photo'] = user_photo_url
            cur_user_dict['name'] = user_name
            cur_user_dict['approachability'] = user_approachability
            cur_user_dict['dorminant_emotion'] = dorminant_emotion

            progress_bar_type = 'info'
            if user_approachability > 75:
                progress_bar_type = 'success'
            elif user_approachability < 50:
                progress_bar_type = 'warning'
            elif user_approachability < 25:
                progress_bar_type = 'danger'

            cur_user_dict['progress_bar_type'] = progress_bar_type

            user_list.append(cur_user_dict)

    elif len(url) > 0:
        cur_user_dict = {}
        user_approachability, dorminant_emotion = get_approachability(url)

        if user_approachability is None:
            user_approachability = 'image/face not found.'

        cur_user_dict['approachability'] = user_approachability
        cur_user_dict['photo'] = url
        cur_user_dict['name'] = 'anon'
        cur_user_dict['dorminant_emotion'] = dorminant_emotion

        progress_bar_type = 'info'
        if user_approachability > 75:
            progress_bar_type = 'success'
        elif user_approachability < 50:
            progress_bar_type = 'warning'
        elif user_approachability < 25:
            progress_bar_type = 'danger'

        cur_user_dict['progress_bar_type'] = progress_bar_type

        user_list.append(cur_user_dict)

    user_list = sorted(user_list, key=lambda k:k['approachability'], reverse=True)

    return render(request, 'faces/analyze.html', {'user_list': user_list}) 

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
