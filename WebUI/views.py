import json
from django.http import HttpResponse
from django.shortcuts import render
from CarPool.settings import API_KEY
from utils import clusterize_latlngs
# Create your views here.
def home(request):
    return render(request, 'index.html', API_KEY)

def save_journey(request):
    if request.is_ajax() and request.method == "POST":
        res = json.loads(request.body)
        cords = res['cords']
        cords = [(x['d'],x['e']) for x in cords]
        distance = res['distance']
        clusters = clusterize_latlngs(cords, distance)
        return HttpResponse()