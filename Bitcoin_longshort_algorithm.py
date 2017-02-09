import requests
import datetime
import time
#import numpy
import csv


#----------------------Bitcoin Price functions using Coindesk price API-----------------------

data = {}

with open('bpx.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ' )

    dates = []
    prices = []

    for row in reader:
        price = row[:2]
        prices.append(price)

    testelement = prices[2]

    len = len(prices) - 3
#    print(len)
#    print(testelement)



def btcnow():
    btcnow = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')

    endtxt = '"'

    btcnow = btcnow.text

    btcnowstart = btcnow.find('"rate":') + 8
    btcnowend = btcnow.find(endtxt, btcnowstart)
    btcnowtext = btcnow[btcnowstart:btcnowend]

    if  btcnowtext.find('}') == 1:
        btcnowtext = btcnowtext.replace('}', '')

    return (btcnowtext)

def btcpricing (date1, date2):

    btc= requests.get('https://api.coindesk.com/v1/bpi/historical/close.json?start='+date1+'&end='+date2)
    #print(btc.text  )

    char1 = "{"
    char2 = ","
    btc=btc.text
    btctext = btc[btc.find(char1)+21:btc.find(char2)]

    if  btctext.find('}'):
        btctext = btctext.replace('}', '')

    #print(btctext)
    return(btctext)

def btcpricingdatabase(len, date1txt, prices):
    for n in range(2, len):
        pricetxt = str(prices[n])
        pendtxt = "'"
        pt = pricetxt
        result = pt.find(date1txt)
        if result == -1:
            pttext='0'
        elif result != -1:

            ptstart = pt.find(date1txt) + 20
            ptend = pt.find(pendtxt, ptstart)
            pttext = pt[ptstart:ptend]
#            print(pttext)
            break
    return (pttext)

#--------------------------------------------------------------------------------------------


#----------------------Volatility Algorithhm used to trade the btc wallet--------------------


def volalgo(year, walletusd, vol, btcamt, walletbtc, currdate, currmonth, curryear,portfoliovalue,len):

    portfoliovalue = portfoliovalue


    def mean(a,b,c):
        mean = (a + b + c)/3
        return mean

    def meanvol(date1, date2, curr1, curr2):

        url = 'http://api.fixer.io/'
        base = '?base=' + curr1

        y1 = url + date1 + base
        t1 = url + date2 + base

        endtxt = ','

        s = requests.get(y1)
        s = s.text
        sstart = s.find(curr2)+5
        send = s.find(endtxt,sstart)
        stext= s[sstart:send]


        t = requests.get(t1)
        t = t.text
        tstart = t.find(curr2)+5
        tend = t.find(endtxt,tstart)
        ttext= t[tstart:tend]

        fx1= float(stext)
        fx2= float(ttext)

        fxdelta = fx2-fx1
        fxchangepct = (abs(fxdelta)/fx1)*100
        pct = str(fxchangepct)

        return(pct)

    def usdpair(curr):
        mv = (meanvol(date1txt1,date2txt1,"USD",curr))
        return(mv)

    A = "GBP"
    #B = 'EUR'
    C = 'CNY'
    D = 'INR'

    for y in range (1,10):

            year = yearint + 1
            month = 0
            for month in range (0,11):

                month = month + 1
                date1 = 0
                date2 = 1
                for d in range (1,31):  #needs fixing only running upto the 28th of the month atm
#                    if not(((date1 == currdate) & (month == currmonth) & (year == curryear))):
                        date1 = date1 + 1
                        date2 = date1 + 1

                        d = date1

                        if (((date2 == 29) & (month == 2)) or (((date2 == 31) & ((month == 4) or (month == 6) or (month == 9) or (month == 11))))):
                            break
                        elif ((date1 == currdate) & (month == currmonth) & (year == curryear)):
                            return(portfoliovalue)
                        else:
                            date1txt = str(datetime.datetime(year, month, date1))
                            date2txt = str(datetime.datetime(year, month, date2))


                            # Truncation of date and time format

                        date1txt1 = date1txt[:10]
#                        print(date1txt1)
                        date2txt1 = date2txt[:10]

                        fxdelta1 = float(usdpair(A))
                        fxdelta2 = float(usdpair(C))
                        fxdelta3 = float(usdpair(D))
                        meanpct = mean(fxdelta1, fxdelta2, fxdelta3)

#
                        btcprice = btcpricingdatabase(len,date1txt1, prices)
                        btcprice = float(btcprice)
#                        print(btcprice)

                        if btcprice == 0:
                            print('No historical pricing for this date - using api processing will be slower')
                            btcprice = btcpricing(date1txt1, date2txt1)
                            btcprice = float(btcprice)

                            if meanpct > vol:  # if mean volatility is higher than the threshold then buy or else sell!
                                btcamt = walletusd / btcprice
                                walletusd = walletusd - btcprice * btcamt
                                walletbtc = walletbtc + btcamt

                            else:
                                btcamt = walletbtc
                                walletusd = btcprice * btcamt + walletusd
                                walletbtc = walletbtc - btcamt

                        elif meanpct > vol:  # if mean volatility is higher than the threshold then buy or else sell!
                            btcamt = walletusd / btcprice
                            walletusd = walletusd - btcprice * btcamt
                            walletbtc = walletbtc + btcamt

                        else:
                            btcamt = walletbtc
                            walletusd = btcprice * btcamt + walletusd
                            walletbtc = walletbtc - btcamt

                        portfoliovalue = walletbtc * btcprice + walletusd
#                        print("Your portfolio value is" + " " + str(portfoliovalue))


#                    else:
#                        return(portfoliovalue)

    return(portfoliovalue)

volincrement = 0.55
vol = 0.01

for v in range (1,9):

    #yearint = 2011 # year to begin backtesting from
    #walletusd = 1000000 # this is the inital value of the wallet
    vol = vol + volincrement # volatility threshold
    print(vol)
    yearint = 2013 # year to begin backtesting from
    walletusd = 1000000 # this is the inital value of the wallet
    btcamt = 0 # number of bitcoin to buy
    walletbtc = 0

    pricenow = btcnow()
    pricenow = pricenow.replace(',', '')

    pricereference = btcpricing (str(yearint)+'-01-01', str(yearint)+'-01-02')

    Passiveperformance = str((float(pricenow)/float(pricereference))*100)

    print('The current live btc price is US$ ' +pricenow + ' and the reference price is US$ ' +pricereference + ' and the passive performance hurdle is '+ Passiveperformance  +' percent')

    date = int(time.strftime("%d"))
    month = int(time.strftime("%m"))
    year = int(time.strftime("%Y"))

    pv = walletusd

    portfoliovalue = volalgo(yearint,walletusd,vol,btcamt,walletbtc,date,month,year,pv,len)

    print('final portfolio value is US$ ' + str(portfoliovalue))
    Activeperformance = ((portfoliovalue / walletusd) - 1)*100

    Activeperf = str(Activeperformance)
    Activeperf = Activeperf[:6]

    print(str(Activeperf)+" percent")