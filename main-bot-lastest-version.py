# colect infomation about appartment rent options in 2 site.
# it import two functions from helper.py
# still much to be done. 

from helper import quero_arrendar, imovirtual
import time

def main():
    max_price = int(input("How much you can afford to pay?\n"))
    numero_whats = input('digite no formato: +000.00.0000000. >')
    quero_arrendar(max_price, numero_whats)
    imovirtual(max_price)
    


if __name__ == '__main__':
    while True:
        main()
        time_wait = 2
        print(f'waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
    