<!DOCTYPE html>
<html>
<head>
  <title>数据管理</title>
</head>
<body>
  <h1>Pending</h1>
  <ul>
  % for i in pending:
    <li><a href="/song/{{ i['id'] }}">{{ i['id'] }} / {{ i['title'] }}</a></li>
  % end
  </ul>
  <h1>Checked</h1>
  <ul>
  % for i in checked:
    <li><a href="/song/{{ i['id'] }}">{{ i['id'] }} / {{ i['title'] }}</a></li>
  % end
  </ul>
</body>
</html>
