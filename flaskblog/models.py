from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# importing from db.Model
# unique ID = column(type(int), primary_key=True (unique ID for our user)
# username = has to be a string of max 20, unique, and cant be nullable
# same for email and password, image_file
# posts attribute is = relationship to our Post model, backref = author, lazy = True
# backref is similar to adding another column to the Post Column, we get attribute who created the post
# lazy defines when sqlalchemy loads the data, True = it loads it in one go (we can get all posts created by
# individual user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    # 1800 = 30minutes
    # into Serializer we pass in the secret_key
    # and we return token created with this serializer
    # we dump it with payload of userid, and we use our own self.id that the user resets
    # and we decode it with utf-8
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # verification of the above token, we make a Serializer object with SECRET_KEY again
    # its in a try except block due to the possibility that token might be expired or invalid
    # we try to get user_id by loading token and we try to get user_id out of that (user_id comes through payload)
    # if we do get user_id without throwing exception, we return the user.
    # if this method does not use self, we need to @staticmethod - telling python not to expect self parameter as arg
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # dunder method (magic method) - how our object is printed, whenever we print it out.
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# same as above
# date_posted = DateTime and we default from datetime.utcnow (without ()) because it would mean we want default rn
# we want to pass the function as argument and not the date right now
# we need username who posted the post, we get a ForeignKey id of user who created the post
# in the User model we are referencing the actual Post class
# in the user.id ForeignKey we are referencing the tablename and columnname in the db
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
