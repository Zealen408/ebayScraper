from csv import writer, reader
from bs4 import BeautifulSoup
from itemClass import ItemData
from security import safe_requests

class EbayScrap:

    def __init__(self, searchTerm: str, maxPrice: float):
        self.searchTerm = searchTerm.replace(" ", "+").lower()
        self.maxPrice = maxPrice
        self.url = None

    def setNewSearch(self, newTerm):
        self.searchTerm = newTerm

    def setAuction(self):
        self.url= f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={self.searchTerm}&_sacat=0&rt=nc&LH_Auction=1&_ipg=100&_pgn='

    def setBuyItNow(self):
        self.url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={self.searchTerm}&_sacat=0&rt=nc&LH_BIN=1&_ipg=100&_pgn=' 

    def getPage(self, pageNum:int):
        return safe_requests.get(self.url + str(pageNum))

    def getData(self, page):
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            items = soup.find_all('div', class_='s-item__wrapper clearfix')
            contentData = []
            for item in items:
                try:
                    dollars = item.find('span', class_='s-item__price').get_text()
                    dollarsToFloat = float(dollars.strip('$'))
                except Exception as e:
                    print(e)
                    continue
                if dollars:
                    if dollarsToFloat <= self.maxPrice:
                        title = item.find('h3', class_ = "s-item__title").get_text()
                        link = item.find('a', class_ = "s-item__link")['href']
                        contentData.append(ItemData(title=title, price=dollarsToFloat, link=link))
            return contentData

    def saveData(self, records: list):
        with open("myData.csv",'a', newline='\n') as f:
            f.truncate()
            csv_writer = writer(f)
            for record in records:
                row = [record.title, record.price, record.link, record.shipping, record.bid_count]
                csv_writer.writerow(row)
        

    def retrieveData(self, file):
        data = []
        with open(file, 'r+', newline='\n') as f:
            items = list(reader(f))
            for item in items:
                _ = ItemData(title=item[0], price=item[1], link=item[2], shipping=item[3], bid_count=item[4])
                data.append(_)
        return data

    def digDeeper(self, items: list):
        for item in items:
            if item.shipping == 0.00 or item.bid_count == 0:
                url = item.link
                itemPage = safe_requests.get(url)
                if itemPage.status_code == 200:
                    soup = BeautifulSoup(itemPage.content)
                    
                    try:
                        item.bid_count = int(soup.find('span', {'id': 'qty-test'}).get_text())
                    except Exception:
                        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                        print(f'Bid Count: {Exception}')

                    try:
                        item.shipping = float(str(soup.find('span', {'id': 'fshippingCost'}).get_text()).strip('$'))
                    except Exception:
                        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                        print(f'Shipping: {Exception}')
                    
                    for ind, x in enumerate(items):
                        if x.link == item.link:
                            items[ind] = item
                            break
        return items

