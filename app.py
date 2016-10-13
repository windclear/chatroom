from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models import db

# 这里 import 具体的 Model 类是为了给 migrate 用
# 如果不 import 那么无法迁移
# 这是 SQLAlchemy 的机制
from models.user import User
from models.message import Message

from routes.chat import main as routes_chat
from routes.user import main as routes_user

app = Flask(__name__)
manager = Manager(app)

db_path = 'todo'
secret_key = 'secret key'


def register_routes(app):
    """
    注册蓝图
    """
    app.register_blueprint(routes_chat)
    app.register_blueprint(routes_user, url_prefix='/user')


def configure_app():
    """
    配置app
    """
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}.sqlite'.format(db_path)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:37777/{}'.format(db_path)
    app.secret_key = secret_key
    db.init_app(app)
    register_routes(app)


def configured_app():
    """
    返回配置好的app实例
    """
    configure_app()
    return app


@manager.command
def server():
    """
    运行调试服务器的命令
    """
    app = configured_app()
    config = {
        'debug': True,
        'port': 3000,
        # host: 0.0.0.0,
    }
    app.run(**config)


def configure_manager():
    """
    配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_app()
    configure_manager()
    manager.run()
