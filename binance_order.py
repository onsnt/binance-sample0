import sqlite3
import logging
import os
import time as t

from binance_api import Binance
from binance_enums import *

bot = Binance()

limits = bot.exchangeInfo()
local_time = int(t.time())
server_time = int(limits['serverTime'])//1000

logging.basicConfig(
    format="%(asctime)s [%(levelname)-5.5s] %(message)s",
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler("{path}/logs/{fname}.log".format(
            path=os.path.dirname(os.path.abspath(__file__)), fname="binance")),
        logging.StreamHandler()
    ])

log = logging.getLogger('')

shift_seconds = server_time-local_time
bot.set_shift_seconds(shift_seconds)


def adjust_to_step(value, step, increase=False):
    return ((int(value * 100000000) - int(value * 100000000) % int(
        float(step) * 100000000)) / 100000000)+(float(step) if increase else 0)


def open_order():

    buy_amount = float(0)
    need_price = float(0)
    try:
        buy_amount = float(input('Enter your amout fo buy: '))
    except:
        print('Wrong input. Please enter a number ...')
        
    try:
        need_price = float(input('Enter price for limit order: '))
    except:
        print('Wrong input. Please enter a number ...')
        
    try:
        conn = sqlite3.connect('binance.db')
        cursor = conn.cursor()

        for elem in limits['symbols']:
            if elem['symbol'] == DEF_SYMBOL:
                CURR_LIMITS = elem
                break
        
        if CURR_LIMITS:
            pass    
        else:
            raise Exception(
                    "No settings for " + DEF_SYMBOL)
        
        if buy_amount*need_price < float(CURR_LIMITS['filters'][2]['minNotional']):
            raise Exception(
                    "Wrong qty min " + DEF_SYMBOL)

        new_order = bot.createOrder(
            symbol=DEF_SYMBOL,
            recvWindow=5000,
            side='BUY',
            type='LIMIT',
            timeInForce='GTC',  # Good Till Cancel
            quantity="{quantity:0.{precision}f}".format(
                                quantity=buy_amount, precision=CURR_LIMITS['baseAssetPrecision']
            ),
            price="{price:0.{precision}f}".format(
                price=need_price, precision=CURR_LIMITS['baseAssetPrecision']
            ),
            newOrderRespType='FULL'
        )
        if 'orderId' in new_order:
            log.info("Create buy order {new_order}".format(
                new_order=new_order))
            cursor.execute(
                """
                                  UPDATE orders
                                  SET
                                    order_type = 'buy',
                                    order_pair = :order_pair,
                                    buy_finished = datetime(),
                                    buy_order_id = :buy_order_id,
                                    buy_created = datetime(),
                                    buy_amount = :buy_amount,
                                    buy_price = :buy_initial_price
                                  

                                """, {
                    'buy_order_id': new_order['orderId'],
                    'buy_amount': buy_amount,
                    'buy_initial_price': need_price,
                    'order_pair': DEF_SYMBOL
                }
            )
            conn.commit()

        else:
            log.warning("Create order error {new_order}".format(
                new_order=new_order))
    except Exception as e:
        log.exception(e)
    finally:
        conn.close()

