<!DOCTYPE html>
<html>
<head>
  <title>{{ song['title'] }}</title>
  <style>.hidden { display: none; }</style>
</head>
<body>
  <form action="/post/song" method="POST">
    <ul>
      % for i in ('id', 'title', 'status', 'date'):
      <input class="hidden" type="text" name="_{{ i }}" value="{{ song[i] }}" />
      <li>{{ i }}: <input type="text" name="{{ i }}" value="{{ song[i] }}" /></li>
      % end
    </ul>
    <input type="submit" value="提交更改" />
  </form>
</body>
</html>