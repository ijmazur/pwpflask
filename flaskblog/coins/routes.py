from flask import render_template, request, Blueprint
from flaskblog.models import Post

coins = Blueprint('coins', __name__)


@coins.route("/btc")
def btc():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@coins.route("/doge")
def doge():
    return render_template('about.html', title='About')