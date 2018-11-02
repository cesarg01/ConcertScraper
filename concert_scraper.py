from bs4 import BeautifulSoup
import requests
import re
import pyowm
import googlemaps
from datetime import datetime

# Check to see if the name provided by the user has a space so we can modify the string to add '+' instead of the space 
# character since that is what is done in the URL.
def checkSpace(artist_name):
    if((' ' in artist_name) == True):
        artist =  list(artist_name)
        for i in range(len(artist)):
            if(' ' == artist[i]):
                artist[i] = '+'
        artist = "".join(artist)
        return artist
    else:
        return artist_name

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

# Get the geolocation of the place where the concert is taking place and return the temperature
def get_loc_temp(place, time):
    gmaps = googlemaps.Client(key='AIzaSyBeDHc2IX4OFFAUnwMuNG93fJbd52_K274')
    geocode_result = gmaps.geocode(place)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    #test - print results
    #print (lat,lon)
    # API key for OWM
    owm = pyowm.OWM('21b71550850fc524c2e46097ba41d774')
    observation = owm.weather_at_coords(lat,lon)
    w = observation.get_weather()
    #print(w)
    
    temperature = w.get_temperature('fahrenheit')['temp']
    #print(temperature)
    print(w.get_detailed_status())
    fc = owm.daily_forecast(place, limit = 1)
    f = fc.get_forecast()
    #print(f)
    rain = fc.will_have_rain()
    snow = fc.will_have_snow()
    fog = fc.will_have_fog()

    info = [temperature,  rain, snow, fog]
    
    return info

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


        
################################################## MAIN PROGRAM #########################################################

# URL used to find where the artist or band will be playing.
songkick_site = 'https://www.songkick.com/search?utf8=✓&type=initial&query='

# Ask the user to input the artist or band.
artist_name = input('Please enter the name of the artist. \n')
artist = checkSpace(artist_name)

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
print(new_link)
#new_link = new_link[2:-2]
#print(new_link)

artist_site = songkick_site[:24] + new_link
if(artist_site == songkick_site[:24]):
    alternative_link = '/artists/' + artist_id + '-' + artist
    print('Artist your looking for not on website. Please try again by removing words like "the".')
    answer = input('Do you want to check if {} is the correct artist link you are looling for? If so please type yes, y, no, or n. \n'.format(alternative_link))
    answer = answer.lower()
    if(answer == 'yes' or answer == 'y'):
        artist_site = songkick_site[:24] + alternative_link
    else:
        print('Artist your looking for not on website. Please try again by removing words like "the".')
        exit()
else:
    print(artist_site)


# Get request from the artist site and parse it
artist_site_object = requests.get(artist_site)
artist_site_text = artist_site_object.text
artist_site_soup = BeautifulSoup(artist_site_text, 'html.parser')

# Check if the artist is on tour so we can get more info
while True:
    try:
        on_tour = artist_site_soup.find('li', class_ = 'ontour').get_text()
        print(on_tour)
        break
    except AttributeError:
        print('Site has no information for {}'.format(artist_name))
        exit()


# Check if the artist is on tour. If so get the tour dates.
if('yes' in on_tour):
    dates = []
    dates = get_tour_dates(artist_site_soup, dates)
    if(len(dates) == 0):
            exit()
    else:
        for date in dates:
            print(date)

            # Get the city and state and check the tempature and the current condition
            location = date.split(', ')
            #print(location)
            date_info = location[0].split(' ')
            month = month_to_num(date_info[2])
            day = date_info[1]
            year = date_info[3]
            time = [year, month, day]
            #print(month)
        
            city = location[len(location)-2]
            state = location[len(location)-1]
            place = city + ', ' + state + ', USA'
            #print(place)

            temp = get_loc_temp(place, time)
            print('The current temperature is {}'.format(temp[0]))
            if(temp[1] == True):
                print('Rain today.')
            if(temp[2] == True):
                print('Snow today.')
            if(temp[3] == True):
                print('Fog today.')
            
            print('For weather during the concert please check the day of the concert.')
    
else:
    print('{} is not on tour.'.format(artist_name))
    exit()