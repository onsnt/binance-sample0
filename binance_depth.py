import websocket
import logging
import json

from binance_enums import *

def on_message(ws, message):
    global COUNT_OF_DEPTH
    jmessage = json.loads(message)
    bid0 = str(jmessage['bids'][0][0])
    ask0 = str(jmessage['asks'][0][0])
    print('bid:' + bid0 +' ask:'+ask0)
        
    if COUNT_OF_DEPTH>MAX_COUNT_OF_DEPTH:
        ws.close()

    COUNT_OF_DEPTH = COUNT_OF_DEPTH+1

def on_error( ws, error):
    log = logging.getLogger('')
    print(error)
    log.exception(error)

def on_close(ws):
    log = logging.getLogger('')
    log.debug("### closed ###")
    
def on_open(ws):
    global COUNT_OF_DEPTH
    log = logging.getLogger('')
    log.debug("### connected ###")
    
    COUNT_OF_DEPTH = 0

def get_depth():
    
    ConectionString = "wss://stream.binance.com:9443/ws/"+DEF_SYMBOL.lower()+"@depth10"
    
    ws = websocket.WebSocketApp(ConectionString,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()