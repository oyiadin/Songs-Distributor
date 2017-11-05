<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>纯文本歌单</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body>
  <pre>
    ######## Pending: {{ pending.count }} total ########
    % for i in pending:
    {{ i['title'] }} - {{ i['comment'] }}
    % end
    <br><br>
    ######## Checked: {{ checked.count }} total ########
    % for i in checked:
    {{ i['title'] }} - {{ i['comment'] }}
    % end
  </pre>
</body>
</html>
