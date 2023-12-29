from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

BASE_CRAIGLIST_URL = 'https://newyork.craigslist.org/search/bbb?query={}'

# Create your views here.

def home(request):
    return render (request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    response = requests.get('https://newyork.craigslist.org/search/bbb?query=python#search=1~thumb~0~0')
    data = response.text
    print(data)
    for_frontend = {
        'search' : search
    }
    return render(request, 'my_app/new_search.html', for_frontend)