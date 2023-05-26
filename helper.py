# its collecting data from the following sites:
# queroarrendar
# imovirtual
# uniplaces       it returns inicially 3 infos:
# olx             title, price and link
# custojusto

import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import pywhatkit
import mysql.connector

# connect to database
mydb = mysql.connector.connect(
    host='localhost',
    username='sqluser',
    password='1994508Zxc',
    database='aptlist'
)

# create cursor to interact with the DB
mycursor = mydb.cursor()

# calls current date to extraction control
current_date = time.strftime("%Y-%m-%d") 


# coleta infs da primeira pagina do site queroarrendar.com
def quero_arrendar(max_price, numero_whats):
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

        # join base url to partial url got from find('a', class_='col-xs..')['href']
        abs_url = urljoin(base_url, link)
        # format number so we can compare to user input
        final_price = int(price[:-2].replace('\xa0', ''))
        # transform final_price into string so it can be written on posts.txt
        f_price = str(final_price)
        # add to apt_options the information about each finding
        apt_option = f'{title}\n{f_price}\n{location}\n{abs_url}\n\n'

        #mycursor.execute(f"INSERT INTO aptoptions (title, price, data, link) VALUES('{title}', {f_price}, '{current_date}', '{abs_url}')")
        #mydb.commit()
        
        # check if the data exists in DB before saving it
        mycursor.execute("SELECT COUNT(*) FROM aptoptions WHERE title = %s AND price = %s", (title, f_price))
        result = mycursor.fetchone()
        count = result[0]
        if count == 0:
            # Insert the record into the database
            mycursor.execute("INSERT INTO aptoptions (title, price, data, link) VALUES(%s, %s, %s, %s)", (title, f_price, current_date, abs_url))
            mydb.commit()

        # add the options that has final price lower than max_price
        if final_price <= max_price:
            apt_options.append(apt_option)
    # write all the apartment options to a file
    with open('posts/posts-queroarrendar.txt', 'a') as f:
        f.writelines(apt_options)

    print("quero_arrendar 1ª parte [x]")


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
            


            # join base url to partial url got from find('a', class_ = 'col-xs..')['href']
            abs_url = urljoin(base_url, link)

            # format number so we can compare to user input
            final_price = int(price[:-2].replace('\xa0', ''))
            
            # transform final_price into string so it can be writen on posts.txt
            f_price = str(final_price)

            # check if the data exists in DB before saving it
            mycursor.execute("SELECT COUNT(*) FROM aptoptions WHERE title = %s AND price = %s", (title, f_price))
            result = mycursor.fetchone()
            count = result[0]
            if count == 0:
            # Insert the record into the database
                mycursor.execute("INSERT INTO aptoptions (title, price, data, link) VALUES(%s, %s, %s, %s)", (title, f_price, current_date, abs_url))
                mydb.commit()


            if final_price <= max_price:

                with open(f'posts/posts-queroarrendar-2.txt', 'a') as f:
                    
                    f.write(f'{title} \n')
                    f.write(f'{f_price} \n')
                    f.write(f'{location} \n')
                    f.write(f'{abs_url} \n')
                    f.write('\n')

    print("quero_arrendar 2ª parte [x]")

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


        # check if the data exists in DB before saving it
        mycursor.execute("SELECT COUNT(*) FROM aptoptions WHERE title = %s AND price = %s", (title, f_price))
        result = mycursor.fetchone()
        count = result[0]
        if count == 0:
            # Insert the record into the database
            mycursor.execute("INSERT INTO aptoptions (title, price, data, link) VALUES(%s, %s, %s, %s)", (title, f_price, current_date, link))
            mydb.commit()


        if f_price <= max_price:
            apt_options.append(apt_option)

    with open('posts/posts-imovirtual.txt', 'a') as f:
        f.writelines(apt_options)


    print("imovirtual 1ª parte [x]")
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


            # check if the data exists in DB before saving it
            mycursor.execute("SELECT COUNT(*) FROM aptoptions WHERE title = %s AND price = %s", (title, f_price))
            result = mycursor.fetchone()
            count = result[0]
            if count == 0:
                # Insert the record into the database
                mycursor.execute("INSERT INTO aptoptions (title, price, data, link) VALUES(%s, %s, %s, %s)", (title, f_price, current_date, link))
                mydb.commit()



            if f_price <= max_price:
                apt_options.append(apt_option)

        with open('posts/posts-imovirtual-2.txt', 'a') as f:
            f.writelines(apt_options)

    print("imovirtual 2ª parte [x]")


