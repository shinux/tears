import json
from bottle import Bottle
from bottle import route, get, redirect, post, request, static_file, error, response
from bottle import jinja2_template as template
from common import basedir
from bson.json_util import dumps


app = Bottle()


@app.route('/')
@app.route('/index')
def index():
    return template('index.html')
