'''
Find a 'scrappable' cryptocurrencies website where you can scrape the top 5 cryptocurrencies and display as a formatted output one currency at a time. 
The output should display the name of the currency, the symbol (if applicable), the current price and % change in the last 24 hrs and corresponding price (based on % change)

Furthermore, for Bitcoin and Ethereum, the program should alert you via text if the value falls below $40,000 for BTC and $3,000 for ETH.
'''

from twilio.rest import Client 
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

#Twilio info 
accountSID = 'ACb428a9d3d45309c1ba5d519bcba9af26'

authToken = '09bf54dfbaaa5b2ab63679cfb10e9e49'

client = Client(accountSID, authToken)

TwilioNumber = '+15407327783'

mycellphone = '+14083182538'

url = 'https://www.coinbase.com/price'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

req = Request(url, headers = headers)

webpage = urlopen(req).read()

soup = BeautifulSoup(webpage, 'html.parser')	

title = soup.title 

print(title.text)

crypto_table = soup.find('tbody')
crypto_rows = crypto_table.findAll('tr')

for x in range(1, 6):
    td = crypto_rows[x].findAll('td')

    #name of the currency
    curr_name = td[1].text

    #the current price
    curr_price = float(td[2].text)

    #% change in the last 24 hrs
    per_change = td[4].text.replace('+','')
    per_change = float(per_change.text.replace('%',''))

    # corresponding price (based on % change) calculation
    if per_change >= 0:
        per_change = per_change/100
        prev_price = round(curr_price - (curr_price * per_change), 2)
    else:
        per_change = per_change/100
        prev_price = round(curr_price + (curr_price * per_change), 2)

    per_change= format(per_change,'.2%')

    if curr_name == 'Bitcoin':
        if curr_price < 40000:
            textmessage = client.messages.create( 
                            to= mycellphone, 
                            from_= TwilioNumber, 
                            body = "The value of BTC fell below $40,000")
    
    if curr_name == 'Ethereum':
        if curr_price < 3000:
            textmessage = client.messages.create(
                            to= mycellphone, 
                            from_= TwilioNumber, 
                            body = "The value of ETH fell below $3,000")  

    print(f'Currency Name: {curr_name}')     
    print(f'Current Price: ${curr_price}')
    print(f'Percentage Change (24 HR): {per_change}')
    print(f'Corresponding/Previous Price: ${prev_price}')
    input()