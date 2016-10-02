from time import sleep

from exchange_layer import Exchange_layer, get_market_data_running, minutes
from algorithm_trader import algo_trader
from threading import Thread

stage = 2

layer = Exchange_layer()

# try:
#     print("Start Test")
#     # Pass all tests
#     try:
#         team_uid = layer.send_setup_request()
#     except Exception as e:
#         print("Err", e)
#         pass  # team exist
#
#     order = layer.buy_sell_market(1, 'buy', '0005', 10)
#     print(order)
#     sleep(2)
#
#     order = layer.buy_sell_market(1, 'sell', '0005', 5)
#     print(order)
#
#     sleep(2)
#
#     order = layer.buy_sell_limit(1, 'buy', '0005', 5, 1)
#     print(order)
#
#     sleep(2)
#
#     print(layer.cancel_order(uid=order['id'], exchange_id=1))
#
#     sleep(2)
#     order = layer.buy_sell_limit(1, 'sell', '0005', 1, 1)
#     print(order)
#
#     sleep(2)
#     stage += 1
#
#     print("Completed Tests")
# except Exception as e:
#     print("Exception: ", e)
#     pass

market_data_thread = Thread(target=get_market_data_running, args=(layer,))
market_data_thread.start()

algo_trader = Thread(target=algo_trader, args=(layer, 0.25 * minutes))
algo_trader.start()

algo_trader.join()
market_data_thread.join()
