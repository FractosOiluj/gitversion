# coleta titulo, valor e link de opções de arrendamento de todas as paginas
# do site 'queroarrendar

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

max_price = int(input("max value you want to pay, in the following format: ex. 600: \n"))

def main():
    other_pages(max_price)


def other_pages(max_price):
    x = 2
    counter = 0
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

                with open(f'posts/posts.txt', 'a') as f:
                    f.write(f'{counter}. {title} \n')
                    f.write(f'{f_price} \n')
                    f.write(f'{location} \n')
                    f.write(f'{abs_url} \n')
                    f.write('\n')

    print('done')
    print(counter)
main()