import json
from django.http import HttpResponse
from django.shortcuts import render
from CarPool.settings import API_KEY
from utils import clusterize_latlngs
from django.contrib.auth.decorators import login_required
# Create your views here.


def welcome(request):
    return render(request, 'index.html')

def new_trip(request):
    return render(request,'createJourney.html',API_KEY)

def home(request):
    return render(request, 'home.html')

def save_journey(request):
    if request.is_ajax() and request.method == "POST":
        res = json.loads(request.body)
        cords = res['cords']
        cords = [(x['d'],x['e']) for x in cords]
        distance = res['distance']
        clusters = clusterize_latlngs(cords, distance)
        return HttpResponse()

