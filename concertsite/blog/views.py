from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
import re

# Create your views here.

def get_url(artist):
    songkick_site = 'https://www.songkick.com/search?utf8=✓&type=initial&query='
    songkick_site = songkick_site + artist
    #print(songkick_site)
    songkick_site_object = requests.get(songkick_site)
    songkick_site_text = songkick_site_object.text

    songkick_site_soup = BeautifulSoup(songkick_site_text, 'html.parser')
    #print(songkick_site_soup)

    # Find the artist id from the HTML tag: <input type="hidden" name="subject_id" value="some number">
    while True:
        try:
            artist_id = songkick_site_soup.find('input', {'name': 'subject_id'})['value']
            print("Artist ID: " , artist_id)
            break
        except AttributeError:
            print('Site has no artist ID for {}'.format(artist_name))
            exit()

    # Find the link to the artist's site on songkick.
    link_found = []
    p = songkick_site_soup.find('p', class_ = 'summary')

    # Convert element to a String and convert it to a list.
    p = str(p)
    link_found = p.split()

    # Convert the element to a string.
    link = str(link_found[3])

    # Search the link between quotation marks.
    result = re.findall('"(.*?)"', link)

    # Convert the list to a String and remove the unnecessary characters that carried over. (ex. [' '])
    new_link = ''.join(result) #str(result)
    return (new_link)
    #new_link = new_link[2:-2]
    #print(new_link)


def index_page(request):
    # The function render will render (put together) our template blog/index_page.html
    context = {}
    if(request.method == 'POST'):
        artist_name = request.POST.get('artist')
        if((' ' in artist_name) == True):
            artist =  list(artist_name)
            for i in range(len(artist)):
                if(' ' == artist[i]):
                    artist[i] = '+'
            artist = "".join(artist)
            artist_site = get_url(artist)
            context['artist_name'] = artist.title()
            context['artist_site'] = artist_site
        else:
            artist_site = get_url(artist_name)
            context['artist_name'] = artist_name.title()
            context['artist_site'] = artist_site
    return render(request, 'blog/index.html', context)