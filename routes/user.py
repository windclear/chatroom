from models.user import User
from routes import *


main = Blueprint('user', __name__)

Model = User


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


@main.route('/login', methods=['GET', 'POST'])
def login():
    u = current_user()
    if u is not None:
        return redirect('/')
    method = request.method
    if method == 'GET':
        msgs = None
    elif method == 'POST':
        form = request.form
        u = User(form)
        user = User.query.filter_by(username=u.username).first()
        if user is not None and user.validate_login(u):
            session['user_id'] = user.id
            return redirect('/')
        else:
            msgs = ['用户名/密码错误']
    return render_template('login.html', message=msgs)


@main.route('/register', methods=['GET', 'POST'])
def register():
    u = current_user()
    if u is not None:
        return redirect('/')
    method = request.method
    if method == 'GET':
        msgs = None
    elif method == 'POST':
        form = request.form
        u = User(form)
        status, msgs = u.valid()
        if status:
            u.save()
            return redirect(url_for('.login'))
    return render_template('register.html', message=msgs)


@main.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')
