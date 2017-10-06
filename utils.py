import random
import time
import datetime
from consts import *

__all__ = ['gen_valid_id', 'gen_list_page', 'log']


def gen_valid_id(collection):
    def gen_id():
        _id = ''
        for i in range(4):
            _id += random.choice('0123456789')
        return _id

    id = gen_id()
    while collection.find_one({'id': id}):
        id = gen_id()

    return id


def gen_list_page(collection, status, page=1):
    page = int(page)
    left = (page - 1) * 15
    right = left + 15

    all = collection.find(
        {'status': status}, {'id': 1, 'title': 1}).sort([('id', 1)])
    max_page = int((all.count()-1) / 15) + 1 if all.count() else 0
    if page > max_page:
        return PAGE_NOT_EXIST
    elif page < 1:
        return ARGS_INCORRECT

    header = '===== {0}/{1} =====\n'.format(page, max_page)
    selected = all[left:right]

    return header + '\n'.join([
        '{id} {title}'.format(**i) for i in selected])

def log(m):
    with open('log', 'a') as f:
        if m.type == 'text': exp=m.content
        elif m.type == 'image': exp=m.img
        elif m.type == 'link': exp=';'.join([m.title, m.description, m.url])
        else: exp=str(dict(m))
        f.write(LOG.format(datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H-%M-%S'), m.source, m.type, exp))

def add_key(key, value):
    from pymongo import MongoClient
    collection = MongoClient()['SongsDistributor']['collection']
    for i in ('checked', 'pending'):
        collection.update_many({'status': i}, {'$set': {key: value}})
    print('ok')
