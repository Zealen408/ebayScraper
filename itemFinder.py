import requests
import time
from csv import writer
from bs4 import BeautifulSoup

def search(searchTerm = 'knife', searchParam = 1):
    pages = []
    for loop in range(5):
        # EBAY PAGE
        urlAction = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={searchTerm}&_sacat=0&rt=nc&LH_Auction=1&_ipg=100&_pgn={loop+1}' 
        urlBuyItNow = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={searchTerm}&_sacat=0&rt=nc&LH_BIN=1&_ipg=100&_pgn={loop+1}'
        if searchParam == 1:
            url = urlAction
        else:
            url = urlBuyItNow
        try:
            print(str(url))
            page = requests.get(url)
            time.sleep(2)
            print(page.status_code)
            soup = BeautifulSoup(page.text, 'html.parser')

            items = soup.find_all('div', class_='s-item__wrapper clearfix')
            print(len(items))
            for item in items:
                # print(item)
                try:
                    dollars = item.find('span', class_='s-item__price').get_text()
                    # print(dollars)
                    dollarsToFloat = float(dollars.strip('$'))
                    if dollarsToFloat <= 5.00:
                        title = item.find('h3', class_ = "s-item__title").get_text()
                        link = item.find('a', class_ = "s-item__link")['href']
                        # shipping = item.find('span', class_="s-item__shipping")
                        # costShipping = float(shipping.strip('+$ shipping'))
                        # costWithShipping = dollarsToFloat + costShipping
                        
                        row_content = [
                            title,
                            dollars,
                            # costWithShipping,
                            link
                        ]

                        getItemData(row_content)
                except Exception as e:
                    print(f'Error Layer 1: {e}')
        except Exception:
            for data in Exception:
                print(f'Error layer 2: {data}')   
    return pages



def getItemData(item):
    with open("myData.csv",'a', newline='\n') as writeObj:
        csv_writer = writer(writeObj)
        csv_writer.writerow(item)



pages = search()

