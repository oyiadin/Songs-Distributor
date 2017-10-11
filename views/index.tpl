<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>数据管理</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body>
  <a href="/add">添加新曲子</a>
  <a href="/del">删除曲子</a>
  <a href="/log">查看所有接收到的消息</a>
  <hr/>
  <h1>Pending / {{ pending.count() }} Total</h1>
  <ul>
    % for i in pending:
    <li>
      <a href="/song/{{ i['id'] }}">
        {{ i['id'] }} / {{ i['title'] }} ({{ i['comment'] }})
      </a>
    </li>
    % end
  </ul>
  <h1>Checked / {{ checked.count() }} Total</h1>
  <ul>
    % for i in checked:
    <li>
      <a href="/song/{{ i['id'] }}">
        {{ i['id'] }} / {{ i['title'] }} ({{ i['comment'] }})
      </a>
      &nbsp;&nbsp;
      <a href="{{ res }}/{{ i['id'] }}.mp3">点我听歌</a>
    </li>
    % end
  </ul>
</body>
</html>
