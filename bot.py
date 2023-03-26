import requests
from bs4 import BeautifulSoup
import time

def main():
    find_apts()

# define function that will be resposible for connecting with website via requests's get method,
# and its going to instanciate it using BeautifulSoup(text_html,'lxml')
def find_apts():
    # use get method from requests lib. it requests information from the website
    # # we are using '.txt' for requesting only text.
    
    text_html = requests.get('https://www.queroarrendar.com/imoveis/apartamentos/arrendamento/porto/').text
    
    # create a beautiful instance. 'html_text' is the object we want to scrap
    # lxml is th parse 'mode'
    soup = BeautifulSoup(text_html, 'lxml')

    # now we select via 'find()' method in html the element we want to
    # look apart which, in this case is 'xxx' tag 'zzzz' element
    apts = soup.find_all('a', class_ = 'col-xs-12 col-md-12 col-lg-6 nopadding')

    for apt in apts:
        price = apt.find('p', class_ = 'price').text

        final_price = int(price[:-2].replace('\xa0', ''))

        if final_price <= 800:
        
            location = apt.find('p', class_ = 'location').text
            title = apt.find('h4', class_ = 'title').text
            link = apt.find('div', class_ = 'list')

            print(title)
            print(price)
            print(location)
            print(link)
            print(" ")

        
        
        
        

if __name__ == '__main__':
    main()
