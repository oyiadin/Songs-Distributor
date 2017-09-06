import random
import utils
import redis
from consts import *

__all__ = ['gen_valid_id', 'gen_list_page', 'parse', 'Database']


def gen_valid_id(db):
    def gen_id():
        _id = ''
        for i in range(4):
            _id += random.choice('0123456789')
        return _id

    id = gen_id()
    while db.keys('{0}_*_{1}'.format(PENDING, id)) or \
        db.keys('{0}_*_{1}'.format(CHECKED, id)):
        id = gen_id()

    return id


def gen_list_page(db, type, page=1):
    page = int(page)
    left = (page - 1) * 10
    right = left + 10

    all = db.keys(type)
    max_page = int((len(all)-1) / 10) + 1 if len(all) else 0
    if page > max_page:
        return PAGE_NOT_EXIST
    elif page < 1:
        return ARGS_INCORRECT

    header = '===== {0}/{1} =====\n'.format(page, max_page)
    selected = all[left:right]

    return header + '\n'.join([
        '{id} {name}'.format(**parse(i)) for i in selected])


def parse(key):
    _list = key.split('_')
    assert len(_list) == 4
    return {'name': _list[1], 'id': _list[2]}


class Database(redis.StrictRedis):
    def set(self, type, name, id=None, value=''):
        if not id:
            id = utils.gen_valid_id(self)
        return super().set('{0}_{1}_{2}_'.format(type, name, id), value)

    def keys(self, type, name='*', id='*'):
        return [i.decode('utf-8') \
            for i in super().keys('{0}_*{1}*_{2}_'.format(type, name, id))]
