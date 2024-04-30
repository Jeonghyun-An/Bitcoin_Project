import pyupbit

df = pyupbit.get_ohlcv("KRW-BTC")
# print(df.head())
df.to_excel("btc.xlsx")