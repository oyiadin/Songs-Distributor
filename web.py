from bottle import get, post, redirect, request, run, template
from pymongo import MongoClient
from config import *
from utils import *

collection = MongoClient()['SongsDistributor']['collection']


@get('/')
def index_page():
    checked = collection.find({'status': 'checked'}).sort([('id', 1)])
    pending = collection.find({'status': 'pending'}).sort([('id', 1)])
    return template(
        'index.tpl', checked=checked, pending=pending, res=RESOURCE_URL)

@get('/log')
def log_page():
	f = open('../log')
	log = f.read()
	f.close()
	return '<pre>{}</pre>'.format(log)

@get('/song/<id>')
def song_page(id):
    selected = collection.find_one({'id': id})
    return template('song.tpl', song=selected, res=RESOURCE_URL)

@get('/add')
def add_song():
    return template(
        'song.tpl',
        song={'id': '', 'title': '', 'status': '', 'date': '', 'comment': ''},
        res=RESOURCE_URL)

@get('/del')
def del_song():
    return template('del.tpl')

@post('/del')
def do_del():
    get = request.forms.getunicode
    if get('password') != PASSWORD:
        return 'wrong password, get out!'
    selected = collection.find_one({'id': get('id'), 'date': get('date')})
    if not selected:
        return 'no result, check your id  & date and try again'
    collection.remove({'id': get('id'), 'date': get('date')})
    return 'OK. <a href="/">Bring me home</a>'

@post('/post/song')
def song_handler():
    get = request.forms.getunicode
    if get('password') != PASSWORD:
        return 'wrong password, get out!'
    try:
        if not get('title') or not get('date'): raise Exception
        if not get('status') in ('checked', 'pending'): raise Exception
    except Exception:
        return '''illegal input
        please go back checking your input and submit again'''

    if collection.find({'id': get('_id')}).count():
        id = get('_id')
        collection.update_one(
            {'id': get('_id')},
            {'$set': {
                'title': get('title'),
                'status': get('status'),
                'date': get('date'),
                'comment': get('comment')}})
    else:
        id = gen_valid_id(collection)
        collection.insert_one({
            'id': id,
            'title': get('title'),
            'status': get('status'),
            'date': get('date'),
            'comment': get('comment')})
    redirect('/song/{0}'.format(id))


if __name__ == '__main__':
    run(host=HOST_WEB, port=PORT_WEB)
