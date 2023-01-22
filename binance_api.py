import hashlib
import hmac
import time
import urllib
import configparser

from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import requests

class Binance():

    methods = {
            # public methods
            'ping':             {'url':'api/v3/ping', 'method': 'GET', 'private': False},
            'time':             {'url':'api/v3/time', 'method': 'GET', 'private': False},
            'exchangeInfo':     {'url':'api/v3/exchangeInfo', 'method': 'GET', 'private': False},
            'depth':            {'url': 'api/v3/depth', 'method': 'GET', 'private': False},
            'trades':           {'url': 'api/v3/trades', 'method': 'GET', 'private': False},
            'historicalTrades': {'url': 'api/v3/historicalTrades', 'method': 'GET', 'private': False},
            'aggTrades':        {'url': 'api/v3/aggTrades', 'method': 'GET', 'private': False},
            'klines':           {'url': 'api/v3/klines', 'method': 'GET', 'private': False},
            'ticker24hr':       {'url': 'api/v3/ticker/24hr', 'method': 'GET', 'private': False},
            'tickerPrice':      {'url': 'api/v3/ticker/price', 'method': 'GET', 'private': False},
            'tickerBookTicker': {'url': 'api/v3/ticker/bookTicker', 'method': 'GET', 'private': False},
            # private methods
            'createOrder':      {'url': 'api/v3/order', 'method': 'POST', 'private': True},
            'testOrder':        {'url': 'api/v3/order/test', 'method': 'POST', 'private': True},
            'orderInfo':        {'url': 'api/v3/order', 'method': 'GET', 'private': True},
            'cancelOrder':      {'url': 'api/v3/order', 'method': 'DELETE', 'private': True},
            'openOrders':       {'url': 'api/v3/openOrders', 'method': 'GET', 'private': True},
            'allOrders':        {'url': 'api/v3/allOrders', 'method': 'GET', 'private': True},
            'account':          {'url': 'api/v3/account', 'method': 'GET', 'private': True},
            'myTrades':         {'url': 'api/v3/myTrades', 'method': 'GET', 'private': True},
            # wapi
            'depositAddress':   {'url': '/wapi/v3/depositAddress.html', 'method':'GET', 'private':True},
            'withdraw':   {'url': '/wapi/v3/withdraw.html', 'method':'POST', 'private':True},
            'depositHistory': {'url': '/wapi/v3/depositHistory.html', 'method':'GET', 'private':True},
            'withdrawHistory': {'url': '/wapi/v3/withdrawHistory.html', 'method':'GET', 'private':True},
            'withdrawFee': {'url': '/wapi/v3/withdrawFee.html', 'method':'GET', 'private':True},
            'accountStatus': {'url': '/wapi/v3/accountStatus.html', 'method':'GET', 'private':True},
            'systemStatus': {'url': '/wapi/v3/systemStatus.html', 'method':'GET', 'private':True},
    }
    
    def __init__(self):

        config = configparser.ConfigParser()
        config.readfp(open(r'bot.cfg'))
        API_KEY = config.get('Binance', 'API_KEY')
        API_SECRET = config.get('Binance', 'API_SECRET')
        baseurl = config.get('Binance', 'baseurl')  

        self.API_KEY = API_KEY
        self.API_SECRET = bytearray(API_SECRET, encoding='utf-8')
        self.shift_seconds = 0
        self.baseurl = baseurl

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            kwargs.update(command=name)
            return self.call_api(**kwargs)
        return wrapper

    def set_shift_seconds(self, seconds):
        self.shift_seconds = seconds
        
    def call_api(self, **kwargs):

        command = kwargs.pop('command')
        #api_url = 'https://api.binance.com/' + self.methods[command]['url']
        api_url = self.baseurl + self.methods[command]['url']
        payload = kwargs
        headers = {}
        
        payload_str = urllib.parse.urlencode(payload)
        if self.methods[command]['private']:
            payload.update({'timestamp': int(time.time() + self.shift_seconds - 1) * 1000})
            payload_str = urllib.parse.urlencode(payload).encode('utf-8')
            sign = hmac.new(
                key=self.API_SECRET,
                msg=payload_str,
                digestmod=hashlib.sha256
            ).hexdigest()

            payload_str = payload_str.decode("utf-8") + "&signature="+str(sign) 
            headers = {"X-MBX-APIKEY": self.API_KEY}

        if self.methods[command]['method'] == 'GET':
            api_url += '?' + payload_str

        response = requests.request(method=self.methods[command]['method'], url=api_url, data="" if self.methods[command]['method'] == 'GET' else payload_str, headers=headers)
        if 'code' in response.text:
            print(response.text)
        return response.json()