def uniplaces(max_price):
    html_text = requests.get('https://www.uniplaces.com/pt/accommodation/porto').text # ok

    soup = BeautifulSoup(html_text, 'lxml') # ok

    apts = soup.find_all('a', class_ ="sc-q9wvaw-0 goZTpP") # ok

    apt_options = []

    for index, apt in enumerate(apts):
        price = apt.find('span', class_ = 'rent__value').text                  # ok                                        # ok
        title = apt.find('h3', class_ = 'property__title').text
        location = ""
        link = apt['href']

        f_price = ""
        for i in price:
            if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                f_price += i
    
        f_price = int(f_price)

        apt_option = f'{title}\n{f_price}\n{location}\n{link}\n'

        # check if the data exists in DB before saving it
        mycursor.execute("SELECT COUNT(*) FROM aptoptions WHERE title = %s AND price = %s", (title, f_price))
        result = mycursor.fetchone()
        count = result[0]
        if count == 0:
            # Insert the record into the database
            mycursor.execute("INSERT INTO aptoptions (title, price, data, link) VALUES(%s, %s, %s, %s)", (title, f_price, current_date, link))
            mydb.commit()

    
        if f_price <= max_price:
            apt_options.append(apt_option)

    with open('posts/posts-uniplaces.txt', 'a') as f:
        f.writelines(apt_options)


    print('uniplaces 1ª parte [x]')
    

    ####
    ## FIM DA PRIMEIRA PARTE
    ####
    x = 2
    while x <= 24:
            html_text = requests.get(f'https://www.uniplaces.com/pt/accommodation/porto?page={x}').text # ok
            x+=1
    soup = BeautifulSoup(html_text, 'lxml') # ok

    apts = soup.find_all('a', class_ ="sc-q9wvaw-0 goZTpP") # ok

    apt_options = []

    for index, apt in enumerate(apts):
        price = apt.find('span', class_ = 'rent__value').text                  # ok                                        # ok
        title = apt.find('h3', class_ = 'property__title').text
        location = ""
        link = apt['href']

        f_price = ""
        for i in price:
            if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                f_price += i
    
        f_price = int(f_price)

        apt_option = f'{title}\n{f_price}\n{location}\n{link}\n'

        # check if the data exists in DB before saving it
        mycursor.execute("SELECT COUNT(*) FROM aptoptions WHERE title = %s AND price = %s", (title, f_price))
        result = mycursor.fetchone()
        count = result[0]
        if count == 0:
            # Insert the record into the database
            mycursor.execute("INSERT INTO aptoptions (title, price, data, link) VALUES(%s, %s, %s, %s)", (title, f_price, current_date, link))
            mydb.commit()

        
        if f_price <= max_price:
            apt_options.append(apt_option)

    with open('posts/posts-uniplaces-2.txt', 'a') as f:
        f.writelines(apt_options)

    print('uniplaces 2ª parte [x]')
    
def olx(max_price):

    html_text = requests.get('https://www.olx.pt/imoveis/apartamento-casa-a-venda/apartamentos-arrenda/porto/q-arrendamento/').text

    soup = BeautifulSoup(html_text, 'lxml')

    apts = soup.find_all('div', class_ ="css-1sw7q4x") # ok

    apt_options = []

    for index, apt in enumerate(apts):
        try:
            price = apt.find('p', class_ = 'css-10b0gli er34gjf0').text   
            title = apt.find('h6', class_ = 'css-16v5mdi er34gjf0').text
            location = ""
            link = apt.a['href']
        
            f_price = ""
            for i in price:
                if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    f_price += i
        
            f_price = int(f_price)
            apt_option = f'----\n{title}\n{f_price}\n{location}\n{link}\n'

            # check if the data exists in DB before saving it
            mycursor.execute("SELECT COUNT(*) FROM aptoptions WHERE title = %s AND price = %s", (title, f_price))
            result = mycursor.fetchone()
            count = result[0]
            if count == 0:
                # Insert the record into the database
                mycursor.execute("INSERT INTO aptoptions (title, price, data, link) VALUES(%s, %s, %s, %s)", (title, f_price, current_date, link))
                mydb.commit()



            if f_price <= max_price:
                apt_options.append(apt_option)

        except AttributeError:
            apt_option = 'None'

    with open('posts/posts-OXL.txt', 'a') as f:
        f.writelines(apt_options)

    print('OLX 1ª parte [x]')
    ## fim da primeira parte"""
    ##

    x = 2
    while x <= 7:

        html_text = requests.get(f'https://www.olx.pt/imoveis/apartamento-casa-a-venda/apartamentos-arrenda/porto/q-arrendamento/?page={x}').text
        x+=1

        soup = BeautifulSoup(html_text, 'lxml')

        apts = soup.find_all('div', class_ ="css-1sw7q4x") # ok

        apt_options = []

        for index, apt in enumerate(apts):
            try:
                price = apt.find('p', class_ = 'css-10b0gli er34gjf0').text   
                title = apt.find('h6', class_ = 'css-16v5mdi er34gjf0').text
                location = ""
                link = apt.a['href']
            
                f_price = ""
                for i in price:
                    if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                        f_price += i
            
                f_price = int(f_price)
                apt_option = f'----\n{title}\n{f_price}\n{location}\n{link}\n\n'


                # check if the data exists in DB before saving it
                mycursor.execute("SELECT COUNT(*) FROM aptoptions WHERE title = %s AND price = %s", (title, f_price))
                result = mycursor.fetchone()
                count = result[0]
                if count == 0:
                    # Insert the record into the database
                    mycursor.execute("INSERT INTO aptoptions (title, price, data, link) VALUES(%s, %s, %s, %s)", (title, f_price, current_date, link))
                    mydb.commit()




                if f_price <= max_price:
                    apt_options.append(apt_option)

            except AttributeError:
                apt_option = 'None'

        with open('posts/posts-OXL-2.txt', 'a') as f:
            f.writelines(apt_options)

    print('OLX 2ª parte [x]')


