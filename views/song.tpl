<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>{{ song['id'] }}/{{ song['title'] }} ({{ song['comment'] }})</title>
  <style>.hidden { display: none; }</style>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body>
  <a href='/'>Home</a>
  <a href="{{ res }}/{{ song['id'] }}.mp3">点我听歌</a>
  <hr />
  <form action="/post/song" method="POST" accept-charset="utf-8">
    <ul>
      % for i in ('title', 'comment', 'date'):
      <li>{{ i }}: <input type="text" name="{{ i }}" value="{{ song[i] }}" /></li>
      % end
      <li>status:
        <input type="radio" name="status" value="pending" {{'checked' if song['status']=='pending' else ''}} />pending
        <input type="radio" name="status" value="checked" {{'checked' if song['status']=='checked' else ''}} />checked
      </li>
    </ul>
    密码：<input type="text" name="password" />
    <input class="hidden" type="text" name="_id" value="{{ song['id'] }}" />
    <input type="submit" value="提交更改" />
  </form>
  <hr />
  <p>一些小说明：</p>
  <p>status 只能填 checked 或者 pending，有啥区别你们应该懂。</p>
  <p>title, comment, status, date 都是可以修改的，不过不要胡乱修改。</p>
  <p>comment 可以填一些补充信息，比如填上歌手</p>
</body>
</html>