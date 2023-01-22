import configparser
from datetime import *

config = configparser.ConfigParser()
config.readfp(open(r'bot.cfg'))


YEARS = ['2017', '2018', '2019', '2020', '2021', '2022', '2023']
MONTHS = list(range(1, 13))
INTERVALS = ["1m", "3m", "5m", "15m", "30m", "1h", "2h",
             "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1mo"]
DAILY_INTERVALS = ["1m", "3m", "5m", "15m", "30m",
                   "1h", "2h", "4h", "6h", "8h", "12h", "1d"]
TRADING_TYPE = ["spot", "um", "cm"]

TRAIN_PROC = float(config.get('ML', 'Train_Proc'))

PERIOD_START_DATE = config.get('General', 'START_DATE')
PERIOD_END_DATE = config.get('General', 'END_DATE')
DATA_FOLDER = config.get('General', 'DATA_FOLDER')

BASE_URL = config.get('Binance', 'databaseurl')
BUY_LIFE_TIME_SEC = config.get('Binance', 'BUY_LIFE_TIME_SEC')
STOCK_FEE = config.get('Binance', 'STOCK_FEE')
USE_BNB_FEES = config.get('Binance', 'USE_BNB_FEES')


START_DATE = date(int(YEARS[6]), MONTHS[0], 1)
END_DATE = datetime.date(datetime.now())

SKIP_DAILY = int(config.get('Download', 'skip_daily'))
SKIP_MONTHLY = int(config.get('Download', 'skip_monthly'))
CHECK_SUM = int(config.get('Download', 'check_sum'))
DEF_SYMBOL = config.get('Download', 'def_symbol')
DEF_INTERVAL = config.get('Download', 'def_interval')

TYPE_SYMBOL = config.get('Download', 'type_sumbol')
MAX_COUNT_OF_DEPTH = 5
COUNT_OF_DEPTH = 0
