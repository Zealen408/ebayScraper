import requests
import time
from csv import writer
from bs4 import BeautifulSoup

def readyURL(pageNum, searchTerm, searchParam = 1):
    pageNum += 1
    urlAction = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={searchTerm}&_sacat=0&rt=nc&LH_Auction=1&_ipg=100&_pgn={pageNum}' 
    urlBuyItNow = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={searchTerm}&_sacat=0&rt=nc&LH_BIN=1&_ipg=100&_pgn={pageNum}'
    if searchParam == 1:
        url = urlAction
    else:
        url = urlBuyItNow
    return url

def returnSoup(url):
    page = requests.get(url)
    if page.status_code == 200:
        return BeautifulSoup(page.content, 'html.parser')
    return None

def prepData(item):
    row_content = []
    dollars = item.find('span', class_='s-item__price').get_text()
    # print(dollars)
    if dollars:
        dollarsToFloat = float(dollars.strip('$'))
        if dollarsToFloat <= 10.00:
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
        return row_content
    else:
        return None


def main():
    itemData = []
    searchTerm = f'{input("Search Term: ") or "knife"}'
    searchParam = f'{int(input("Enter 2 for Buy Now search") or 1)}'

    for loop in range(2):

        url = readyURL(loop, searchTerm, searchParam)
        
        soup = returnSoup(url)

        if soup != None:

            items = soup.find_all('div', class_='s-item__wrapper clearfix')
            # print(len(items))
            
            for item in items:
                # print(item)
            
                try:
            
                    row_content = prepData(item)
                    if len(row_content) > 0:
                        itemData.append(row_content)
            
                except Exception as e:
            
                    print(f'Error item find: {e}')
        
        else:
            break

    
    return itemData



def saveData(row_content):
    with open("myData.csv",'a', newline='\n') as writeObj:
        csv_writer = writer(writeObj)
        for row in row_content:
            csv_writer.writerow(row)



data = main()
saveData(data)
