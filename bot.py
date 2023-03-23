import requests
from bs4 import BeautifulSoup
import time

# define function that will be resposible for connecting with website via requests's get method,
# and its going to instanciate it using BeautifulSoup(text_html,'lxml')

def find_apts():
    # use get method from requests lib. it requests information from the website
    # # we are using '.txt' for requesting only text.
    x = 1 
    while x <= 11:
        text_html = requests.get(f'https://www.queroarrendar.com/imoveis/apartamentos/arrendamento/porto/?page={x}').text
        x+=1
        
        # create a beautiful instance. 'html_text' is the object we want to scrap
        # lxml is th parse 'mode'
        soup = BeautifulSoup(text_html, 'lxml')

        # now we select via 'find()' method in html the element we want to
        # look apart which, in this case is 'xxx' tag 'zzzz' element
        apts_price = soup.find_all('p', class_ = 'price')
        apts_location = soup.find_all('p', class_ = 'location')
        

        for apt in apts_price:
            print(apt.text)

        for apt in apts_location:
            print(apt.text)
find_apts() 
