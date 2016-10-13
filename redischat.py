import flask
from flask import request
import redis
import time
import json
from flask import abort
from routes.user import current_user
from routes.user import main as routes_user
from models import db

'''
# 使用 gunicorn 启动
gunicorn --worker-class=gevent -t 9999 redischat:app
# 开启 debug 输出
gunicorn --log-level debug --worker-class=gevent -t 999 redis_chat81:app
# 把 gunicorn 输出写入到 gunicorn.log 文件中
gunicorn --log-level debug --access-logfile gunicorn.log --worker-class=gevent -t 999 redis_chat81:app
'''

# 连接上本机的 redis 服务器
# 所以要先打开 redis 服务器
red = redis.Redis(host='localhost', port=6379, db=0)
print('redis', red)

app = flask.Flask(__name__)
app.secret_key = 'key'

# 发布聊天广播的 redis 频道
chat_channel = 'chat'


def stream():
    '''
    监听 redis 广播并 sse 到客户端
    '''
    # 对每一个用户 创建一个[发布订阅]对象
    pubsub = red.pubsub()
    # 订阅广播频道
    pubsub.subscribe(chat_channel)
    # 监听订阅的广播
    for message in pubsub.listen():
        print(message)
        if message['type'] == 'message':
            data = message['data'].decode('utf-8')
            # 用 sse 返回给前端
            yield 'data: {}\n\n'.format(data)


@app.route('/subscribe')
def subscribe():
    return flask.Response(stream(), mimetype="text/event-stream")


@app.route('/')
def index_view():
    return flask.render_template('index.html')


def current_time():
    return int(time.time())


@app.route('/chat/add', methods=['POST'])
def chat_add():
    cu = current_user()
    if cu is None:
        abort(401)
    msg = request.get_json()
    msg.set('user_id', cu.id)
    m = Message(msg)
    m.save()
    r = {
        'name': m.user.username,
        'content': m.content,
        'channel': m.channel,
        'created_time': m.created_time,
    }
    message = json.dumps(r, ensure_ascii=False)
    print('debug', message)
    # 用 redis 发布消息
    red.publish(chat_channel, message)
    return 'OK'


if __name__ == '__main__':
    config = dict(
        debug=True,
    )
    app.run(**config)
