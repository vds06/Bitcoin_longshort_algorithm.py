import requests
import datetime
import time
#import numpy
import csv
import urllib, pprint
import urllib.parse


#Potential work to be done -
# Find out the maximum drawdown required - in conditions of leverage this will be required to work out what kind of margin calls might be needed

# Give a dynamic weighting to currencies
# Use different signals to control the buy and sell mechanism
# Find out the signals which are really affecting XBT (BTCUSD) price and plug them in
    # Volatility
    # Number of news articles being produced by Newsfeeds
    # Twitter
    # Central bank press releases (especially PBOC - give higher wieghting)
    # SNR! (how to separate? from any signal stream)
    # Connect to margin trading platforms MagNr - Bitmex

# Apply back propagation to all the factors above to intensify returns
# rerun the algo


#Twitter sentiment analysis



text = urllib.parse.quote("châteu", safe='')
'ch%C3%A2teu'


#from urllib import quote_plus

#text = urllib.quote_plus("I'm a huge fan of Cowboy Bebop")
url = "https://jamiembrown-tweet-sentiment-analysis.p.mashape.com/api/"
r = requests.get(url, {"text": text})
pprint.pprint(r.json())

# {'sentiment': 'positive', 'score': 0.451951011074}

#------------------------------------------------------------------------




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

with open('FXCSV2_4.csv') as csvfile:
    reader2 = csv.reader(csvfile, delimiter=',')

    rates = []

    for row in reader2:
        rate = row[0]
        rates.append(rate)

    ratetestelement = rates[2]

#    fxlen = len(rates) - 3


#    print(fxlen)
#    print(rates)
#    print(ratetestelement)

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

# FX pricing database function below operates in exactly the same way as the BTC pricing database function above

def fxpricingdatabase(len, date1txt, curr): # len needs to be replaced with fxlen (to execute upto the length of the fx database)
    for n in range(2, len):
        nminusone = n - 1
        ratetxt = str(rates[nminusone:n])
        pendtxt = "'"
        pt = ratetxt
        date1txtslash = date1txt.replace("-","/")
#        print(date1txtslash)
        result = pt.find(date1txtslash)
        if result == -1:

            #pttext='0'
#            print (date1txt)




            # setup a recursive function
#            pttext = fxpricingdatabase(len, recurrsivedate, curr)
            # split function and reconcatenate date1text to subtract one from date till a result can be established from the loop

            pttext = "null"
#            break

        elif result != -1:

            string = pt
            mylist = pt.split(',')

#            print(mylist)

            inr = str(mylist[6:7])
            cny = str(mylist[5:6])
            gbp = str(mylist[4:5])

            if curr is "INR" :
                pttext = inr
                pendtxt = "\\"
                ptstart = pttext.find('"') + 1
                ptend = pttext.find(pendtxt, ptstart)
                pttext = pttext[ptstart:ptend]
 #               print(pttext)



            elif curr is "CNY" :
                pttext = cny

                ptstart = pttext.find("'") + 1
                ptend = pttext.find(pendtxt, ptstart)
                pttext = pttext[ptstart:ptend]
 #               print(pttext)



            elif curr is "GBP" :
                pttext = gbp

                ptstart = pttext.find("'") + 1
                ptend = pttext.find(pendtxt, ptstart)
                pttext = pttext[ptstart:ptend]
 #               print(pttext)


 #               print(pttext + "this is currency fetched")

            break


    return(pttext)

#--------------------------------------------------------------------------------------------


#----------------------Volatility Algorithhm used to trade the btc wallet--------------------


def volalgo(year, walletusd, vol, btcamt, walletbtc, currdate, currmonth, curryear,portfoliovalue,len):

    portfoliovalue = portfoliovalue
    minportfoliovalue = portfoliovalue


    def mean(a,b,c):
        mean = (a + b + c)/3
        return mean

    def meanvol(date1, date2, curr1, curr2):

        databaseflag = 1

        if databaseflag == 0 :

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

        else:


            stext = "null"
            ttext = "null"
            recursivedateloppcnt1=1
            recursivedateloppcnt2=1
            while stext is "null":

                from datetime import datetime, timedelta


                recurrsivedate = date1txt.replace("/", "-")
                recurrsivedate = recurrsivedate[0:10]
                recurrsivedate = str(datetime.strptime(recurrsivedate, "%Y-%m-%d" ) - timedelta(days=recursivedateloppcnt1))
                recurrsivedate = recurrsivedate[0:10]
