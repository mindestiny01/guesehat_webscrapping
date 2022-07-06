from string import ascii_lowercase as UC
from bs4 import BeautifulSoup
import requests
import pandas as pd
# import csv

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

                        # Get the Medicine Name
                        __med_name = pref_soup.find('h1', {'class' : 'disdetail-head-title'})

                        # Check if the page is not visible for name, 
                        # otherwise get the medicine name and casting to a list
                        if __med_name is None: continue
                        else : __med_name = [pref_soup.find('h1', {'class' : 'disdetail-head-title'}).text]

                        # Get the first paragraph of medicine description
                        __desc = pref_soup.find('div', {'class' : 'obat-group-head clearfix'})

                        # Check if the page is not visible for description, 
                        # otherwise replace specific word with empty string,
                        # and casting to a list 
                        if __desc is None: continue
                        else: __desc_fix = [__desc.text.replace('Penggunaan', '')]
                        
                        # This for making the name and Description are side-by-side inside the list
                        # And append all of it in to the list
                        get_zip = zip(__med_name, __desc_fix)
                        for name, desc in get_zip: 
                                Medicine_Full = {
                                        'Medicine Name' : name,
                                        'Description' : desc
                                }
                                medicine_list.append(Medicine_Full); break

## Another option to create csv file
df = pd.DataFrame(medicine_list)
df.to_csv('data/medicine_info_2.csv')
print('Ready to Use')




