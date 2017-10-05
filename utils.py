import random
import utils
from pymongo import MongoClient
from consts import *

__all__ = ['gen_valid_id', 'gen_list_page']


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

    all = collection.find({'status': status}, {'id': 1, 'title': 1}).sort({'id': 1})
    max_page = int((all.count()-1) / 15) + 1 if all.count() else 0
    if page > max_page:
        return PAGE_NOT_EXIST
    elif page < 1:
        return ARGS_INCORRECT

    header = '===== {0}/{1} =====\n'.format(page, max_page)
    selected = all[left:right]

    return header + '\n'.join([
        '{id} {title}'.format(**i) for i in selected])
