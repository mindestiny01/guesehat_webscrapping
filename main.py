from string import ascii_lowercase as UC
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Global Variable of Google Chrome
HEADERS = {'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

# List of all recorded information
medicine_list = []

# Looping through all upppercase letter
for letter in UC:

        # Declare the url alongside the prefix
        base_url = f'https://www.guesehat.com/info-obat?prefix={letter}'

        # Initialize the requests
        main_req = requests.get(base_url, headers = HEADERS)

        # Initialize the BeautifulSoup class
        main_soup = BeautifulSoup(main_req.content, 'html.parser')

        # Finding all list with specified class
        __medicine_tag_req = main_soup.find_all('li', {'class' : 'col-sm-4'})

        # if there is no list with specified class, so continue
        if len(__medicine_tag_req) == 0: continue

        # Looping through founded list with specified class
        for med_tag in __medicine_tag_req:

                # List for recorded link
                temp_med = []

                # Finding all link in the page
                medicine_link_info = med_tag.find('a')['href']

                # Append the link in to list
                temp_med.append(medicine_link_info)
                
                # Looping through all recorded link in list
                for link in temp_med:

                        # Make requests and parsing with BeautifulSoup
                        pref_url = requests.get(str(link), headers = HEADERS)
                        pref_soup = BeautifulSoup(pref_url.content, 'html.parser')

                        # Get the HTML tag of Medicine Name 
                        __med_name = pref_soup.find('h1', {'class' : 'disdetail-head-title'})

                        # Check if the page is not visible for name, 
                        # otherwise get the medicine name as a plain text
                        if __med_name is None: continue
                        else : name  = __med_name.text 

                        # Get the all <div> tag of paragraph
                        __medicine_desc_list = pref_soup.find_all('div', {'class' : 'obat-group-head clearfix'})

                        # Check if the page is not visible for description, 
                        # otherwise take every related paragraph to the new variable
                        if __medicine_desc_list is None: continue
                        else:
                                __overview = __medicine_desc_list[0].text
                                __how_works = __medicine_desc_list[1].text
                                __side_effects = __medicine_desc_list[2].text
                                __how_use = __medicine_desc_list[3].text
                                __dose = __medicine_desc_list[4].text
                        
                        # And append all of it in to the list
                        Medicine_Full = {
                                'Name' : name,
                                'Overview' : __overview,
                                'Works' : __how_works,
                                'Effects' : __side_effects,
                                'Use' : __how_use,
                                'Dose': __dose
                        }
                        medicine_list.append(Medicine_Full); break

## Create csv file
df = pd.DataFrame(medicine_list)
df.to_csv('data/indonesian_medicine_dataset.csv')
print('Ready to Use')




