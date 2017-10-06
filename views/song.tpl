<!DOCTYPE html>
<html>
<head>
  <title>{{ song['title'] }}</title>
</head>
<body>
  <form>
    <ul>
      % for i in ('id', 'title', 'status', 'date'):
      <li>{{ i }}: <input type="text" name="{{ song[i] }}" /></li>
      % end
    </ul>
  </form>
</body>
</html>