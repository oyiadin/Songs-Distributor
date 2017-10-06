<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>数据管理</title>
</head>
<body>
  <a href="/add">添加新曲子</a>
  <a href="/del">删除曲子</a>
  <hr/>
  <h1>Pending / {{ pending.count() }} Total</h1>
  <ul>
    % for i in pending:
    <li>
      <a href="/song/{{ i['id'] }}">{{ i['id'] }} / {{ i['title'] }}</a>
    </li>
    % end
  </ul>
  <h1>Checked / {{ checked.count() }} Total</h1>
  <ul>
    % for i in checked:
    <li>
      <a href="/song/{{ i['id'] }}">{{ i['id'] }} / {{ i['title'] }}</a>
      &nbsp;&nbsp;
      <a href="{{ res }}/{{ id }}.mp3">点我听歌</a>
    </li>
    % end
  </ul>
</body>
</html>
