import json
from django.http import HttpResponse
from django.shortcuts import render
from CarPool.settings import API_KEY
# Create your views here.
def home(request):
    return render(request, 'index.html', API_KEY)


def save_journey(request):
    if request.is_ajax() and request.method == "POST":
        print json.loads(request.body)
        return HttpResponse()