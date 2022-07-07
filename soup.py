from bs4 import BeautifulSoup
import requests
import pandas as pd

HEADERS = {'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
medicine_list = []

def get_content():

    base_url = 'https://www.guesehat.com/info-obat?prefix=a'
    headers = {'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

    main_req = requests.get(base_url, headers = headers)

    main_soup = BeautifulSoup(main_req.content, 'html.parser')

    __medicine_tag_req = main_soup.find_all('li', {'class' : 'col-sm-4'})

    if len(__medicine_tag_req) == 0: pass

    for med_tag in __medicine_tag_req:

            temp_med = []

            medicine_link_info = med_tag.find('a')['href']

            temp_med.append(medicine_link_info)
                
            for link in temp_med:

                    pref_url = requests.get(str(link), headers = HEADERS)
                    soup = BeautifulSoup(pref_url.content, 'html.parser')

                    name_desc = soup.find('h1', {'class': 'disdetail-head-title'})

                    if name_desc is None: continue 
                    else : name = name_desc.text

                    _medicine_list = soup.find_all('div', {'class':'obat-group-head clearfix'})
                    if _medicine_list is None: continue
                    else: 
                        _overview = _medicine_list[0].text
                        _how_work = _medicine_list[1].text
                        _side_effects = _medicine_list[2].text
                        _how_use = _medicine_list[3].text
                        _dose = _medicine_list[4].text

                    question = {
                        'Name' : name,
                        'Overview': _overview,
                        'Works' : _how_work,
                        'Effect': _side_effects,
                        'Use' : _how_use,
                        'Dose': _dose
                    }

                    medicine_list.append(question); break   

if __name__ == '__main__':

    get_content()
    df = pd.DataFrame(medicine_list)
    df.to_csv('data/prefix_a.csv')
    print('Ready to Use')
