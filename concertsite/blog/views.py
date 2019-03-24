from django.shortcuts import render
from django.http import HttpResponse
from .myfunctions import *


def index_page(request):
    # The function render will render (put together) our template blog/index_page.html
    context = {}
    if(request.method == 'POST'):
        artist_name = request.POST.get('artist', '')
        if((' ' in artist_name) == True):
            artist =  list(artist_name)
            for i in range(len(artist)):
                if(' ' == artist[i]):
                    artist[i] = '+'
            artist = "".join(artist)
            artist_site = get_url(artist)
            context['artist_name'] = artist_name.title()
            context['artist_site'] = artist_site
        else:
            artist_site = get_url(artist_name)
            context['artist_name'] = artist_name.title()
            context['artist_site'] = artist_site
        
        text = get_request_text(context['artist_site'])
        tour = on_tour(text)
        context['tour'] = tour.title()

        # Get the tour dates for the artists
        dates = []
        dates = get_dates(tour, dates, text)
        context['venue'] = dates
       
    return render(request, 'blog/index.html', context)