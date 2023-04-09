# coleta as opções de arrendamnto de todas as paginas do site queroarrendar..
# Work on progress para coletar todas as opções do site imovirtual

import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import pywhatkit

# coleta infs da primeira pagina do site queroarrendar.com
def quero_arrendar(max_price, numero_whats):

    counter = 0
    # use get method from requests lib. it requests information from the website
    # # we are using '.txt' for requesting only text.
    text_html = requests.get('https://www.queroarrendar.com/imoveis/apartamentos/arrendamento/porto/').text
    # create a beautiful instance. 'html_text' is the object we want to scrap
    # lxml is the parse 'mode'
    soup = BeautifulSoup(text_html, 'lxml')
    # now we select via 'find()' method in html the element we want to
    # look apart which, in this case is 'xxx' tag 'zzzz' element
    apts = soup.find_all('a', class_='col-xs-12 col-md-12 col-lg-6 nopadding')
    # define base url for later join to partial url
    base_url = 'https://www.queroarrendar.com/'
    apt_options = []
    for index, apt in enumerate(apts):
        price = apt.find('p', class_='price').text
        location = apt.find('p', class_='location').text
        title = apt.find('h4', class_='title').text
        link = apt['href']
        

        counter +=1

        # join base url to partial url got from find('a', class_='col-xs..')['href']
        abs_url = urljoin(base_url, link)
        # format number so we can compare to user input
        final_price = int(price[:-2].replace('\xa0', ''))
        # transform final_price into string so it can be written on posts.txt
        f_price = str(final_price)
        # add to apt_options the information about each finding
        apt_option = f'{counter}. {title}\n{f_price}\n{location}\n{abs_url}\n\n'
        # add the options that has final price lower than max_price
        if final_price <= max_price:
            apt_options.append(apt_option)
    # write all the apartment options to a file
    with open('posts/posts-queroarrendar.txt', 'a') as f:
        f.writelines(apt_options)


    ## .....................
    ## FIM DA PRIMEIRA PARTE
    ## .....................
    
    
    x = 2
    while x < 14:

        text_html = requests.get(f'https://www.queroarrendar.com/imoveis/apartamentos/arrendamento/porto/?page={x}').text
        x+=1
        soup = BeautifulSoup(text_html, 'lxml')

        apts = soup.find_all('a', class_ = 'col-xs-12 col-md-12 col-lg-6 nopadding')

        # define base url for later join to partial url
        base_url = 'https://www.queroarrendar.com/'


        for index, apt in enumerate(apts):
            price = apt.find('p', class_ = 'price').text
            location = apt.find('p', class_ = 'location').text
            title = apt.find('h4', class_ = 'title').text
            link = soup.find('a', class_ = 'col-xs-12 col-md-12 col-lg-6 nopadding')['href']
            

            counter +=1

            # join base url to partial url got from find('a', class_ = 'col-xs..')['href']
            abs_url = urljoin(base_url, link)

            # format number so we can compare to user input
            final_price = int(price[:-2].replace('\xa0', ''))
            
            # transform final_price into string so it can be writen on posts.txt
            f_price = str(final_price)

            if final_price <= max_price:

                with open(f'posts/posts-queroarrendar-2.txt', 'a') as f:
                    
                    f.write(f'{counter}. {title} \n')
                    f.write(f'{f_price} \n')
                    f.write(f'{location} \n')
                    f.write(f'{abs_url} \n')
                    f.write('\n')

    print('done')

    # send the WhatsApp message with all the apartment options
    #if apt_options:
     #   message = '\n'.join(apt_options)
      #  pywhatkit.sendwhatmsg_instantly(numero_whats, message, 10, True, 3)

def imovirtual(max_price):
    text_html = requests.get('https://www.imovirtual.com/arrendar/apartamento/porto/?search%5Bregion_id%5D=13').text
    
    # create a beautiful instance. 'html_text' is the object we want to scrap
    # lxml is the parse 'mode'
    soup = BeautifulSoup(text_html, 'lxml')

    # now we select via 'find()' method in html the element we want to
    # look apart which, in this case is 'xxx' tag 'zzzz' element
    apts = soup.find_all('article', class_="offer-item")

    apt_options = []
    
    for apt in apts:
        price = apt.find('li', class_ = 'offer-item-price').text.replace(" ", "").strip('\n')
        location = ""
        title = apt.header.text.strip('\n').replace("\n", "/")
        link = apt.h3.a['href']
        
        f_price = ""
        for i in price:
            if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                f_price += i

        f_price = int(f_price)

        apt_option = f'{title}\n{f_price}\n{location}\n{link}\n'
        if f_price <= max_price:
            apt_options.append(apt_option)

    with open('posts/posts-imovirtual.txt', 'a') as f:
        f.writelines(apt_options)
    # send the WhatsApp message with all the apartment options
    #if apt_options:
     #   message = '\n'.join(apt_options)
      #  pywhatkit.sendwhatmsg_instantly(numero_whats, message, 10, True, 3)

    ## .....................
    ## FIM DA PRIMEIRA PARTE
    ## .....................
    
    x = 2
    while x < 21:
        
        text_html = requests.get(f'https://www.imovirtual.com/arrendar/apartamento/porto/?search%5Bregion_id%5D=13&page={x}').text
        x+=1
        # create a beautiful instance. 'html_text' is the object we want to scrap
        # lxml is the parse 'mode'
        soup = BeautifulSoup(text_html, 'lxml')

        # now we select via 'find()' method in html the element we want to
        # look apart which, in this case is 'xxx' tag 'zzzz' element
        apts = soup.find_all('article', class_="offer-item")

        apt_options = []
        
        for apt in apts:
            price = apt.find('li', class_ = 'offer-item-price').text.replace(" ", "").strip('\n')
            location = ""
            title = apt.header.text.strip('\n').replace("\n", "/")
            link = apt.h3.a['href']
            
            f_price = ""
            for i in price:
                if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    f_price += i

            f_price = int(f_price)

            apt_option = f'{title}\n{f_price}\n{location}\n{link}\n'
            if f_price <= max_price:
                apt_options.append(apt_option)

        with open('posts/posts-imovirtual-2.txt', 'a') as f:
            f.writelines(apt_options)


