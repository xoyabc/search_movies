<!--ts-->
* [search_movies 实现方法](#search_movies-实现方法)
* [Run in Docker](#run-in-docker)
* [search_movie_maccms.py](#search_movie_maccmspy)
* [search_movie_6vdy.py](#search_movie_6vdypy)

<!-- Added by: root, at: 2020-05-17T23:31+0800 -->

<!--te-->



## search_movies 实现方法

1，搜索结果只有一个：“绀青之拳”
（对比年份及片名，片名及年份 或 片名 一致即可 ）

2，搜索结果多个：“英雄本色”
匹配片名和年份，取二者相同的，若无年份时则取片名相同的。若无片名相同的，则继续下一个，直至循环完毕，若还是没有，则继续下一个影片（with open as f）

3，搜索结果多个 且 片名年份都一样： “花生酱猎鹰”

取第一个，接着继续下一轮循环，直至循环完毕，若还是没有，则继续下一个影片。最终片名即为最后匹配到的那个。

4，搜索结果一个也没有：“呵呵呵呵呵”
继续下一轮循环

5，豆瓣口碑榜排除院线片（上映距今未满 90 天）

```

根据片名搜  &  豆瓣每周口碑榜  &  新片(new)
1，结果数大于0
2，结果数等于0，提示未找到
3，结果数等于十，翻页(单独一个if，不要和大于0的if在一起，避免结果数小于9时，执行提取下一页链接try语句)


以下情况不发:
1，在中国大陆上映，未满15天的。
2，在中国大陆上映，已满15天，但视频网站(优酷/腾讯/爱奇艺/芒果TV/1905电影网/B站)未上线的。

不可发标准

当前:
在中国大陆上映，上映期未满90天。

存在问题:
上映期未满90天，但实际上视频网站已上线，此时可以发。(如影片《沉默的证人》)

改进:
再加一个不可播放(视频网站未上线)，即:在中国大陆上映，上映期未满90天，且不可播放(优爱腾等平台未上线)。

最后合为一个:
在中国大陆上映，不能播放(视频网站未上线)，上映未满90天。(1 and 2 and 3)


院线/非院线(在没在中国大陆上映)
```

## Run in Docker

```shell
docker pull xoyabc/search_movie

docker run -it -d --name search_movies xoyabc/search_movies:latest

docker exec -it search_movies /bin/bash
```

## search_movie_maccms.py

将片名贴入到 movie.name 中，执行 search_movie_maccms.py 即可，输出格式见下：
```plain
[片名][年份]
短链接
```

```shell
root@b0b3fd4693fe:/home/git/search_movies#  cat movie.name 
一九零零
天堂的孩子
安德烈·卢布廖夫
巴里·林登
芬妮与亚历山大
豹
阿拉伯的劳伦斯


python search_movie_maccms.py

*** 新片/经典 start ***
[一九零零][1976]
http://t.cn/Ai3sAGR7
[芬妮与亚历山大][1982]
http://t.cn/Ai3sAGR7
[阿拉伯的劳伦斯][1962]
http://t.cn/Ai3sAGR7
*** 新片/经典 end ***
```

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
