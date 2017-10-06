<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>{{ song['id'] }}/{{ song['title'] }}</title>
  <style>.hidden { display: none; }</style>
</head>
<body>
  <a href=''>Home</a>
  <a href="{{ res }}/{{ id }}.mp3">点我听歌</a>
  <hr />
  <form action="/post/song" method="POST" accept-charset="utf-8">
    <ul>
      % for i in ('title', 'status', 'date'):
      <li>{{ i }}: <input type="text" name="{{ i }}" value="{{ song[i] }}" /></li>
      % end
    </ul>
    密码：<input type="text" name="password" />
    <input class="hidden" type="text" name="_id" value="{{ song['id'] }}" />
    <input type="submit" value="提交更改" />
  </form>
  <hr />
  <p>一些小说明：</p>
  <p>status 只能填 checked 或者 pending，有啥区别你们应该懂。</p>
  <p>title, status, date 都是可以修改的，不过不要胡乱修改。</p>
  <p>
</body>
</html>