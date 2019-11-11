# search_movies
1，搜索结果只有一个：“绀青之拳”
（对比年份及片名，片名及年份 或 片名 一致即可 ）
2，搜索结果多个：“英雄本色”
匹配片名和年份，取二者相同的，若无年份时则取片名相同的。若无片名相同的，则继续下一个，直至循环完毕，若还是没有，则继续下一个影片（with open as f）
3，搜索结果多个 且 片名年份都一样： “花生酱猎鹰”
取第一个，接着继续下一轮循环
4，搜索结果一个也没有：“呵呵呵呵呵”
继续下一轮循环


## search_movie_6vdy.py

从 [6vdy电影网](http://www.hao6v.com/) 搜素影片，并返回对应链接。 第一个参数为影片名。

```shell

$python search_movie_6vdy.py 巴黎野玫瑰
Search result link: http://so.hao6v.com/e/search/result/?searchid=739478
Status code: 200
名称：经典高分剧情《巴黎野玫瑰》720p.BD中英双字 链接：http://so.hao6v.com/gq/2015-06-08/BLYMG.html

$python search_movie_6vdy.py 英雄本色
Search result link: http://so.hao6v.com/e/search/result/?searchid=739496
Status code: 200
名称：《中国刑警803英雄本色》全集 链接：http://so.hao6v.com/dlz/2018-10-27/32063.html
名称：2018动作剧情《英雄本色2018》720p.BD国语中字 链接：http://so.hao6v.com/dy/2018-01-28/YXBS2018.html
名称：经典动作《英雄本色3》720p.国粤双语.BD中字 链接：http://so.hao6v.com/gq/2011-06-17/15202.html
名称：经典动作《英雄本色2》720p.国粤双语.BD中字 链接：http://so.hao6v.com/gq/2011-06-15/15197.html
名称：经典动作《英雄本色》720p.国粤双语.BD中字 链接：http://so.hao6v.com/gq/2011-06-15/15196.html

```
