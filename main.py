from exchange_layer import Exchange_layer

stage = 2

layer = Exchange_layer()
if stage == 1 :
    team_uid = layer.send_setup_request()

if stage == 2 :
    while True :
        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0005',qty=10**6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0386', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0388', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='3988', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0001', qty=10 ** 6)

        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0005', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0386', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0388', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='3988', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0001', qty=10 ** 6)

        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0005', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0386', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0388', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='3988', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='sell', symbol='0001', qty=10 ** 6)

        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0005', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0386', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0388', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='3988', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0001', qty=10 ** 6)

        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0005', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0386', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0388', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='3988', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0001', qty=10 ** 6)

        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0005', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0386', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0388', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='3988', qty=10 ** 6)
        ret = layer.test_buy_sell_market(exchange_id=1, type='buy', symbol='0001', qty=10 ** 6)


    # uid = ret['id']
    # Exchange_layer.cancel_order(uid)