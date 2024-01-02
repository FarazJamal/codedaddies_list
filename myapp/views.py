from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

BASE_CRAIGLIST_URL = 'https://losangeles.craigslist.org/search/bbb?query={}'
BASE_IMAGE_URL = 'https://losangeles.craigslist.org/{}_300x300.jpg'

# Create your views here.

def home(request):
    return render (request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    if search: 
        final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
        models.Search.objects.create(search=search)
        response = requests.get(final_url)
        data = response.text
        soup = BeautifulSoup(data, features='html.parser')
        #print(final_url)
        post_listening = soup.find_all('li', { 'class' : 'gallery-card' })
        final_posting = []
        if post_listening:
            post_title = post_listening[0].find(class_='label').text
            post_url = post_listening[0].find('a').get('href')
            post_price = post_listening[0].find(class_='priceinfo').text

            for post in post_listening:
                post_title = post.find(class_='label').text
                post_url = post.find('a').get('href')
                if post.find(class_='priceinfo'):
                    post_price = post.find(class_='priceinfo').text
                else:
                    post_price = 'N/A'

            if post.find(class_='loading').get('data-ids'):
                post_image_id = post.find(class_='loading').get('data-pid').split(',')[0].split(':')
                print(post_image_id)
                post_image_url = BASE_IMAGE_URL.format(post_image_id)
            else:
                post_image_url = 'https://craigslist.org/images/peace.jpg'
                
            final_posting.append((post_title, post_url, post_price, post_image_url))

        else:
            print("No results found")
            
        post_titles = soup.find_all('a', {'class' : 'search'})

        for_frontend = {
            'search' : search,
            'final_posting' : final_posting,
        }
        return render(request, 'my_app/new_search.html', for_frontend)
    else:
        return render(request, 'my_app/new_search.html', {'error': 'Search cannot be empty'})