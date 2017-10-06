<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Del a song</title>
</head>
<body>
  <form action="/del" method="POST" accept-charset="utf-8">
    <p>Input the id and date of a song to delete it. Password required.</p>
    id: <input type="text" name="id" />
    date: <input type="text" name="date" />
    password: <input type="text" name="password" />
    <input type="submit" value="OK" />
  </form>
</body>
</html>
