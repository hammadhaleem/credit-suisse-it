
def algo_trader(layer):
    if True:
        # ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0005', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0386', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0388', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='3988', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0001', qty=10 ** 3)

        # ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0005', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0386', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0388', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='3988', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0001', qty=10 ** 3)

        # ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0005', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0386', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0388', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='3988', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0001', qty=10 ** 3)

        # ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0005', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0386', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0388', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='3988', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0001', qty=10 ** 3)

        # ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0005', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0386', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0388', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='3988', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0001', qty=10 ** 3)

        # ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0005', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0386', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0388', qty=10 ** 3)
        # ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='3988', qty=10 ** 3)
        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0001', qty=10 ** 2)
        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0001', qty=10 ** 2)
        print("---",layer.get_market_data(exchange_id=1, stock_symbol='0001'))

