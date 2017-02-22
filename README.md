# Bitcoin_longshort_algorithm.py
A small long-short algorithm that buys and sells bitcoin - based on day-to-day intra-fiat-currency volatility (CNY/INR/GBP v USD)
Currently relies on 2 APIs (Coindesk and Fixer.io) to source data (BTC pricing and FX respectively) - however, because of limitations on calling - these are being
kept as fallback options to utilising CSV files for back testing with data downloaded prior to execution - this also helps with 
the speed of algorithm execution.



#Potential work to be done -
# Give a dynamic weighting to currencies
# Use different signals to control the buy and sell mechanism
# Find out the signals which are really affecting XBT (BTCUSD) price and plug them in
# rerun the algo