#                print(recurrsivedate)

                stext = fxpricingdatabase(len, recurrsivedate, curr2)

                recursivedateloppcnt1=recursivedateloppcnt1+1

            while ttext is "null":
                from datetime import datetime, timedelta

                recurrsivedate2 = date2txt.replace("/", "-")
                recurrsivedate2 = recurrsivedate2[0:10]
                recurrsivedate2 = str(datetime.strptime(recurrsivedate2, "%Y-%m-%d") - timedelta(days=recursivedateloppcnt2))
                recurrsivedate2 = recurrsivedate2[0:10]
                ttext = fxpricingdatabase(len, recurrsivedate2, curr2)
                recursivedateloppcnt2=recursivedateloppcnt2+1

#            print(stext)
#            print(ttext)

        fx1= float(stext)
        fx2= float(ttext)

#        print(fx1)
#        print(fx2)


        fxdelta = fx2-fx1
        fxchangepct = (abs(fxdelta)/fx1)*100
        pct = str(fxchangepct)


        return(pct)

    def usdpair(curr,date1txt1,date2txt1):
        mv = (meanvol(date1txt1,date2txt1,"USD",curr))
        return(mv)

    A = "GBP"
    #B = 'EUR'
    C = "CNY"
    D = "INR"
    year = yearint

    for y in range (1,10):

            year = year + 1
            month = 0
            for month in range (1,12):
                month = month + 1
                date1 = 0
                date2 = 1
                for d in range (1,31):  #needs fixing only running upto the 28th of the month atm
#                    if not(((date1 == currdate) & (month == currmonth) & (year == curryear))):
                        date1 = d
                        date2 = d + 1


                        if minportfoliovalue > portfoliovalue:
                            minportfoliovalue = portfoliovalue
#                            return (minportfoliovalue)



                        if (((date2 == 29) & (month == 2)) or (((date2 == 31) & ((month == 4) or (month == 6) or (month == 9) or (month == 11))))):
                            break
                        elif ((date1 == currdate) & (month == currmonth) & (year == curryear)):
                            return(portfoliovalue,minportfoliovalue)
                        else:

                            date2txt = str(datetime.datetime(year, month, date2))

                        if (((date1 == 29) & (month == 2)) or (((date1 == 31) & ((month == 4) or (month == 6) or (month == 9) or (month == 11))))):
                            break
                        elif ((date1 == currdate) & (month == currmonth) & (year == curryear)):
                            return (portfoliovalue,minportfoliovalue)
                        else:

                            date1txt = str(datetime.datetime(year, month, date1))

                            # Truncation of date and time format

                        date1txt1 = date1txt[:10]
#                        print(date1txt1)
                        date2txt1 = date2txt[:10]

                        fxdelta1 = float(usdpair(A,date1txt1,date2txt1))
                        fxdelta2 = float(usdpair(C,date1txt1,date2txt1))
                        fxdelta3 = float(usdpair(D,date1txt1,date2txt1))
                        meanpct = mean(fxdelta1, fxdelta2, fxdelta3)

#
                        btcprice = btcpricingdatabase(len,date1txt1, prices)
                        btcprice = float(btcprice)
#                        print(btcprice)

                        if btcprice == 0:
#                            print('No historical pricing for this date - using api processing will be slower')
                            btcprice = btcpricing(date1txt1, date2txt1)
                            btcprice = float(btcprice)

                            if meanpct < vol:  # if mean volatility is lower than the threshold then buy or else sell! (Edit: this was reversed to produce better gains)
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
#                        print (("Your minimum portfolio value is" + " " + str(minportfoliovalue)))


#                    else:
#                        return(portfoliovalue)
#                        return(minportfoliovalue)
                        returnvars  = [portfoliovalue,minportfoliovalue]
#                        return(portfoliovalue,minportfoliovalue)


#                        print(returnvars)


#                return(minportfoliovalue)

    return (minportfoliovalue, portfoliovalue)



#    return(portfoliovalue,minportfoliovalue)
#    return (portfoliovalue, minportfoliovalue)


volincrement = 0.001
vol = 0.275

for v in range (1,99):

    #yearint = 2011 # year to begin backtesting from
    #walletusd = 1000000 # this is the inital value of the wallet
    vol = vol + volincrement # volatility threshold
    print(vol)
    yearint = 2015 # year to begin backtesting from
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

    portfoliovalue = []
    portfoliovalue = (volalgo(yearint,walletusd,vol,btcamt,walletbtc,date,month,year,pv,len))


    print(portfoliovalue)
#    minportfoliovalue = returnvars[:1]

#    print (portfoliovalue['minportfoliovalue'])
    print('final portfolio value is US$ ' + str(portfoliovalue))
    Activeperformance = ((portfoliovalue[0] / walletusd) - 1)*100

    Activeperf = str(Activeperformance)
    Activeperf = Activeperf[:6]

    drawdown = walletusd - portfoliovalue[1]

    print(str(Activeperf)+" percent" + "with drawdown of " + str(drawdown))