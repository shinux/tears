import os
import sys
import yaml
import pymongo
from os import listdir

from tears import basedir


client = pymongo.MongoClient("localhost", 27017)
db = client.tears
post_collection = db.posts
category_collection = db.categories
tag_collection = db.tags
about_collection = db.about
link_collection = db.link

basedir += '/source/'


def get_all_file(target='posts'):
    return [basedir + target + '/' + i for i in listdir(basedir + target)]


def generate_url(date, full_file_path):
    file_name = full_file_path.split('/')[-1].split('.')[0]
    return '/' + str(date.year) + '/' + str(date.month) + '/' + str(date.day) + '/' + file_name


def check_file():
    """check file then drop collection and insert into database"""
    posts = get_all_file('posts')
    for post in posts:
        with open(post, 'r') as stream:
            _stream = stream.read()
            if len(_stream.split('---', 1)) < 1:
                print('error on --- split between ')
                return False
            _dict = yaml.load(_stream.split('---', 1)[0])
            if '---' in _dict.get('title'):
                print('--- is not available in title')
                return False
            content = _stream.split('---', 1)[1]
            if not content.replace(' ', '').replace(' ', ''):
                print('content in {name} is blank'.format(name=stream.name))
                return False

    return True


# generate posts
def generate_posts():
    # TODO: better check the files and backup the old file then insert
    client.drop_database('tears')

    category_dict = {}
    tag_dict = {}

    posts = get_all_file('posts')
    if not posts:
        print('no post until now')
    else:
        for post in posts:
            with open(post, 'r') as stream:
                _stream = stream.read()
                _dict = yaml.load(_stream.split('---', 1)[0])
                _content = _stream.split('---', 1)[1]
                _dict.update({'content': _content})
                _dict.update({'url': generate_url(_dict.get('date'), stream.name)})
                post_id = post_collection.insert_one(_dict).inserted_id
                current_category = _dict.get('categories')
                if current_category:
                    if current_category in category_dict:
                        category_dict[current_category].append(post_id)
                    else:
                        category_dict[current_category] = [post_id]
                for i in _dict.get('tags', []):
                    if i in tag_dict:
                        tag_dict[i].append(post_id)
                    else:
                        tag_dict[i] = [post_id]
        # insert category and tag
        for key, item in category_dict.items():
            category_collection.insert_one({'name': key, 'posts': item})
        for key, item in tag_dict.items():
            tag_collection.insert_one({'name': key, 'posts': item})

    about = get_all_file('about')
    if not about:
        print('no about until now')
    else:
        with open(about[0], 'r') as stream:
            _stream = stream.read()
            about_collection.insert_one({'content': _stream})

    link = get_all_file('link')
    if not link:
        print('no link until now')
    else:
        with open(link[0], 'r') as stream:
            _stream = stream.read()
            link_collection.insert_one({'content': _stream})


def main():
    if len(sys.argv) < 2:
        valid = check_file()
        if valid:
            generate_posts()
        return
    if sys.argv[1] in ['-h', 'help', '-help']:
        print("""
        Tears command line:

        -i init -init : check if not exist initiate the source dictionary.

        -h help -hlep : show help

        -c create -create [file name]: create a post md file in /posts folder.

        -g generate -generate: generate blog insert markdown file into the mongo.

                """)
        return
    if sys.argv[1] in ['-i', 'init', '-init']:
        if not os.path.exists(basedir):
            os.makedirs(basedir + '/about')
            os.makedirs(basedir + '/link')
            os.makedirs(basedir + '/posts')
        return
    if sys.argv[1] in ['-c', 'create', '-create']:
        if len(sys.argv) < 2:
            print('you have not specify the post name')
            return
        else:
            file_name = sys.argv[2].split('.')[0] + '.md'
            if os.path.isfile(basedir + '/posts/' + file_name):
                print('{name} is already exist'.format(name=file_name))
                return
            else:
                open(basedir + '/posts/' + file_name, 'w+')
                print('file {name} generate successfully'.format(name=file_name))
                return
    if sys.argv[1] in ['-g', 'generate', '-generate']:
        valid = check_file()
        if valid:
            generate_posts()
        return

if __name__ == '__main__':
    main()
