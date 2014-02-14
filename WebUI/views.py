from django.shortcuts import render
from CarPool.settings import API_KEY
# Create your views here.
def home(request):
    return render(request, 'home.html', API_KEY)