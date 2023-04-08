# coleta todas as opções de arrendamnto da primira pagina do site queroarrendar

import requests
from bs4 import BeautifulSoup
import time
import pywhatkit

from urllib.parse import urljoin

# define a max value of rent for th program to send me msg'
max_price = int(input("How much you can afford to pay?\n"))
numero_whats = input('digite no formato: +000.00.0000000. >')


def main():
    find_apts(max_price)

# define function that will be resposible for connecting with website via requests's get method,
# and its going to instanciate it using BeautifulSoup(text_html,'lxml')
def find_apts(n):
    
    # use get method from requests lib. it requests information from the website
    # # we are using '.txt' for requesting only text.
    text_html = requests.get('https://www.queroarrendar.com/imoveis/apartamentos/arrendamento/porto/').text
    
    # create a beautiful instance. 'html_text' is the object we want to scrap
    
    # lxml is th parse 'mode'
    soup = BeautifulSoup(text_html, 'lxml')

    # now we select via 'find()' method in html the element we want to
    # look apart which, in this case is 'xxx' tag 'zzzz' element
    apts = soup.find_all('a', class_ = 'col-xs-12 col-md-12 col-lg-6 nopadding')

    # define base url for later join to partial url
    base_url = 'https://www.queroarrendar.com/'

    for index, apt in enumerate(apts):
        price = apt.find('p', class_ = 'price').text
        location = apt.find('p', class_ = 'location').text
        title = apt.find('h4', class_ = 'title').text
        link = soup.find('a', class_ = 'col-xs-12 col-md-12 col-lg-6 nopadding')['href']

        # join base url to partial url got from find('a', class_ = 'col-xs..')['href']
        abs_url = urljoin(base_url, link)

        # format number so we can compare to user input
        final_price = int(price[:-2].replace('\xa0', ''))
        
        # transform final_price into string so it can be writen on posts.txt
        f_price = str(final_price)

        with open(f'posts/posts.txt', 'a') as f:
            f.write(f'{index}. {title} \n')
            f.write(f'{f_price} \n')
            f.write(f'{location} \n')
            f.write(f'{abs_url} \n')
            f.write('\n')



        # add whatsapp msg here
    print(f'apt option saved: {index}') 
    
if __name__ == '__main__':
    while True:
        find_apts(max_price)
        time_wait = 2
        print(f"wait few seconds")
        # define a delay so the program will wait for as long as we define (time.sleep) accept time in seconds
        time.sleep(time_wait * 6) #600sec = 10min
