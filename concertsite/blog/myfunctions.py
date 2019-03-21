from bs4 import BeautifulSoup
from django.http import HttpResponse
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
            #print('Site has no artist ID for {}'.format(artist_name))
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
    artist_site = songkick_site[:24] + new_link
    return (artist_site)
    #new_link = new_link[2:-2]
    #print(new_link)

def get_request_text(artist_site):
    # Get request from the artist site and parse it
    artist_site_object = requests.get(artist_site)
    artist_site_text = artist_site_object.text
    artist_site_soup = BeautifulSoup(artist_site_text, 'html.parser')
        
    return artist_site_soup

def on_tour(artist_site_soup):
    # Check if the artist is on tour so we can get more info
    on_tour = ''
    while True:
        try:
            on_tour = artist_site_soup.find('li', class_ = 'ontour').get_text()
            break
        except AttributeError:
            #print('Site has no information for {}'.format(artist_name))
            on_tour = 'Site has no information.'
    return on_tour