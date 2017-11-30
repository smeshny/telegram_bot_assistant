from coinmarketcap import Market


def get_markets(exchange):
    try:
        coinmarketcap = Market()
    except:
        return 'Неполадки на сервере coinmarketcap'
    get_m = coinmarketcap.ticker(limit=900, convert='USD')
    for i in get_m:
        if i['symbol'] == exchange.upper():
            return "*" + i['name'] + ':*' + '\n' + \
                   'USD price: ' + i['price_usd'] + '\n' + \
                   'BTC price: ' + i['price_btc'] + '\n' + \
                   'Change 1h: ' + i['percent_change_1h'] + '%' + '\n' + \
                   'Change 24h: ' + i['percent_change_24h'] + '%' + '\n' + \
                   'Change 7d: ' + i['percent_change_7d'] + '%' + '\n' + \
                   '24H Volume: ' + str(round(float(i['24h_volume_usd']) / 1000000000, 3)) + ' B' + '\n' + \
                   'Market cap USD: ' + str(round(float(i['market_cap_usd']) / 1000000000, 3)) + ' B' + '\n'
        else:
            continue
    return 'Такой команды или валюты нету'


def get_market():
    try:
        coinmarketcap = Market()
    except:
        return 'Неполадки на сервере coinmarketcap'
    request = coinmarketcap.stats()
    return '*Market Cap:* ' + str(round(request['total_market_cap_usd'] / 1000000000, 3)) + ' B' + '\n' + \
           '24h Vol: ' + str(round(request['total_24h_volume_usd'] / 1000000000, 3)) + ' B' + '\n' + \
           'BTC Dominance: ' + str(round(request['bitcoin_percentage_of_market_cap'], 2)) + '%' + '\n' + \
           'Active currencies: ' + str(int(request['active_currencies']))


def get_market_cap():
    try:
        coinmarketcap = Market()
    except:
        return 'Неполадки на сервере coinmarketcap'
    request = coinmarketcap.stats()
    return 'Market Cap: ' + str(round(request['total_market_cap_usd'] / 1000000000, 3)) + ' B'


def bitcoin_usd():
    try:
        coinmarketcap = Market()
    except:
        return 'Неполадки на сервере coinmarketcap'
    get_m = coinmarketcap.ticker(limit=900, convert='USD')
    for i in get_m:
        if i['symbol'] == "BTC":
            return i['price_usd']
        else:
            continue
    return 'Такой команды или валюты нету'
