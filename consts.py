

########################################
#         Section of Constants         #
########################################


PENDING = 'pending'
CHECKED = 'checked'
TOKEN = 'token_here'
HOST = '0.0.0.0'
PORT = 80
PASSWORD = 'pw_no_blank'
RESOURCE_URL = 'http://example.com/songs'  # Mustn't end with '/'


########################################
#          Section of Messages         #
########################################


SUBSCRIBE = '''\
你好，感谢你的关注！这是一个私人管理的公众号，旨在分享饶平县第二中学宿区的歌单。同时，\
我们随时欢迎大家为这个歌单添砖加瓦。\n\n另外，由于我们几个维护者都是二中毕业生，这段时\
间忙于开学、军训，所以会暂停更新。请大家谅解哦~'''

HELP = '''\
=====================
help: 回复本帮助信息
add [歌名]: 反馈新歌
list [页数]: 查看现有歌单
play [歌名]: 播放指定歌单
about: 关于我们
=====================
suadd [密码] [歌曲ID]: 将待定歌曲添加到正式歌单
sulist [密码] [页数]: 查看待定歌曲列表
=====================
su 开头的命令正式发布时会隐藏，只有我们知道。'''

SHORT_HELP = '输入 help 可以获取帮助哦~'

ABOUT = '''\
# 我们是一个小团体，
# 怀念着曾在二中的日子。
# 成员名录：
橙小圆、淤青鸡、Gay Gay Way、Fish、瑞星、黄弟弟、草果
# 该号后台基于 WeRoBot、redis-py 等框架开发，源码见于：
https://github.com/oyiadin/Songs-Distributor'''

ADDED = '''\
感谢你的反馈 :)
我们找到资源后就会添加至歌单中~'''

NEED_MORE_ARGS = '参数不够。' + SHORT_HELP

TOO_MANY_ARGS = '参数过多。' + SHORT_HELP

INVALID_SYMBOL = "由于技术原因，歌名里不允许出现符号 {0}，请重试。"

ID_INCORRECT = '''\
你输入的歌曲ID错了，再检查一遍？
注意:歌曲ID均为4位数字，且0不可省略。'''

PASSWORD_INCORRECT = '密码错误，操作取消。'

ARGS_INCORRECT = '参数错误，不要调戏人家嘛~'

PAGE_NOT_EXIST = '该页不存在，可能你输入的页码太大了。换个小一点的数字试试？'

NO_SONG = '不好意思，我们没有找到这首歌，再检查一遍你输入的内容？'

TOO_MANY_SONGS = 'emm，请找出你想播放的歌曲所对应的ID，并输入 play 歌曲ID'

SONG_DESCRIPTION = '由 @二种旋律 所整理的二中宿区曲子'

SONG_SUADDED_DESCRIPTION = 'ID {0} 添加成功，请试听确认无误。'