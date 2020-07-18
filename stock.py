import yfinance as yf
# ^GSPC
msft = yf.Ticker("^DJI")
# "^IXIC"
# get stock info
print(msft.info)

# get historical market data
hist = msft.history(period="5d")
print(hist)