def custojusto(max_price):

    html_text = requests.get('https://www.custojusto.pt/porto/imobiliario/apartamentos/q/arrendamento?sp=1').text

    soup = BeautifulSoup(html_text, 'lxml')
    
    apts = soup.find_all('div', class_ = 'container_related')

    apt_options = []
    
    for apt in apts:
        try:
            price = apt.find('h5', class_ = 'col-md-2 col-sm-2 col-xs-6 no-padding text-right pull-right price_related').text
            title = apt.find('h2', class_ = 'no-padding no-margin col-md-10 col-sm-10 words li_subject title_related').text
            location = ""
            link = apt.a['href']
         
            f_price = ""
            for i in price:
                if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    f_price += i
            
            price = int(f_price)
            apt_option = f'{title}\n{f_price}\n{location}\n{link}\n'

            # check if the data exists in DB before saving it
            mycursor.execute("SELECT COUNT(*) FROM aptoptions WHERE title = %s AND price = %s", (title, f_price))
            result = mycursor.fetchone()
            count = result[0]
            if count == 0:
                # Insert the record into the database
                mycursor.execute("INSERT INTO aptoptions (title, price, data, link) VALUES(%s, %s, %s, %s)", (title, f_price, current_date, link))
                mydb.commit()


            if price <= max_price:
                apt_options.append(apt_option)
        except:
            pass

        with open('posts/posts-custo-justo.txt', 'a') as f:
            f.writelines(apt_options)

    print('custojusto 1ª parte [x]')

    # Alguma coisa errada na segunda parte do custojusto..
    # ta lendo apenas 1 opção
    x = 2
    while x <= 15:

        html_text = requests.get(f'https://www.custojusto.pt/porto/imobiliario/apartamentos/q/arrendamento?sp={x}').text
        x+=1

        soup = BeautifulSoup(html_text, 'lxml')
        
        apts = soup.find_all('div', class_ = 'container_related')

        apt_options = []
        
        for apt in apts:
            try:
                price = apt.find('h5', class_ = 'col-md-2 col-sm-2 col-xs-6 no-padding text-right pull-right price_related').text
                title = apt.find('h2', class_ = 'no-padding no-margin col-md-10 col-sm-10 words li_subject title_related').text
                location = ""
                link = apt.a['href']
            
                f_price = ""
                for i in price:
                    if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                        f_price += i
                
                price = int(f_price)
                apt_option = f'{title}\n{f_price}\n{location}\n{link}\n'


                # check if the data exists in DB before saving it
                mycursor.execute("SELECT COUNT(*) FROM aptoptions WHERE title = %s AND price = %s", (title, f_price))
                result = mycursor.fetchone()
                count = result[0]
                if count == 0:
                    # Insert the record into the database
                    mycursor.execute("INSERT INTO aptoptions (title, price, data, link) VALUES(%s, %s, %s, %s)", (title, f_price, current_date, link))
                    mydb.commit()


                if price <= max_price:
                    apt_options.append(apt_option)
            except:
                pass

            with open('posts/posts-custo-justo-2.txt', 'a') as f:
                f.writelines(apt_options)

    print('custojusto 2ª parte [x]')

    mysql.close()