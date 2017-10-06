from bottle import get, post, redirect, request, run, template
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
	get = request.forms.get
	try:
		if len(get('id')) != 4 or not get('id').isdigit(): raise Exception
		if not get('title'): raise Exception
		if not status in ('checked', 'pending'): raise Exception
	except:
		return '''illegal input
		please go back checking your input and submit again'''
	collection.update_many(
		{'id': get('_id')},
		{'$set': {
			'id': get('id'),
			'title': get('title'),
			'status': get('status'),
			'date': get('date)')}})
	redirect('/song/{0}'.format(get('id')))


if __name__ == '__main__':
	run(host=input('host: '), port=int(input('port: ')))
