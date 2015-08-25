import os
import json
from bottle import Bottle
from bottle import jinja2_template as template
from bottle import TEMPLATE_PATH
from bottle import route, get, redirect, post, request, static_file, error, response
from bottle.ext.mongo import MongoPlugin
from bson.json_util import dumps


app = Bottle()


# Basedir
basedir = os.path.abspath(os.path.dirname(__file__))

# Template location
TEMPLATE_PATH.append(basedir + "/templates")

# Database
plugin = MongoPlugin(uri='mongodb://127.0.0.1', db='tears', json_mongo=True)
app.install(plugin)


@app.route('/')
@app.route('/index')
def index():
    return template('index.html', name=[{'sdf':'ss', 'title': 'douniwan'}])


@app.route('/posts/:post/', name='posts')
def posts(post):
    pass


@app.route('/static/<filetype>/<filename>')
def serve_static(filetype, filename):
    return static_file(filename, root=basedir + '/static/' + filetype)


@app.error(404)
def error404(error):
    return 'Nothing here, sorry'


if __name__ == '__main__':
    from bottle import run, debug

    # Active debug
    DEBUG = True
    debug(DEBUG)

    # Run WSGI web-server
    run(app, host='localhost', port=8080, reloader=DEBUG)
