# colect infomation about appartment rent options in 2 site.
# it import two functions from helper.py
# still much to be done. 

from helper import quero_arrendar, imovirtual, uniplaces
import time

def main():
    max_price = int(input("How much you can afford to pay?\n"))
    numero_whats = input('digite no formato: +000.00.0000000. >')
    cnt = 0
    try:
        quero_arrendar(max_price, numero_whats)
        imovirtual(max_price)
        uniplaces(max_price)
    except ValueError:
        print(f"value error nº:{cnt}")
        cnt+=1


if __name__ == '__main__':
    while True:
        main()
        time_wait = 2
        print(f'waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
    