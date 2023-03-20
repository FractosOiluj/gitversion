import requests
from bs4 import BeautifulSoup
import time


# ask me about the max value im willing to pay for renting a apt
valorMaximo = input("how much is enough for paying for renting a apt: \n")
print("Give me a number so i can send you the options")
numero_whats = input("digite o numero no formato: +000.00.0000000. >")
print("wait for the bot to search and gather the information")



def find_apts():
    # use get method from requests lib. it requests information from the website
    # # we are using '.txt' for requesting only text.
    text_html = requests.get(f'https://www.queroarrendar.com/imoveis/apartamentos/arrendamento/portugal/?pricemin=0&pricemax={valorMaximo}').text

    # create a beautiful instance. 'html_text' is the object we want to scrap
    # lxml is th parse 'mode'
    soup = BeautifulSoup(text_html, 'lxml')

    # now we select via 'find()' method in html the element we want to
    # look apart which, in this case is 'xxx' tag 'zzzz' element
    apts = soup.find_all('item')

    print(apts)    

find_apts()  
