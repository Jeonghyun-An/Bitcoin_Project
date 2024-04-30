# Rest API
import requests
import pyupbit
import pandas as pd
import pprint
import time
import datetime

# url = "https://api.upbit.com/v1/market/all" #?isDetails=true
# #headers = {"accept": "application/json"}
#
# resp = requests.get(url)
# data = resp.json()  # JSON
#
# krw_tickers = []
# for coin in data :
#     ticker = coin['market']     # coin in dict
#
#     if ticker.startswith("KRW"):
#         krw_tickers.append(ticker)
# print(krw_tickers)
# print(len(krw_tickers))
#################################################################################
# '''마켓 코드 조회'''
# tickers = pyupbit.get_tickers(fiat="KRW")
# print(tickers)
# print(len(tickers))
#
# '''분봉 캔들로 조회(1분봉)https://api.upbit.com/v1/candles/minutes/1?market=KRW-BTC&count=1'''
# '''open / high / low / volume / value'''
# df = pyupbit.get_ohlcv("KRW-BTC","minute1")
# print(df)
#
# '''일봉 캔들로 조회 (https://api.upbit.com/v1/candles/days)'''
# df = pyupbit.get_ohlcv(ticker="KRW-BTC",interval="day",count=100)
# print(df)
#
# '''주봉 캔들로 조회 (https://api.upbit.com/v1/candles/weeks)'''
# df = pyupbit.get_ohlcv(ticker="KRW-BTC",interval="week")
# df.to_excel("week_btc.xlsx")
#
# '''월봉 캔들로 조회 (https://api.upbit.com/v1/candles/months)'''
# pd.options.display.float_format = "{:.1f}".format       # value값이 지수값으로 표현되기 때문에 실수형으로 포맷변경
# df = pyupbit.get_ohlcv(ticker="KRW-BTC",interval="month")
# print(df)

#############################################################################
# '''현재가 정보(종가) 조회'''
# '''get_current_price 함수'''
# krw_tickers = pyupbit.get_tickers(fiat="KRW")
# prices = pyupbit.get_current_price(krw_tickers)
#
# for k,v in prices.items():
#     print(k,v)
#
# '''호가 정보 조회'''
# '''get_orderbook()'''
# # orderbooks = pyupbit.get_orderbook(krw_tickers)
# # print(orderbooks)
# orderbooks = pyupbit.get_orderbook("KRW-BTC")
# pprint.pprint(orderbooks)       # pretty print
#
# orderbook = orderbooks[0]
#
# total_ask_size = orderbook['total_ask_size']
# total_bid_size = orderbook['total_bid_size']
#
# print("매도호가 총합: ",total_ask_size)
# print("매수호가 총합: ",total_bid_size)
#
#
# '''회원가입 및 로그인'''
# f = open("upbit.txt")
# lines = f.readlines()
# access = lines[0].strip()   # access key '/n' remove
# secret = lines[1].strip()   # secret key
# f.close()
# upbit = pyupbit.Upbit(access,secret)    # Class instance, object
# print("Autotrade start")

# balance = upbit.get_balance("KRW")  # 특정 잔고 조회
# print(balance)
#
#
# '''잔고조회'''
# balances = upbit.get_balances()
# # print(balances)
# # pprint.pprint(balances[0])
#
# print(balance,type(balance))
#
# '''지정가 매수주문'''
# # xrp_price = upbit.buy_limit_order("KRW-XRP")
# # print(xrp_price)
# # 지정가 주문을 통해서 매매금액보다 낮게 테스팅
# resp = upbit.buy_limit_order("KRW-XRP", 200, 100)   # 종목,금액,수량
# pprint.pprint(resp)
#
# '''지정가 매도주문'''
# xrp_balance = upbit.get_balance("KRW-XRP")
# resp = upbit.sell_limit_order("KRW-XRP",265,xrp_balance)
# print(resp)
#
# '''시장가 매수주문'''
# '''buy_market_order(티커,주문총가격(원화))'''
# resp = upbit.buy_market_order("KRW-XRP",10000)     # 비트코인을 만원어치 구매
# pprint.pprint(resp)
#
# '''시장가 매도주문'''
# '''sell_market_order(티커,주문량)'''
#
# '''주문취소'''
# '''cancel_order(uuid)'''
# upbit.buy_limit_order("KRW-XRP",200,100)
# uuid = resp[0]['uuid']
# resp = upbit.cancel_order(uuid)
# pprint.pprint(resp)
#
# '''1초에 한번 현재시간과 비트코인 가격이 출력하기'''
# while True:
#     now = datetime.datetime.now()
#     price = pyupbit.get_current_price("KRW-BTC")
#     print(now,price)
#     time.sleep(1)
#############################################################
'''인공지능 이용하기'''


############################################################
'''변동성 돌파 전략에 의거하여 값 구하기'''
def cal_target(ticker):
    df = pyupbit.get_ohlcv(ticker,"day")
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    yesterday_range = yesterday['high']-yesterday['low']
    target = today['open']+yesterday_range * 0.5
    return target

##################객체생성###########
f = open("upbit.txt")
lines = f.readlines()
access = lines[0].strip()   # access key '/n' remove
secret = lines[1].strip()   # secret key
f.close()
upbit = pyupbit.Upbit(access,secret)    # Class instance, object

#############변수생성############
target = cal_target("KRW-BTC")

'''첫날은 매수 안되게 하는용 변수(변동성 돌파 전략 때문)'''
op_mode = False

'''매수기능 추가 용 변수'''
hold = False

'''시간에 맞춰서 갱신하기'''
while True:
    try:
        now = datetime.datetime.now()
        '''매도 시도'''
        if now.hour == 8 and now.minute == 59 and 50 <= now.second <= 59:
            if op_mode is True and hold is True:
                btc_balance = upbit.get_balance("KRW-BTC")
                upbit.sell_market_order("KRW-BTC",btc_balance*0.9995)
                hold = False
            op_mode=False
            time.sleep(10)

        '''9시 목표일 때 목표값 계산'''
        if now.hour == 9 and now.minute==0 and 20 <= now.second <= 30:
            target = cal_target("KRW-BTC")
            op_mode = True
            time.sleep(5)   # 생략 가능

        price = pyupbit.get_current_price("KRW-BTC")

        '''매 초 마다 조건을 확인한 수 매수 시도'''
        if op_mode is True and hold is False and price is not None and price >= target:
            '''매수'''
            krw_balance = upbit.get_balance("KRW")
            if krw_balance > 5000:
                upbit.buy_market_order("KRW-BTC", krw_balance*0.9995)
                hold = True
        '''상태 출력'''
        print(f"현재시간 :{now}  목표가: {target} 보유상태: {hold} 동작상태: {op_mode}")
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)