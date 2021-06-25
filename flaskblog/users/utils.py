import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


# random hex from secrets is a base for randomising name of picture, so it never hurts our db
# we save the file with same extension as its uploaded (os - needed for that)
# the filename.extension is split and we save the extension
# we need to use _, as variable not used in our application (f_name)
# we join the two in picture_fn = hexname + extension
# picture_path = root app(package directory) and static/profile_pics and we add te picture filename we created
# the picture cant be bigger than 125x125
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    # to delete previous profile pic, while adding new one
    # prev_picture = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
    # if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.jpg':
    #   os.remove(prev_picture)
    return picture_fn


# get_reset_token (main app models.py)
    # 1800 = 30minutes
    # into Serializer we pass in the secret_key
    # and we return token created with this serializer
    # we dump it with payload of userid, and we use our own self.id that the user resets
    # and we decode it with utf-8
# we send the email message from pwpumcsim@gmail.com with reset token
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, then simply ignore this email and no changes will be made.
'''
    mail.send(msg)