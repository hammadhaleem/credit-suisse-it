from exchange_layer import Exchange_layer, get_market_data_running
from algorithm_trader import algo_trader
from threading import Thread


stage = 2

layer = Exchange_layer()
if stage == 1 :
    team_uid = layer.send_setup_request()

if stage == 2 :
    market_data_thread = Thread(target=get_market_data_running, args=(layer, ))
    market_data_thread.start()

    algo_trader = Thread(target= algo_trader, args = (layer, ))
    algo_trader.start()
    algo_trader.join()

if __name__ == "__main__":
    print ("thread finished...exiting")
