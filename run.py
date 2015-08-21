from bottle import run, debug
from views import app
from bottle import TEMPLATE_PATH
from bottle.ext.mongo import MongoPlugin
from common import basedir


# Template location
TEMPLATE_PATH.append(basedir + "/templates")

# Database
plugin = MongoPlugin(uri='mongodb://127.0.0.1', db='tears', json_mongo=True)
app.install(plugin)

# Active debug
DEBUG = True
debug(DEBUG)

# Run WSGI server
run(app, host='localhost', port=8080, reloader=DEBUG)
