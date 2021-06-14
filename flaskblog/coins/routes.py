from flask import render_template, request, Blueprint
from flaskblog.models import Post
import os
import coinmarketcapapi
import json
from types import SimpleNamespace

coins = Blueprint('coins', __name__)
cmc = coinmarketcapapi.CoinMarketCapAPI('64f799c2-1ea2-4b31-b23a-2f0e731203e8')


@coins.route("/btc")
def btc():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@coins.route("/doge")
def doge():
    data = '{"DOGE": {"id": 74,"name": "Dogecoin","symbol": "DOGE","slug": "dogecoin","num_market_pairs": 376,"date_added": "2013-12-15T00:00:00.000Z","tags": ["mineable","pow","scrypt","medium-of-exchange","memes","payments"],"max_supply": "None","circulating_supply": 129952951776.40607,"total_supply": 129952951776.40607,"is_active": 1,"platform": "None","cmc_rank": 6,"is_fiat": 0,"last_updated": "2021-06-09T10:23:03.000Z","quote": {"EUR": {"price": 0.2648561967893428,"volume_24h": 2679960884.4213257,"percent_change_1h": -0.91804719,"percent_change_24h": -2.86532626,"percent_change_7d": -23.78394102,"percent_change_30d": -38.38258941,"percent_change_60d": 411.89322012,"percent_change_90d": 487.94902906,"market_cap": 34418844569.04778,"last_updated": "2021-06-09T10:23:17.000Z"}}}}'
    x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

    print(x.DOGE.quote)
    return render_template('doge.html', title='DOGE Info', value=x.DOGE)