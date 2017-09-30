CMD_HELP = ('help', '帮助'， '帮助信息')
CMD_ABOUT = ('about', '关于', '你是谁', '你们是谁')
CMD_PING = ('ping', '活着没', '活着吗')
CMD_ADD = ('add', '添加', '增加', '新增', '反馈')
CMD_LIST = ('list', '歌曲列表', '列表')
CMD_PLAY = ('play', '播放', '播放歌曲', '返回', '获取')
CMD_SEARCH = ('ss', 'search', '搜索', '查找', '寻找', '查询')

ALL_COMMANDS = CMD_HELP + CMD_ABOUT + CMD_PING + CMD_ADD + CMD_LIST + \
	CMD_PLAY + CMD_SEARCH

SUBSCRIBE = '''你好，感谢你的关注！这是一个私人管理的公众号，旨在分享饶平县第二中学\
宿区的歌单。同时，我们随时欢迎大家为这个歌单添砖加瓦~'''

HELP = '''\
可用命令：
=====================
添加 [歌名]: 反馈新歌
列表 [页数]: 查看现有歌单
播放 [歌名]: 播放指定歌曲
查找 [歌名]: 查看歌曲ID
帮助: 回复本帮助信息
关于: 关于我们
=====================
示例: 输入“播放《不要说话》”就可以播放这首歌曲了~'''

SU_HELP = '''\
=====================
sulist [密码] [页数]: 查看待定歌曲列表
suadd [密码] [ID1] [ID2] ...: 将待定歌曲添加到正式歌单
sudel [密码] [ID1] [ID2] ...: 将某歌曲从待定列表里移除
sumv [密码] [ID] [新曲名]: 为待定列表里的指定曲子更名
=====================
suadd, sudel 可一次性操作多首曲子'''

SHORT_HELP = '输入“帮助”可以获取帮助哦~'

ABOUT = '''\
# 我们是一个小团体，
# 怀念着曾在二中的日子。
# 成员名录：
橙小圆、淤青鸡、Gay Gay Way、Fish、瑞星、黄弟弟、草果
# 该号后台基于 WeRoBot、MongoDB 等框架开发，源码见于：
https://github.com/oyiadin/Songs-Distributor'''

ADDED = '''\
感谢你的反馈 :)
我们找到资源后就会添加至歌单中~'''

SUDELETED = '{1}《{0}》已从待定列表删除。'

SUADDED = '{1}《{0}》已移动到正式曲库。'

RENAMED = '《{0}》已成功更名为《{1}》。'

PING = '活着0w0'

SEARCH_NO_SONG = '''\
对不起，曲库里没找到这首歌。
你可以输入“添加 {0}”为我们反馈这首曲子。'''

SEARCH_HEADER = '找到如下曲子:'

SEARCH_TIP_FOR_PENDING = '注: 标*号的歌曲正在收录，请耐心等候'

NEED_MORE_ARGS = '参数不够。' + SHORT_HELP

TOO_MANY_ARGS = '参数过多。' + SHORT_HELP

INVALID_SYMBOL = "由于技术原因，歌名里不允许出现符号“{0}”，请重试。"

ID_INCORRECT = '找不到ID为{0}的曲子。'

PASSWORD_INCORRECT = '密码错误，操作取消。'

ARGS_INCORRECT = '参数错误，不要调戏人家嘛~'

PAGE_NOT_EXIST = '该页不存在，可能你输入的页码太大了。换个小一点的数字试试？'

NO_SONG = '找不到这首曲子，检查一下？'

TOO_MANY_SONGS = '''\
找到好多曲子呀，用“播放+ID”播放吧。
“+”号不用输入哦~'''

MESSAGE_TOO_LONG = '你输入的内容好长啊~ 我是不会理你的哟，哼~'

SONG_DESCRIPTION = '由@二中旋律 所整理的二中宿区曲子{0}'

SONG_SUADDED_DESCRIPTION = 'ID{0}添加成功，请试听确认无误。'