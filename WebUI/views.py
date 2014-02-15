import json
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render
from CarPool.settings import API_KEY
from utils import clusterize_latlngs
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from models import CustomUser, Request, Trip
# Create your views here.


def welcome(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    return render(request, 'index.html')

@login_required
def new_trip(request):
    if request.method=='GET':
        return render(request,'createJourney.html',API_KEY)
    else:
        return HttpResponseNotAllowed()

@login_required
def home(request):
    if request.method=='GET':
        return render(request, 'home.html')
    else:
        return HttpResponseNotAllowed()


def signup(request):
    if request.method=='POST':
        try:
            first_name = request.POST['first']
            last_name = request.POST['last']
            email = request.POST['email']
            password = request.POST['password']
            contact = request.POST['contact']

            user = CustomUser.objects.create_user(email, first_name, last_name, contact, password=password)
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/home/')
                else:
                    return HttpResponseRedirect('/welcome/')

            return HttpResponseRedirect('/welcome/')

        except KeyError:
            return HttpResponseRedirect('/welcome/')
    else:
        return HttpResponseNotAllowed()

def signin(request):
    if request.method=='POST':
        try:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/home/')
                else:
                    return HttpResponseRedirect('/welcome/')

            return HttpResponseRedirect('/welcome/')

        except KeyError:
            return HttpResponseRedirect('/welcome/')
    else:
        return HttpResponseNotAllowed()

@login_required
def save_journey(request):
    if request.is_ajax() and request.method == "POST":
        res = json.loads(request.body)
        cords = res['cords']
        cords = [(x['d'],x['e']) for x in cords]
        distance = res['distance']
        start_place = res['startPlace']
        end_place = res['endPlace']
        clusters = clusterize_latlngs(cords, distance)

        return HttpResponse()

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/welcome/')

@login_required
def search_trip(request):
    return render(request,'searchjourney.html')