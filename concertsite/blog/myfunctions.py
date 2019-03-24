from bs4 import BeautifulSoup
from django.http import HttpResponse
import requests
import re

# Create your views here.

def month_to_num(month):
    return {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }[month]

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
    
    # Get the tour dates of the artists.
def get_tour_dates(artist_site_soup, new_dates):
    #tour_dates = artist_site_soup.find('div', class_ = 'event-row').get_text()
    tour_dates = []
    for dates in artist_site_soup.find_all('div', class_ = 'event-row'):
        tour_dates.append(dates)
    #tour_dates = tour_dates.split()
    if(len(tour_dates) == 1):
        print('{} concert near you. \n'.format(len(tour_dates)))
    else:
        print('{} concerts near you. \n'.format(len(tour_dates)))


    for i in range(0, len(tour_dates)):
        tour_dates[i] = tour_dates[i].get_text()
        #print(tour_dates[i].split())
        # Convert each tour date into a list
        tour_dates[i] = tour_dates[i].split()
        # Convert list to string for each tour date list
        date = " ".join(tour_dates[i])
        # Delete all the unnecessary info after the state
        #print(date)
        head, sep, tail= date.partition(', US')
        new_dates.append(head)
        #print(head + '\n')
    return new_dates

def get_dates(on_tour, dates, artist_site_soup):
    if('yes' in on_tour):
        dates = get_tour_dates(artist_site_soup, dates)
        if(len(dates) == 0):
                return 'No concerts near you.'
        else:
            venue = []
            for date in dates:
                # Get the city and state and check the tempature and the current condition
                location = date.split(', ')
                print(location)
                date_info = location[0].split(' ')
                month = month_to_num(date_info[2])
                day = date_info[1]
                year = date_info[3]
                time = [year, month, day]
                print('Venue: ' , ' '.join(date_info[4:len(date_info)]))
                venue.append(' '.join(date_info[4:len(date_info)]))
                print(date_info)
                print(time)
                city = location[len(location)-2]
                state = location[len(location)-1]
                place = city + ', ' + state + ', USA'
                print(place)
    return venue