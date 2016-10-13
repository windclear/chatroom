from functools import wraps

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import jsonify
from flask import session
from flask import Response
# from flask import send_from_directory


# main = Blueprint('main', __name__)
#
#
# @main.route('/')
# def index():
#     return redirect(url_for('todo.index'))
