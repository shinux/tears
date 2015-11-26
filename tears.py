import os
import json
import pymongo
import markdown2
from functools import partial
from bottle import Bottle
from bottle import jinja2_template
from bottle import TEMPLATE_PATH
from bottle import route, get, redirect, post, request, static_file, error, response, abort
from bottle.ext.mongo import MongoPlugin
from bson.objectid import ObjectId
from bson.json_util import dumps


app = Bottle()


# Basedir
basedir = os.path.abspath(os.path.dirname(__file__))

# Template location
TEMPLATE_PATH.append(basedir + "/templates")

###############################################################################
# filters ######################################################################
###############################################################################


def datetime_to_date(datetime):
    return str(datetime)[:10]


def markdown(string):
    return markdown2.markdown(string, extras=["fenced-code-blocks"])


def generate_post_url():
    return

# Template filter and setting
template_settings = dict(filters={"datetime_to_date": datetime_to_date,
                                  "markdown": markdown})
template = partial(jinja2_template, template_settings=template_settings)

# Database
plugin = MongoPlugin(uri='mongodb://127.0.0.1', db='tears', json_mongo=True)
app.install(plugin)

client = pymongo.MongoClient("localhost", 27017)
db = client.tears


###############################################################################
# core #########################################################################
###############################################################################

@app.route('/static/:filename#.*#')
def serve_static(filename):
     return static_file(filename, root='./static/')


@app.error(404)
def error404(error):
    return template('error.html')


@app.error(500)
def error500(error):
    return template('error.html')


@app.route('/')
@app.route('/index')
@app.route('/posts/<page_num:int>')
def index(page_num=1):
    page_size = 5
    post_list = []
    for p in db.posts.find().sort("date", -1):
        post_list.append(p)
    if len(post_list) % page_size == 0 and post_list:
        total = len(post_list) // page_size
    else:
        total = len(post_list) // page_size + 1
    if page_num > total:
        abort(404, "No such database.")
    final_list = post_list[(page_num - 1) * page_size: page_num * page_size]
    return template('index.html',
                    posts=final_list,
                    page_num=page_num,
                    total=total,
                    earlier=page_num + 1,
                    later=page_num - 1)


@app.route('/post/<year>/<month>/<day>/<name>')
def posts(year, month, day, name):
    url = '/' + year + '/' + month + '/' + day + '/' + name
    current_post = db.posts.find_one({'url': url})
    print(url)
    return template('post.html',
                    post=current_post,
                    )


@app.route('/archive')
def archive():
    final_dict = {}
    for p in db.posts.find().sort("date", -1):
        year = p.get('date').year
        if year in final_dict:
            final_dict[year].append({'url': p.get('url'), 'title': p.get('title')})
        else:
            final_dict[year] = []
            final_dict[year].append({'url': p.get('url'), 'title': p.get('title')})
    total = db.posts.find().count()
    years = len(final_dict)
    time_line_height = 50 * total + 75 * years
    return template('archive.html', archives=final_dict, height=time_line_height)


@app.route('/tag/<tag_name>')
def tag(tag_name):
    pass


@app.route('/category/<category_name>')
def category(category_name):
    current_category = db.categories.find_one({'name': category_name})
    ids = current_category.get('posts')
    post_list = []
    for p in db.posts.find({"_id": {"$in": ids}}).sort("date", -1):
        post_list.append(p)
    return template('category.html', posts=post_list, category_name=category_name)


@app.route('/about')
def about():
    _about = db.about.find_one()
    if _about:
        return template('about.html', about=_about)
    else:
        return template('about.html')


@app.route('/link')
def link():
    _link = db.link.find_one()
    if _link:
        return template('link.html', link=_link)
    else:
        return template('link.html')


if __name__ == '__main__':
    from bottle import run, debug

    # Active debug
    DEBUG = True
    debug(DEBUG)

    # Run WSGI web-server
    run(app, host='localhost', port=8080, reloader=DEBUG)
