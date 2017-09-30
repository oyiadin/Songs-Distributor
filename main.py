import werobot
import re
from pymongo import MongoClient
from utils import *
from consts import *
from config import *


robot = werobot.WeRoBot(token=TOKEN)
robot.config.update(HOST=HOST, PORT=PORT, SESSION_STORAGE=False)

client = MongoClient()
db = client['SongsDistributor']
collection = db['collection']


def compile(middle='', precise=False):
    format = '.*?{0}.*?' if not precise else '{0}'
    return re.compile(format.format(middle), re.IGNORECASE)


@robot.subscribe
def subscribe_handler():
    return SUBSCRIBE + '\n\n' + SHORT_HELP


@robot.text
def text_handler(message):
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
            'title': compile(arg),
            'title': arg,
            'status': 'pending'})
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
            reply += ('\n' + '{id} {title}'.format(**i))
        if selected_p.count():
            for i in selected_p:
                reply += ('\n' + '*{id} {title}'.format(**i))
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
                '{id} {title}'.format(**i) for i in selected])

        selected = selected.next()
        return werobot.replies.MusicReply(
            message=message,
            title=selected['title'],
            description=SONG_DESCRIPTION.format(selected['id']),
            url='{0}/{1}.mp3'.format(RESOURCE_URL, selected['id']))

    elif command in ('suadd', 'sudel'):
        if len(args) < 2:
            return NEED_MORE_ARGS
        if args[0] != PASSWORD:
            return PASSWORD_INCORRECT
        if len(args[1]) != 4:
            return ID_INCORRECT

        reply = []
        invalids = []
        for i in args[1:]:
            selected = collection.find_one({'id': i, 'status': 'pending'})
            if not selected.count():
                invalids.append(ID_INCORRECT.format(i))
            else:
                title, id = selected['title'], selected['id']

                if command == 'sudel':
                    collection.remove({'id': id, 'status': 'pending'})
                    reply.append(SUDELETED.format(title, id))
                elif command == 'suadd':
                    collection.update_one(
                        filter={'id': id, 'status': 'pending'},
                        update={'$set': {'status': 'checked'}})
                    if len(args) == 2:
                        return werobot.replies.MusicReply(
                            message=message,
                            title=title,
                            description=SONG_SUADDED_DESCRIPTION.format(id),
                            url='{0}/{1}.mp3'.format(RESOURCE_URL, id))
                    else:
                        reply.append(SUADDED.format(title, id))
        return '\n'.join(reply) + '\n' + '\n'.join(invalids)

    elif command == 'sumv':
        if len(args) < 3:
            return NEED_MORE_ARGS
        if args[0] != PASSWORD:
            return PASSWORD_INCORRECT
        if len(args[1]) != 4:
            return ID_INCORRECT
        if len(args) > 3:
            args = [args[0], args[1], ' '.join(args[2:])]

        selected = collection.find_one({'id': args[1], 'status': 'pending'})
        if not selected.count():
            return NO_SONG
        title, id = selected['title'], selected['id']
        collection.replaceOne(
            filter={'id': args[1], 'status': 'pending'},
            replacement={'id': args[1], 'title': args[2], 'status': 'pending'})

        return RENAMED.format(id, args[2])

    elif command == 'sulist':
        if len(args) < 1:
            return NEED_MORE_ARGS
        elif len(args) > 2:
            return TOO_MANY_ARGS
        if args[0] != PASSWORD:
            return PASSWORD_INCORRECT

        page = args[1] if len(args) == 2 else 1
        return gen_list_page(collection, 'pending', page)


if __name__ == '__main__':
    robot.run()
