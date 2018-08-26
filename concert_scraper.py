from bs4 import BeautifulSoup
import requests
import re

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

# Convert the list to a String and remove the unnecessary characters that carried over.
new_link = str(result)
new_link = new_link[2:-2]
    

