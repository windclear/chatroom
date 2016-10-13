from models.user import User
from models.message import Message
from routes import *
from routes.user import current_user
import json
import redis

main = Blueprint('chat', __name__)

red = redis.Redis(host='localhost', port=6379, db=0)

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


@main.route('/subscribe')
def subscribe():
    return Response(stream(), mimetype="text/event-stream")


@main.route('/')
def index_view():
    ms = Message.query.all()
    return render_template('index.html', messages=ms)


def current_time():
    return int(time.time())


@main.route('/chat/add', methods=['POST'])
def chat_add():
    cu = current_user()
    if cu is None:
        abort(401)
    msg = request.get_json()
    msg['user_id'] = cu.id
    m = Message(msg)
    m.save()
    r = {
        'name': m.user.username,
        'content': m.content,
        'channel': m.channel,
        'created_time': m.created_time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    message = json.dumps(r, ensure_ascii=False)
    print('debug', message)
    # 用 redis 发布消息
    red.publish(chat_channel, message)
    return 'OK'
