from datetime import *
import pandas as pd
from binance_enums import *
from binance_utility import download_file, get_all_symbols, get_parser, convert_to_date_object, get_path

import logging

# sample arg for download ETHUSDT BTCUSDT BNBBUSD spot trades from year 2020, month of Feb and Dec with CHECKSUM
# arg -t spot -s ETHUSDT BTCUSDT BNBBUSD -y 2020 -m 02 12 -c 1
# sample arg for download all symbols' daily USD-M futures trades from 2021-01-01 to 2021-02-02
# arg -t um -skip-monthly 1 -startDate 2021-01-01 -endDate 2021-02-02


def download_monthly_klines(trading_type, symbols, num_symbols, intervals, years, months, start_date, end_date, folder, checksum):
    log = logging.getLogger('')
    current = 0
    date_range = None

    if start_date and end_date:
        date_range = str(start_date) + " " + str(end_date)

    print("Found {} symbols".format(num_symbols))

    for symbol in symbols:
        print("[{}/{}] - start download monthly {} klines ".format(current +
              1, num_symbols, symbol))
        for interval in intervals:
            for year in years:
                for month in months:
                    current_date = convert_to_date_object(
                        '{}-{}-01'.format(year, month))
                    if current_date >= start_date and current_date <= end_date:

                        path = get_path(
                            trading_type, "klines", "monthly", symbol, interval)
                        file_name = "{}-{}-{}-{}.zip".format(
                            symbol.upper(), interval, year, '{:02d}'.format(month))
                        download_file(path, file_name, date_range, folder)

                        if checksum == 1:
                            checksum_path = get_path(
                                trading_type, "klines", "monthly", symbol, interval)
                            checksum_file_name = "{}-{}-{}-{}.zip.CHECKSUM".format(
                                symbol.upper(), interval, year, '{:02d}'.format(month))
                            download_file(
                                checksum_path, checksum_file_name, date_range, folder)

                        current += 1


def download_daily_klines(trading_type, symbols, num_symbols, intervals, dates, start_date, end_date, folder, checksum):
    log = logging.getLogger('')
    current = 0
    date_range = None

    if start_date and end_date:
        date_range = str(start_date) + " " + str(end_date)

    # Get valid intervals for daily
    intervals = list(set(intervals) & set(DAILY_INTERVALS))
    print("Found {} symbols".format(num_symbols))

    for symbol in symbols:
        print("[{}/{}] - start download daily {} klines ".format(current +
              1, num_symbols, symbol))
        for interval in intervals:
            for date in dates:
                current_date = convert_to_date_object(date)
                if current_date >= start_date and current_date <= end_date:
                    try:
                        path = get_path(trading_type, "klines",
                                        "daily", symbol, interval)
                        file_name = "{}-{}-{}.zip".format(
                            symbol.upper(), interval, date)
                        download_file(path, file_name, date_range, folder)

                        if checksum == 1:
                            checksum_path = get_path(
                                trading_type, "klines", "daily", symbol, interval)
                            checksum_file_name = "{}-{}-{}.zip.CHECKSUM".format(
                                symbol.upper(), interval, date)
                            download_file(
                                checksum_path, checksum_file_name, date_range, folder)
                    except Exception as e:
                        log.exception(e)
        current += 1


def download_csv():

    if not DEF_SYMBOL:
        print("fetching all symbols from exchange")
        symbols = get_all_symbols(TYPE_SYMBOL)
        num_symbols = len(symbols)

    else:
        symbols = [DEF_SYMBOL]
        num_symbols = len(symbols)

    period = convert_to_date_object(datetime.today().strftime(
        '%Y-%m-%d')) - convert_to_date_object(PERIOD_START_DATE)
    dates = pd.date_range(end=datetime.today(),
                          periods=period.days + 1).to_pydatetime().tolist()
    dates = [date.strftime("%Y-%m-%d") for date in dates]

    if SKIP_MONTHLY == 0:
        download_monthly_klines(TYPE_SYMBOL, symbols, num_symbols, INTERVALS,
                                YEARS, MONTHS, START_DATE, END_DATE, DATA_FOLDER, CHECK_SUM)

    if SKIP_DAILY == 0:
        download_daily_klines(TYPE_SYMBOL, symbols, num_symbols, INTERVALS,
                              dates, START_DATE, END_DATE, DATA_FOLDER, CHECK_SUM)
