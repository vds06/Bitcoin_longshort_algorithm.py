import requests
import datetime
import time
#import numpy



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
    print(btc.text  )

    char1 = "{"
    char2 = ","
    btc=btc.text
    btctext = btc[btc.find(char1)+21:btc.find(char2)]

    if  btctext.find('}'):
        btctext = btctext.replace('}', '')

    print(btctext)
    return(btctext)

def volalgo(year, walletusd, vol, btcamt, walletbtc, currdate, currmonth, curryear):

#----------------------Bitcoin Price function using Coindesk price API-----------------------

#--------------------------------------------------------------------------------------------

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
    #   (fx1)
        fx2= float(ttext)
    #   print(fx2)

        fxdelta = fx2-fx1
        fxchangepct = (abs(fxdelta)/fx1)*100
        pct = str(fxchangepct)
    #   print(  pct + " percent")

        return(pct)

    def usdpair(curr):
        mv = (meanvol(date1txt1,date2txt1,"USD",curr))
        return(mv)

    A = "GBP"
    #B = 'EUR'
    C = 'CNY'
    D = 'INR'

    for y in range (1,10):

            year = year + 1



            month = 0
            for month in range (0,11):

                month = month + 1
                date1 = 0
                date2 = 1
                for d in range (1,31):  #needs fixing only running upto the 28th of the month atm
                    if (((date1 == currdate) & (month == currmonth) & (year == curryear))):
                        break
                    else:




                        date1 = date1 + 1
                        date2 = date1 + 1
    #                    datecutoff = date1
                        d = date1
#                        print(datecutoff)

                        if (((date2 == 29) & (month == 2)) or (((date2 == 31) & ((month == 4) or (month == 6) or (month == 9) or (month == 11))))):
                            break
                        else:
                            date1txt = str(datetime.datetime(year, month, date1))
                            date2txt = str(datetime.datetime(year, month, date2))

                            # Truncation of date and time format

                        date1txt1 = date1txt[:10]
                        date2txt1 = date2txt[:10]

                        fxdelta1 = float(usdpair(A))
                        fxdelta2 = float(usdpair(C))
                        fxdelta3 = float(usdpair(D))
                        meanpct = mean(fxdelta1, fxdelta2, fxdelta3)

                        btcprice = btcpricing(date1txt1, date2txt1)
                        #             print(btcprice)
                        btcprice = float(btcprice)
                        if meanpct > vol:  # if mean volatility is higher than the threshold then buy or else sell!
                            btcamt = walletusd / btcprice
                            #           print("You are buying " +str(btcamt)+ " bitcoin")
                            walletusd = walletusd - btcprice * btcamt
                            walletbtc = walletbtc + btcamt

                        else:
                            btcamt = walletbtc
                            walletusd = btcprice * btcamt + walletusd
                            walletbtc = walletbtc - btcamt
                            #               print("You are selling " +str(btcamt)+ " bitcoin")
                            #           print("Your current balance is US$" + str(walletusd)+" with " + str(walletbtc) + " stored.")
                            # total portfolio value

                        portfoliovalue = walletbtc * btcprice + walletusd
                        print("Your portfolio value is" + " " + str(portfoliovalue))



    return (portfoliovalue)

#    label .end

yearint = 2016 # year to begin backtesting from
walletusd = 10000 # this is the inital value of the wallet
vol = 0.09 # volatility threshold
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


portfoliovalue = volalgo(yearint,walletusd,vol,btcamt,walletbtc,date,month,year)

Print('final portfolio value is US$ ' + str(portfoliovalue))
Activeperformance = (portfoliovalue*100 / walletusd)

Print(Activeperformance)