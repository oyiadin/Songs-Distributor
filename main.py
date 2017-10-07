import werobot
import re
import time
import datetime
from pymongo import MongoClient
from utils import *
from consts import *
from config import *
import tornado.ioloop
import tornado.web
from werobot.contrib.tornado import make_handler


robot = werobot.WeRoBot(token=TOKEN)
robot.config.update(HOST=HOST, PORT=PORT, SESSION_STORAGE=False)

client = MongoClient()
db = client['SongsDistributor']
collection = db['collection']

start_time = time.time()


def compile(middle='', precise=False):
    format = '.*?{0}.*?' if not precise else '^{0}$'
    return re.compile(format.format(middle), re.IGNORECASE)


@robot.subscribe
def subscribe_handler():
    return SUBSCRIBE + '\n\n' + SHORT_HELP


@robot.text
def text_handler(message):
    log(message)

    content_list = message.content.split()
    command = content_list[0]
    args = content_list[1:] if len(content_list) >= 2 else []

    if len(message.content) > 1024:
        return MESSAGE_TOO_LONG

    ##### wrong format handling #####
    # no space between command and argument
    for i in ALL_COMMANDS:
        if command.startswith(i) and command != i:
            args.insert(0, command.replace(i, ''))
            command = i
            break
    # input argument with symbol [ ] or 【 】 or 《 》 or “ ”
    for (n, i) in enumerate(args):
        for s in '[]【】《》“”':
            args[n] = args[n].replace(s, '')
    # input ID without beginnng with `play`
    if len(command) == 4 and command.isdigit() and \
        collection.find_one({"id": command}):
        args.insert(0, command)
        command = 'play'
    # input song-name without beginning with `play`
    if collection.find_one({
        'title': compile(middle=message.content, precise=True)}):
        args = [command + ' ' + ' '.join(args) if args else command]
        command = 'play'


    if command in CMD_HELP:
        if args:
            return TOO_MANY_ARGS
        return HELP

    elif command in CMD_ABOUT:
        if args:
            return TOO_MANY_ARGS
        return ABOUT

    elif command in CMD_PING:
        if args:
            return TOO_MANY_ARGS
        return PING

    elif command in CMD_ADD:
        if len(args) < 1:
            return NEED_MORE_ARGS
        arg = ' '.join(args)

        for i in ('_', '*'):
            if i in arg:
                return INVALID_SYMBOL.format(i)

        collection.insert_one({
            'id': gen_valid_id(collection),
            'title': arg,
            'status': 'pending',
            'date': datetime.datetime.fromtimestamp(
                time.time()).strftime('%Y-%m-%d'),
            'comment': '',
        })
        return ADDED

    elif command in CMD_LIST:
        if len(args) > 1:
            return TOO_MANY_ARGS
        
        page = args[0] if args else 1
        return gen_list_page(collection, 'checked', page)

    elif command in CMD_SEARCH:
        if len(args) < 1:
            return NEED_MORE_ARGS
        arg = ' '.join(args)

        selected_c = collection.find({
            'title': compile(arg), 'status': 'checked'})
        selected_p = collection.find({
            'title': compile(arg), 'status': 'pending'})
        if not selected_c.count() and not selected_p.count():
            return SEARCH_NO_SONG.format(arg)

        reply = SEARCH_HEADER

        for i in selected_c:
            reply += ('\n' + '{id} {title} ({comment})'.format(**i))
        if selected_p.count():
            for i in selected_p:
                reply += ('\n' + '*{id} {title} ({comment})'.format(**i))
            reply += ('\n' + SEARCH_TIP_FOR_PENDING)
        return reply

    elif command in CMD_PLAY:
        if len(args) < 1:
            return NEED_MORE_ARGS
        arg = ' '.join(args)

        if arg.isdigit():
            selected = collection.find({'id': arg, 'status': 'checked'})
        else:
            selected = collection.find({
                'title': compile(arg), 'status': 'checked'})

        for i in ('_', '*'):
            if i in arg:
                return INVALID_SYMBOL.format(i)

        if not selected.count():
            return NO_SONG
        elif selected.count() > 1:
            return TOO_MANY_SONGS + '\n' + '\n'.join([
                '{id} {title} ({comment})'.format(**i) for i in selected])

        selected = selected.next()
        return werobot.replies.MusicReply(
            message=message,
            title='{0} ({1})'.format(selected['title'], selected['comment']),
            description=SONG_DESCRIPTION.format(selected['id'], selected['date']),
            url='{0}/{1}.mp3'.format(RESOURCE_URL, selected['id']))

    elif command in CMD_STAT:
        if args:
            return TOO_MANY_ARGS

        return STAT.format(
            int(((time.time() - start_time) / (60*60*24.))*10)/10.,
            collection.count({'status': 'checked'}),
            collection.count({'status': 'pending'}))


if __name__ == '__main__':
    application = tornado.web.Application([
        (r"/", make_handler(robot)),
    ])
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
