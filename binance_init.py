#depricated
import sqlite3
import logging

def binance_init():
    log = logging.getLogger('')    
    try:
        conn = sqlite3.connect('binance.db')
        cursor = conn.cursor()

        # Если не существует таблиц, их нужно создать (первый запуск)
        orders_q = """
          create table if not exists
            orders (
              order_type TEXT,
              order_pair TEXT,

              buy_order_id NUMERIC,
              buy_amount REAL,
              buy_price REAL,
              buy_created DATETIME,
              buy_finished DATETIME NULL,
              buy_cancelled DATETIME NULL,

              sell_order_id NUMERIC NULL,
              sell_amount REAL NULL,
              sell_price REAL NULL,
              sell_created DATETIME NULL,
              sell_finished DATETIME NULL,
              force_sell INT DEFAULT 0
            );
        """
        cursor.execute(orders_q)

        kline_q = """
          create table if not exists
            kline (
                opentime DATETIME,
                closetime DATETIME,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                number_trade NUMERIC
            );
        """
        cursor.execute(kline_q)
        
        trades_q = """
          create table if not exists
            trades (
                tradetime DATETIME,
                price REAL,
                qty REAL,
                quoteQty REAL,
                tradeid NUMERIC
            );
        """
        cursor.execute(trades_q)

    except Exception as e:
        log.exception(e)
    finally:
        conn.close()

