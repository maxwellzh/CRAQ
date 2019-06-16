### 处理QQ聊天记录

#### 介绍

检索出某段时间内聊天记录内某关键词出现次数，及每个发言成员发言中出现该词次数.

开发环境 Python `3.7.3`

目前仅支持`.txt`文本格式，使用帮助

```
$ .\search.exe -h

发布版本：20190615
使用方式：
    search.exe -i <input file> [options] [...]

可用选项：
    -i, --infile <path>             指定输入文件位置，只添加-i参数时进入菜单模式（推荐）.
    -o, --outfile <path>            指定输出文件位置.
    -k, --kwd <key word>            指定关键词，不与-r同时使用.
    -r, --regular <pattern>         使用正则表达式搜索，不与-k同时使用.
    -c, --count                     消息统计.
    -h, --help                      展示帮助信息（本信息）.

使用示例：
    search.exe -i chatting.txt

获取更详细帮助信息，请访问项目：
https://github.com/maxwellzh/CRAQ/blob/master/README.md

```
- `-i`指定输入文件位置，除打印帮助信息外为必须选项；只有该选项时会进入菜单模式；可使用`+`连接多个文件同时处理，如

  ```
  $ search.exe -i .\file1.txt+.\file2.txt
  ```

  

- `-o`指定输出文件位置，将处理后文本信息输出到指定文件中，若文件不存在则会新建，**文件已存在会覆盖！**

- `-k`关键词检索， 若搜索内容包含特殊字符（例如`@`、` `（空格）等），可用英文标点的双引号将关键词括起来（如`"<key word>"`）

- `-c`在本地的记录中进行统计，将会输出所有发言人发言数统计结果。

- `-r`使用[正则表达式](https://docs.python.org/zh-cn/3/howto/regex.html#regex-howto)搜索



菜单模式

```
$ .\search.exe -i .\talk.txt
2019-5-14:2019-5-26期间检索到消息记录26697条

检索方式：
    [options] <argument> [...]
可用选项：
    -t, --time                      在所指定日期范围内搜索，时间格式示例：190611
        <date begin>[:<date end>]   可用beg代表记录中开始时间，end代表记录结束时间.
    -k, --kwd <key word>            指定关键词，不可与-r共同使用.
    -a, --all                       统计所有信息，会覆盖其他参数（-k -t）.
    -m, --member                    按照成员发言数输出（默认为按日期输出）.
    -r, --regular <pattern>         使用正则表达式搜索，不可与-k共同使用.
    -d, --detail                    添加可输出详细信息.
    -n, --name <name>               查询特定用户发言
    -e, --exit                      退出（或ctrl+c）.

示例：
    -k 你们 -t end-6:end -n 飞翔的企鹅 -d
    表示在最近1周内查询用户“飞翔的企鹅”包含“你们”的发言，并输出
>
```

* `-t`参数支持`beg`和`end`表示开始和结束日期，也可以使用相对时间表示，以下用法都是被接受的：

  ```
  >-t beg:end
  >-t beg
  >-t 190520:end
  >-t end-30:end
  >-t 190510:190510+10
  ```

  

#### 使用示例

##### 简单模式

```
$ .\search.exe -i .\talk.txt -k 日本

2019-5-14:2019-5-26期间检索到消息记录26392条

|2019-5-14:2019-5-26期间检索到关键词'日本'232次
|------------------------------------------------------------|次数|用户名
|############################################################|48  |xxx
|          ##################################################|40  |xxx
|               #############################################|36  |xxx
|                                 ###########################|22  |xxx
|                                      ######################|18  |xxx
|                                          ##################|15  |xxx
|                                           #################|14  |xxx
|                                               #############|11  |xxx
|                                                      ######|5   |xxx
|                                                      ######|5   |xxx
|                                                       #####|4   |xxx
|                                                         ###|3   |xxx
|                                                          ##|2   |xxx
|                                                          ##|2   |xxx
|                                                          ##|2   |xxx
|                                                          ##|2   |xxx
|                                                           #|1   |xxx
|                                                           #|1   |xxx
|                                                           #|1   |xxx
```

右侧“xxx”表示用户ID名称，此处出于隐私考虑替换



##### 菜单模式
默认按时间轴显示
```
>-k 日本 -t 2019-5-14:end
|------------------------------------------------------------|   日期   |次数
|                                                     #######|2019-05-14|8
|                                    ########################|2019-05-15|25
|     #######################################################|2019-05-16|56
|                                                          ##|2019-05-17|3
|############################################################|2019-05-18|61
|                                     #######################|2019-05-19|24
|                                                ############|2019-05-20|13
|                                                           #|2019-05-21|2
|                                                   #########|2019-05-22|10
|                                                      ######|2019-05-23|7
|                                                ############|2019-05-24|13
|                                                   #########|2019-05-25|10
|                                                            |2019-05-26|0

Press Enter to continue
```

添加参数`-m`后按成员显示
```
>-k 日本 -t 2019-5-14:end -m

|2019-5-14:2019-5-26期间检索到关键词'日本'232次
|------------------------------------------------------------|次数|用户名
|############################################################|48  |xxx
|          ##################################################|40  |xxx
|               #############################################|36  |xxx
|                                 ###########################|22  |xxx
|                                      ######################|18  |xxx
|                                          ##################|15  |xxx
|                                           #################|14  |xxx
|                                               #############|11  |xxx
|                                                      ######|5   |xxx
|                                                      ######|5   |xxx
|                                                       #####|4   |xxx
|                                                         ###|3   |xxx
|                                                          ##|2   |xxx
|                                                          ##|2   |xxx
|                                                          ##|2   |xxx
|                                                          ##|2   |xxx
|                                                           #|1   |xxx
|                                                           #|1   |xxx
|                                                           #|1   |xxx


Press Enter to continue
```

使用正则表达式搜索示例（搜索任意长度为6的数字）

```
>-r \d{6}
==================================================
xxx<ID>[24]
==================================================
xxx<ID>[30]
==================================================
xxx<ID>[42]
==================================================
xxx<ID>[6]
==================================================
xxx<ID>[18]
==================================================
```

输出详细信息

```
>-r \d{6} -d
==================================================
xxx<ID>[18]
==================================================
2019-05-16 22:13:38
...

2019-05-25 21:32:41
...

2019-05-25 22:46:15
...


==================================================
xxx<ID>[12]
==================================================
2019-05-25 00:32:48
...

2019-05-25 14:18:32
...


==================================================
xxx<ID>[18]
==================================================
2019-05-21 11:10:19
...

2019-05-23 23:32:34
...

2019-05-23 23:35:15
...


==================================================
xxx<ID>[6]
==================================================
2019-05-25 14:41:35
...
```

`...`为具体的消息，出于隐私考虑此处替换

#### To do

- [ ] 制作GUI
- [x] 添加正则表达式搜索
- [ ] 如何让代码更优雅



#### P.S

如何导出QQ聊天记录：**QQ/Tim PC客户端**

1. 打开任意聊天界面
2. - **TIM：**输入文本框右上角点击“消息管理”，再选择”消息管理器“
   - **QQ：** 将鼠标指针移动至输入文本框右上角”···“处，选择”消息管理器“
4. 列表内右击群组/个人，选择“导出消息聊天记录”
5. 保存为`.txt`格式