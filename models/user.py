from . import ModelMixin
from . import db
import urllib, hashlib

class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    avatar = db.Column(db.String(256))

    messages = db.relationship('Message', backref="user")

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.avatar = self.random_avatar()

    def validate_login(self, u):
        return u is not None and u.username == self.username and u.password == self.password

    def valid(self):
        valid_username = User.query.filter_by(username=self.username).first() is None
        valid_username_len = len(self.username) >= 3
        valid_password_len = len(self.password) >= 3
        # valid_captcha = self.captcha == '3'
        msgs = []
        if not valid_username:
            message = '用户名已经存在'
            msgs.append(message)
        if not valid_username_len:
            message = '用户名长度必须大于等于 3'
            msgs.append(message)
        if not valid_password_len:
            message = '密码长度必须大于等于 3'
            msgs.append(message)
        # elif not valid_captcha:
        #     message = '验证码必须输入 3'
        #     msgs.append(message)
        status = valid_username and valid_username_len and valid_password_len
        return status, msgs

    def random_avatar(self):
        username = self.username.encode('utf-8')
        default = 'retro'
        size = 80
        gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(username.lower()).hexdigest() + "?"
        gravatar_url += 's={}&d={}'.format(size, default)
        return gravatar_url
