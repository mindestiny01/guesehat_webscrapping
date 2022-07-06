from bs4 import BeautifulSoup
from string import ascii_uppercase as UC
import re
import requests
import csv

##  Global Variable for Headers
# HEADERS = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

def get_content(base_url, headers):
    '''
    Find the HTML specific class in the specific URL prefix
    :param str base_url: the BASE_URL of the website
    :param dict headers: User Agent of the Website
    :return __medicine_requests: All the founded list with specific class
    '''
    # Looping A - Z 
    for letter in UC:
        # Initialize the page with specific prefic
        __first_layer = str(base_url + letter)
        
        # Requests the URL -> 200
        first_req = requests.get(__first_layer, headers = headers)
        
        # Initialize the BeautfiulSoup for parsing the Page Content
        test_soup_one = BeautifulSoup(first_req.content, 'html.parser')

        # Finding all founded list with specific class
        __medicine_requests = test_soup_one.find_all('li', {'class' : 'col-sm-4'})

        # Check if the Page have no requested list with specific class
        if len(__medicine_requests) == 0: continue

        #return the sorted page
        return __medicine_requests

def get_desc(__medicine_requests, headers):
    # List for recorded info
    medicine_temp = []

    # Looping through recorded link
    for scrap in __medicine_requests:
        link_temp = []
        # Finding the Link with a tag and append in to list
        medicine_link_info = scrap.find('a')['href']
        link_temp.append(medicine_link_info)

        # Looping through recorded link
        for link in link_temp:
            
            #Requests and get the content from requested link
            specific_req = requests.get(str(link), headers = headers)
            specific_soup = BeautifulSoup(specific_req.content, 'html.parser')

            # Finding the Medicine Name
            __med_name = specific_soup.find('h1', {'class' : 'disdetail-head-title'})

            # Check if there is empty tag, otherwise convert it to list
            if __med_name is None: continue
            else : __med_name = [specific_soup.find('h1', {'class' : 'disdetail-head-title'}).text]

            # Finding the description of medicine, only first paragraph
            __desc = specific_soup.find('div', {'class' : 'obat-group-head clearfix'})

            # Check if there is empty tag, otherwise replace 'Penggunaan' with empty string and convert it to list
            if __desc is None: continue
            else: __desc_fix = [__desc.text.replace('Penggunaan', '')]
        
            # Zip the Fixed Medicine Name and Description
            get_zip = zip(__med_name, __desc_fix)

            # Append the all recorded information to a list
            for name, desc in get_zip: medicine_temp.append([name, desc]); break

    column_name = ['Name of Medicine', 'Medicine Description']
    file_name = csv.writer(open('data/medicine_link.csv', 'w', newline = ''))
    file_name.writerow(column_name)
    for dt in medicine_temp: file_name.writerow(dt)
    print('Ready to Use')

if __name__ == '__main__':
    base_url = 'https://www.guesehat.com/info-obat?prefix='
    headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    __medicine_scrap = get_content(base_url, headers)
    get_the_desc = get_desc(__medicine_scrap, headers)
    get_the_desc
    