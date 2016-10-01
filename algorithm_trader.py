from time import sleep

from exchange_layer import df_from_sql


def algo_trader(layer,tradeFrequency):
    sleep(10)
    while True:
        query = "select * from stock_price_data order by time desc limit 5000;"
        df = df_from_sql(query)

        mask = ((df.exchange == '1') & (df.symbol =='0001'))

        df = df[mask]

        print(df.describe())

        print(
            "[Trade] Exchange: {exchange_id} {stock_symbol}".format(
                exchange_id=1,
                stock_symbol='0001'
            ),layer.get_market_data(exchange_id=1, stock_symbol='0001'))

        sleep(tradeFrequency)

