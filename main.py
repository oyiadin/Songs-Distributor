import werobot
import redis
import random


STR_SUBSCRIBE = '''你好，感谢你的关注！这是一个私人管理的公众号，旨在分享饶平县第二中学宿区的歌单。同时，我们随时欢迎大家为这个歌单添砖加瓦。
另外，我们几个维护者都是准大学生/准大二生，这段时间就会陆陆续续地离开家，开始忙碌起来。由于这个缘故，我们无法保证一直及时更新，只能不定期进行维护，敬请谅解哦~'''

STR_HELP = '''help: to get this help page
add [song-name]: to tell us something new
list [page-num]: to show you a list containing all the songs we have
play [song-name]: to play the specific song for you
about: about us
------------
set [song-id] [link] [password]: to set the right version of a song
list-pending [page] [password]: to show you a list of songs to be checked.'''

STR_ADDED = 'Thanks for your updating! We have already added it to our pending-list.'

STR_NEED_ARGS = 'Need more arguments! Type `help` for more information.'

STR_WRONG_PASSWORD = 'The command you required is the one needs password, and your password is incorrect.'

STR_ABOUT = '''We are a small group of people who wants to in memory of our 3 years in Raoping No.2 Middle School.
This robot was made by @oyiadin, based on WeRoBot and redis. Source-code lies here:
https://github.com/oyiadin/Songs-Distributor'''

STR_PAGE_NOT_EXIST = "I'm sorry but this page doesn't exist. Try a smaller number please."

PENDING = 'songPending'
CHECKED = 'songChecked'


token = input('token: ') or 'token_oyoy'
host = input('host: ') or '127.0.0.1'
password = input('password: ') or 'oyoy'

robot = werobot.WeRoBot(token=token)
robot.config.update(HOST=host, PORT=80)

db = redis.StrictRedis()


def gen_id():
    id = ''
    for i in range(5):
        id += random.choice('0123456789')
    return id

def dbSet(type, name, value=''):
    id = gen_id()
    while db.keys(type + '_' + '*' + '_' + id):
        id = gen_id()

    key = type + '_' + name + '_' + id

    db.set(key, value)
    return id


@robot.text
def textHandler(message):
    command = message.content.split()
    if command[0] == 'help':
        return STR_HELP

    elif command[0] == 'add':
        if len(command) >= 2:
            dbSet(PENDING, ' '.join(command[1:]))
            return STR_ADDED
        else:
            return STR_NEED_ARGS

    elif command[0] == 'about':
        if len(command) == 1:
            return STR_ABOUT
        else:
            return STR_NEED_ARGS

    elif command[0] in ('list', 'list-pending'):
        if command[0] == 'list-pending':
            if len(command) != 3:   return STR_NEED_ARGS
            elif command[2] != password:    return STR_WRONG_PASSWORD

        if len(command) == 1: command.append('1')
        left = (int(command[1])-1) * 10
        right = left+11
        db_type = CHECKED if command[0] == 'list' else PENDING
        keys = db.keys(db_type + '_*')
        if len(keys) < (int(command[1]*10-9)):
            return STR_PAGE_NOT_EXIST
        keys = keys[left:right]
        return '\n'.join(keys)

    elif command[0] == 'play':
        if len(command) >= 2:
            songs = db.keys(CHECKED + '_*' + command[1] + '*_*')
            if len(songs) == 1:
                return werobot.replies.MusicReply(
                    message=message,
                    title=songs[0].split('_')[1],
                    description='A song from @rpezmusic',
                    url=db.get(songs[0]))
            else:
                content = "I'm sorry but there is too many songs matched:\n"
                content += '\n'.join([i for i in songs])
                return content
        else:
            return STR_NEED_ARGS

    elif command[0] == 'set':
        if len(command) != 4:   return STR_NEED_ARGS
        elif command[3] != password:    return STR_WRONG_PASSWORD

        _, name, id = db.keys(PENDING + '_*_' + command[1])[0].split('_')
        db.delete('_'.join([_, name, id]))
        db.set('_'.join(CHECKED, name, id), command[2])

        return werobot.replies.MusicReply(
            message=message, title=name, description=id, url=command[2])


@robot.subscribe
def subscribeHandler():
    return STR_SUBSCRIBE + '\n' + STR_HELP


try:
    robot.run()
except KeyboardInterrupt as e:
    print('Closing datebase..')
    PENDING.close()
    CHECKED.close()
    raise e