from bs4 import BeautifulSoup
import requests
import re
import pyowm

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
        head, sep, tail= date.partition(', US')
        new_dates.append(head)
        #print(head + '\n')
    return new_dates



################################################## MAIN PROGRAM #########################################################

# URL used to find where the artist or band will be playing.
songkick_site = 'https://www.songkick.com/search?utf8=✓&type=initial&query='

# Ask the user to input the artist or band.
artist_name = input('Please enter the name of the artist. \n')
artist = checkSpace(artist_name)

songkick_site = songkick_site + artist
songkick_site_object = requests.get(songkick_site)
songkick_site_text = songkick_site_object.text

songkick_site_soup = BeautifulSoup(songkick_site_text, 'html.parser')
#print(songkick_site_soup)

# Find the artist id from the HTML tag: <input type="hidden" name="subject_id" value="some number">
artist_id = songkick_site_soup.find('input', {'name': 'subject_id'})['value']
print("Artist ID: " , artist_id)

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
new_link = str(result)
new_link = new_link[2:-2]
#print(new_link)

artist_site = songkick_site[:24] + new_link
print(artist_site)

# Get request from the artist site and parse it
artist_site_object = requests.get(artist_site)
artist_site_text = artist_site_object.text
artist_site_soup = BeautifulSoup(artist_site_text, 'html.parser')

# Check if the artist is on tour so we can get more info
on_tour = artist_site_soup.find('li', class_ = 'ontour').get_text()
print(on_tour)

if('yes' in on_tour):
    dates = []
    get_tour_dates(artist_site_soup, dates)
    for date in dates:
        print(date)

    # Get the city and state and check the tempature and the current condition
    location = dates[0].split(', ')
    print(location)
    
    city = location[len(location)-2]
    state = location[len(location)-1]
    place = city + ', ' + state + ', USA'
    print(place)
    
    # API key for OWM
    owm = pyowm.OWM('21b71550850fc524c2e46097ba41d774')
    observation = owm.weather_at_coords(37.3382082,-121.88632860000001)
    w = observation.get_weather()
    print(w)
    
    temperature = w.get_temperature('fahrenheit')['temp']
    print(temperature)
    print(w.get_detailed_status())
    
else:
    print('{} is not on tour.'.format(artist_name))
    exit