def close_all_order():

    for elem in limits['symbols']:
        if elem['symbol'] == DEF_SYMBOL:
            CURR_LIMITS = elem
            break
        
    if CURR_LIMITS:
        pass    
    else:
        raise Exception(
            "No settings for " + DEF_SYMBOL)
    try:
        conn = sqlite3.connect('binance.db')
        cursor = conn.cursor()

        orders_info = {}

        for row in cursor.execute("""
            SELECT
                CASE WHEN order_type='buy' THEN buy_order_id ELSE sell_order_id END order_id
                , order_type
                , order_pair
                , sell_amount
                , sell_price
                ,  strftime('%s',buy_created)
                , buy_amount
                , buy_price 
            FROM
              orders
            WHERE
              order_pair = :order_pair AND buy_cancelled IS NULL AND CASE WHEN order_type='buy' THEN buy_finished IS NULL ELSE sell_finished IS NULL END

                """, {
                'order_pair': DEF_SYMBOL
        }
        ):
            orders_info[str(row[0])] = {'order_type': row[1], 'order_pair': row[2], 'sell_amount': row[3], 'sell_price': row[4],
                                        'buy_created': row[5], 'buy_amount': row[6], 'buy_price': row[7]}

        if orders_info:
            log.debug("Orders from DB: {orders}".format(
                orders=[(order, orders_info[order]['order_pair']) for order in orders_info]))

            for order in orders_info:
                stock_order_data = bot.orderInfo(
                    symbol=orders_info[order]['order_pair'], orderId=order)

                order_status = stock_order_data['status']
                log.debug(
                    "Order status {order} - {status}".format(order=order, status=order_status))
                if order_status == 'NEW':
                    log.debug('Order {order} dont execute'.format(order=order))

                if orders_info[order]['order_type'] == 'buy':

                    if order_status == 'FILLED':
                        log.info("""
                            Order {order} executed, buy {exec_qty:0.8f}.
                            Sell order create
                        """.format(
                            order=order, exec_qty=float(
                                stock_order_data['executedQty'])
                        ))

                        for elem in limits['symbols']:
                            if elem['symbol'] == orders_info[order]['order_pair']:
                                CURR_LIMITS = elem
                                break
                        else:
                            raise Exception("NO settings for " + DEF_SYMBOL)

                        has_amount = orders_info[order]['buy_amount'] * \
                            ((1-STOCK_FEE) if not USE_BNB_FEES else 1)

                        sell_amount = adjust_to_step(
                            has_amount, CURR_LIMITS['filters'][2]['stepSize'])

                        need_to_earn = orders_info[order]['buy_amount'] * \
                            orders_info[order]['buy_price']

                        min_price = (need_to_earn/sell_amount) / \
                            ((1-STOCK_FEE) if not USE_BNB_FEES else 1)

                        cut_price = max(
                            adjust_to_step(
                                min_price, CURR_LIMITS['filters'][0]['tickSize'], increase=True),
                            adjust_to_step(
                                min_price, CURR_LIMITS['filters'][0]['tickSize'])
                        )

                        curr_rate = float(bot.tickerPrice(
                            symbol=orders_info[order]['order_pair'])['price'])

                        need_price = max(cut_price, curr_rate)

                        new_order = bot.createOrder(
                            symbol=orders_info[order]['order_pair'],
                            recvWindow=5000,
                            side='SELL',
                            type='LIMIT',
                            timeInForce='GTC',  # Good Till Cancel
                            quantity="{quantity:0.{precision}f}".format(
                                quantity=sell_amount, precision=CURR_LIMITS['baseAssetPrecision']
                            ),
                            price="{price:0.{precision}f}".format(
                                price=need_price, precision=CURR_LIMITS['baseAssetPrecision']
                            ),
                            newOrderRespType='FULL'
                        )

                        if 'orderId' in new_order:
                            log.info("Создан ордер на продажу {new_order}".format(
                                new_order=new_order))
                            cursor.execute(
                                """
                                  UPDATE orders
                                  SET
                                    order_type = 'sell',
                                    buy_finished = datetime(),
                                    sell_order_id = :sell_order_id,
                                    sell_created = datetime(),
                                    sell_amount = :sell_amount,
                                    sell_price = :sell_initial_price
                                  WHERE
                                    buy_order_id = :buy_order_id

                                """, {
                                    'buy_order_id': order,
                                    'sell_order_id': new_order['orderId'],
                                    'sell_amount': sell_amount,
                                    'sell_initial_price': need_price
                                }
                            )
                            conn.commit()

                        else:
                            log.warning("Dont create sell order {new_order}".format(
                                new_order=new_order))

                    elif order_status == 'NEW':
                        order_created = int(orders_info[order]['buy_created'])
                        time_passed = int(time.time()) - order_created

                        if time_passed > BUY_LIFE_TIME_SEC:
                            log.info("""Order {order} cancel, time {passed:0.1f} sec.""".format(
                                order=order, passed=time_passed
                            ))
                            # cancel order
                            cancel = bot.cancelOrder(
                                symbol=orders_info[order]['order_pair'],
                                orderId=order
                            )
                            # update DB
                            if 'orderId' in cancel:

                                log.info(
                                    "Order {order} canceled successfully".format(order=order))
                                cursor.execute(
                                    """
                                      UPDATE orders
                                      SET
                                        buy_cancelled = datetime()
                                      WHERE
                                        buy_order_id = :buy_order_id
                                    """, {
                                        'buy_order_id': order
                                    }
                                )

                                conn.commit()
                            else:
                                log.warning(
                                    "Order dont cancel: {cancel}".format(cancel=cancel))
                    elif order_status == 'PARTIALLY_FILLED':
                        log.debug(
                            "Order {order} partly execute, waiting".format(order=order))

                if order_status == 'FILLED' and orders_info[order]['order_type'] == 'sell':
                    log.debug("Sell order {order} execute".format(
                        order=order
                    ))

                    cursor.execute(
                        """
                          UPDATE orders
                          SET
                            sell_finished = datetime()
                          WHERE
                            sell_order_id = :sell_order_id

                        """, {
                            'sell_order_id': order
                        }
                    )
                    conn.commit()

    except Exception as e:
        log.exception(e)
    finally:
        conn.close()
