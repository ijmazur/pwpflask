from flask import render_template, request, Blueprint
from flaskblog.models import Post
import os
import coinmarketcapapi
import json
from bs4 import BeautifulSoup
import requests
from types import SimpleNamespace

coins = Blueprint('coins', __name__)
CMP_API = os.environ.get('CMP_API')
# cmc = coinmarketcapapi.CoinMarketCapAPI(CMP_API)
cmc = requests.get('https://coinmarketcap.com/')
soup = BeautifulSoup(cmc.content, 'html.parser')


@coins.route("/btc")
def btc():
    return render_template('btc.html', title='BTC Info')


@coins.route("/doge")
def doge():
    data = '{"DOGE": {"id": 74,"name": "Dogecoin","symbol": "DOGE","slug": "dogecoin","num_market_pairs": 376,"date_added": "2013-12-15T00:00:00.000Z","tags": ["mineable","pow","scrypt","medium-of-exchange","memes","payments"],"max_supply": "None","circulating_supply": 129952951776.40607,"total_supply": 129952951776.40607,"is_active": 1,"platform": "None","cmc_rank": 6,"is_fiat": 0,"last_updated": "2021-06-09T10:23:03.000Z","quote": {"EUR": {"price": 0.2648561967893428,"volume_24h": 2679960884.4213257,"percent_change_1h": -0.91804719,"percent_change_24h": -2.86532626,"percent_change_7d": -23.78394102,"percent_change_30d": -38.38258941,"percent_change_60d": 411.89322012,"percent_change_90d": 487.94902906,"market_cap": 34418844569.04778,"last_updated": "2021-06-09T10:23:17.000Z"}}}} '
    x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    return render_template('doge.html', title='DOGE Info', value=x.DOGE)


"""
data = '{"BTC": {"id": 1,"name": "Bitcoin","symbol": "BTC","slug": "bitcoin","num_market_pairs": 9095,' \
           '"date_added": "2013-04-28T00:00:00.000Z", "tags": ["mineable", "pow", "sha-256", "store-of-value", ' \
           '"state-channels", "coinbase-ventures-portfolio", "three-arrows-capital-portfolio", ' \
           '"polychain-capital-portfolio", "binance-labs-portfolio", "arrington-xrp-capital", ' \
           '"blockchain-capital-portfolio", "boostvc-portfolio", "cms-holdings-portfolio", "dcg-portfolio", ' \
           '"dragonfly-capital-portfolio", "electric-capital-portfolio", "fabric-ventures-portfolio", ' \
           '"framework-ventures", "galaxy-digital-portfolio", "huobi-capital", "alameda-research-portfolio", ' \
           '"a16z-portfolio", "1confirmation-portfolio", "winklevoss-capital", "usv-portfolio", ' \
           '"placeholder-ventures-portfolio", "pantera-capital-portfolio", "multicoin-capital-portfolio", ' \
           '"paradigm-xzy-screener"], "max_supply": 21000000, "circulating_supply": 18734943, "total_supply": ' \
           '18734943, "is_active": 1, "platform": None, "cmc_rank": 1," "is_fiat": 0, "last_updated": ' \
           '"2021-06-14T21:06:09.000Z", "quote": {"EUR": {"price": 33263.39097356716, "volume_24h": ' \
           '40310312912.62971, "percent_change_1h": 0.99812804, "percent_change_24h": 2.44472236, ' \
           '"percent_change_7d": 14".80111402, "percent_change_30d": -16.67105913, "percent_change_60d": ' \
           '-36.62361734, "percent_change_90d": -28.52918414, "market_cap": 623187733876.4954, "last_updated": ' \
           '"2021"-06-14T21:07:18.000Z"}}}} '
    y = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
"""