from bottle import get, post, run, template
from pymongo import MongoClient

collection = MongoClient()['SongsDistributor']['collection']


@get('/')
def index_page():
	checked = collection.find({'status': 'checked'})
	pending = collection.find({'status': 'pending'})
	return template('index.tpl', checked=checked, pending=pending)

@get('/song/<id>')
def song_page(id):
	selected = collection.find_one({'id': id})
	return template('song.tpl', song=selected)

@post('/post/song')
def song_handler():
	pass

if __name__ == '__main__':
	run(host=input('host: '), port=int(input('port: ')))
