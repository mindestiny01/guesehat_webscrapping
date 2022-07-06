from bs4 import BeautifulSoup
import requests
import pandas as pd

medicine_list = []

def get_content():

    base_url = 'https://www.alomedika.com/obat'
    headers = {'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

    req = requests.get(base_url, headers = headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    _medicine_list = soup.find_all('li', {'class':'page_item index-item'})
    for medicine in _medicine_list:
        
        # Store in Dictionary
        question = {
            'Name' : medicine.find('a', {'class':'title-az-results'}).text,
            'Link' : str('https://www.alomedika.com' + medicine.find('a', {'class':'title-az-results'})['href'])
        }

        medicine_list.append(question)
    return    


if __name__ == '__main__':

    get_content()
    df = pd.DataFrame(medicine_list)
    df.to_csv('data/medicine_info_2.csv')
    print('Ready to Use')
