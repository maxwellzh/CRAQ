# QQ聊天记录消息文本搜索

## 介绍

检索出某段时间内聊天记录内某关键词出现次数，及每个发言成员发言中出现该词次数.

开发环境 Python `3.7.5`

目前仅支持`.txt`文本格式，使用帮助

```shell
$ .\search.exe -h
usage: search.py [-h] [-i in-file [in-file ...]] [-o out-file]
                 [-k KEYWORD | -r REGULAR | -c] [-v]

QQ消息文本搜索[20191116]

optional arguments:
  -h, --help            显示当前信息.
  -i in-file [in-file ...]
                        指定输入文件，只添加-i参数时进入菜单模式（推荐）.
  -o out-file           指定输出文件.
  -k KEYWORD            指定关键词，不与-r同时使用.
  -r REGULAR            使用正则表达式搜索，不与-k同时使用.
  -c, --count           消息统计.
  -v, --version         显示当前程序版本

获取更详细帮助信息：https://github.com/maxwellzh/CRAQ/blob/master/README.md
```

- `-i`指定输入文件位置，除打印帮助信息外为必须选项；只有该选项时会进入菜单模式；可使用` `（空格）连接多个文件或正则式同时处理，如

  ```shell
  $ search.exe -i .\file1.txt .\file2.txt
  $ search.exe -i *.txt
  ```

- `-o`指定输出文件位置，将处理后文本信息输出到指定文件中，若文件不存在则会新建，**文件已存在会覆盖！**

- `-k`关键词检索， 若搜索内容包含特殊字符（例如`@`、` `（空格）等），可用英文标点的双引号将关键词括起来（如`"<key word>"`）

- `-c`在本地的记录中进行统计，将会输出所有发言人发言数统计结果。

- `-r`使用[正则表达式](https://docs.python.org/zh-cn/3/howto/regex.html#regex-howto)搜索

### 菜单模式

```shell
$ .\search.exe -i .\talk.txt
                                                                                                                                                                   2019-8-4:2019-11-15期间检索到消息记录16141条

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

- `-t`参数支持`beg`和`end`表示开始和结束日期，也可以使用相对时间表示，以下用法都是被接受的：

  ```shell
  > -t beg:end
  > -t beg
  > -t 190520:end
  > -t end-30:end
  > -t 190510:190510+10
  ```

## 使用示例

### 简单模式

```shell
$ .\search.exe -i .\talk.txt -k 猪
                                                                                                                                                                   2019-8-4:2019-11-15期间检索到消息记录16141条

>2019-8-4:2019-11-15期间检索到关键词'猪'15次
|------------------------------------------------------------|次数|用户名
|############################################################|6   |xxx
|                                        ####################|2   |xxx
|                                        ####################|2   |xxx
|                                        ####################|2   |xxx
|                                        ####################|2   |xxx
|                                                  ##########|1   |xxx
```

右侧“xxx”表示用户ID名称，此处出于隐私考虑替换

### 菜单模式

默认按时间轴显示

```shell
> -k 猪 -t end-6:end
>2019-11-9:2019-11-15期间检索到关键词'猪'12次
|------------------------------------------------------------|   日期   |次数
|                                                            |2019-11-09|0
|                                                            |2019-11-10|0
|############################################################|2019-11-11|8
|                                             ###############|2019-11-12|2
|                                                            |2019-11-13|0
|                                             ###############|2019-11-14|2
|                                                            |2019-11-15|0
>  
```

添加参数`-m`后按成员显示

```shell
> -k 猪 -t beg:end -m
>2019-10-4:2019-11-15期间检索到关键词'猪'15次
|------------------------------------------------------------|次数|用户名
|############################################################|6   |xxx
|                                        ####################|2   |xxx
|                                        ####################|2   |xxx
|                                        ####################|2   |xxx
|                                        ####################|2   |xxx
|                                                  ##########|1   |xxx
>  
```

使用正则表达式搜索示例（搜索任意长度为6的数字并按照成员发言数输出）

```shell
> -r \d{6} -m
>2019-8-4:2019-11-15期间检索到正则式'\d{6}'33次
|------------------------------------------------------------|次数|用户名
|############################################################|10  |xxx
|                                    ########################|4   |xxx
|                                    ########################|4   |xxx
|                                    ########################|4   |xxx
|                                                ############|2   |xxx
|                                                ############|2   |xxx
|                                                ############|2   |xxx
|                                                      ######|1   |xxx
|                                                      ######|1   |xxx
|                                                      ######|1   |xxx
|                                                      ######|1   |xxx
|                                                      ######|1   |xxx
```

输出详细信息

```shell
> -r \d{6} -d
==================================================
xxx<123456789>[2]
==================================================
2019-11-11 01:01:48
...

==================================================
xxx<123456789>[4]
==================================================
2019-08-24 19:52:16
...

2019-11-01 20:44:14
...

2019-11-14 22:12:00
...


==================================================
xxx<123456789>[1]
==================================================
2019-08-18 01:34:03
...


==================================================
xxx<123456789>[1]
==================================================
2019-08-18 01:08:44
...


==================================================
xxx<123456789>[1]
==================================================
2019-11-13 22:41:01
...


==================================================
xxx<123456789>[2]
==================================================
2019-11-01 13:33:40
...

2019-11-11 21:32:35
...


==================================================
xxx<123456789>[1]
==================================================
2019-11-13 21:40:16
...
...
...
...
>  
```

`...`为具体的消息，出于隐私考虑此处替换

## To do

- [ ] 制作GUI
- [x] 添加正则表达式搜索
- [ ] 如何让代码更优雅
- [ ] ~~添加成员行为统计（按时间段）~~(已完成但需要matplotlib包打包后体积太大因此不打算在留master分支)

## P.S

如何导出QQ聊天记录：

### Windows

1. 打开任意聊天界面
2. - **TIM：** 输入文本框右上角点击“消息管理”，再选择”消息管理器“
   - **QQ：** 将鼠标指针移动至输入文本框右上角”···“处，选择”消息管理器“
3. 列表内右击群组/个人，选择“导出消息聊天记录”
4. 保存为`.txt`格式

### MacOS/Linux/Mobile OS

not support
