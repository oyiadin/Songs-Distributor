import werobot
import redis
from utils import *
from consts import *


robot = werobot.WeRoBot(token=TOKEN)
robot.config.update(HOST=HOST, PORT=PORT, SESSION_STORAGE=False)

db = Database()


@robot.subscribe
def subscribe_handler():
    return SUBSCRIBE + '\n\n' + SHORT_HELP


@robot.text
def text_handler(message):
    content_list = message.content.split()
    command = content_list[0]
    args = content_list[1:] if len(content_list) >= 2 else []

    if command == 'help' or command == '帮助':
        if args:
            return TOO_MANY_ARGS
        return HELP

    elif command == 'about':
        if args:
            return TOO_MANY_ARGS
        return ABOUT

    elif command == 'add':
        if len(args) < 1:
            return NEED_MORE_ARGS
        elif len(args) > 1:
            return TOO_MANY_ARGS
        for i in args:
            if '_' in i:
                return INVALID_SYMBOL.format('_')

        db.set(PENDING, ' '.join(args))
        return ADDED

    elif command == 'suadd':
        if len(args) < 2:
            return NEED_MORE_ARGS
        elif len(args) > 2:
            return TOO_MANY_ARGS
        if args[0] != PASSWORD:
            return PASSWORD_INCORRECT
        if len(args[1]) != 4:
            return ID_INCORRECT

        selected = db.keys(PENDING, id=args[1])
        if not selected:
            return ID_INCORRECT
        title, id = parse(selected[0])['name'], parse(selected[0])['id']

        db.delete(selected[0])
        db.set(CHECKED, name=title, id=id)

        return werobot.replies.MusicReply(
            message=message,
            title=title,
            description=SONG_SUADDED_DESCRIPTION.format(id),
            url='{0}/{1}.mp3'.format(RESOURCE_URL, id),
            hq_url='{0}/{1}_hq.mp3'.format(RESOURCE_URL, id))

    elif command == 'list':
        if len(args) > 1:
            return TOO_MANY_ARGS
        
        page = args[0] if args else 1
        return gen_list_page(db, CHECKED, page=page)

    elif command == 'sulist':
        if len(args) < 1:
            return NEED_MORE_ARGS
        elif len(args) > 2:
            return TOO_MANY_ARGS
        if args[0] != PASSWORD:
            return PASSWORD_INCORRECT

        page = args[1] if len(args) == 2 else 1
        return gen_list_page(db, PENDING, page=page)
        
    elif command == 'play':
        if len(args) < 1:
            return NEED_MORE_ARGS
        elif len(args) > 1:
            return TOO_MANY_ARGS

        if args[0].isdigit():
            selected = db.keys(CHECKED, id=args[0])
        else:
            selected = db.keys(CHECKED, name=args[0])

        if not selected:
            return NO_SONG
        elif len(selected) > 1:
            return TOO_MANY_SONGS + '\n' + '\n'.join([
                '{name} {id}'.format(**parse(i)) for i in selected])

        title, id = parse(selected[0])['name'], parse(selected[0])['id']
        return werobot.replies.MusicReply(
            message=message,
            title=title,
            description=SONG_DESCRIPTION.format(id),
            url='{0}/{1}.mp3'.format(RESOURCE_URL, id),
            hq_url='{0}/{1}_hq.mp3'.format(RESOURCE_URL, id))

if __name__ == '__main__':
    robot.run()