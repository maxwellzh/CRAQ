### 处理QQ聊天记录

#### 介绍

检索出某段时间内聊天记录内某关键词出现次数，及每个发言成员发言中出现该词次数.

开发环境 Python `3.6.7`

目前仅支持`.txt`文本格式，使用帮助

```
$ .\search.exe -h

Version: 20190527

Usage:
  search.exe -i <input file> [options] [...]

General Options:
  -i, --input_loc <path>        Location of input file.
  -o, --output_loc <path>       Location of output file.
  -k, --key_word <string>       The key word to search.
  -c, --count_enable            Enable count of messages.
  -h, --help                    Show this info.

Notice: if there is only '-i' option, program would run on menu mode.
        (which is more suggested and flexible.)

For more help, visit
https://github.com/maxwellzh/CRAQ/blob/master/README.md

```
- `-i`指定输入文件位置，除打印帮助信息外为必须选项；只有该选项时会进入菜单模式
- `-o`指定输出文件位置，将处理后文本信息输出到指定文件中，若文件不存在则会新建，**文件已存在会覆盖！**
- `-k`关键词检索， 若搜索内容包含特殊字符（例如`@`、` `（空格）等），可用英文标点的单引号将关键词括起来（如`'<key word>'`）
- `-c在本地的记录中进行统计，将会输出所有发言人发言数统计结果。



菜单模式

```
$ .\search.exe -i .\group\talk.txt

2019-5-14:2019-5-26期间检索到消息记录26392条
Search modes support:
1. Search all chatting history.
   usage: -a
2. Search chatting history specify by a key word or time duration.
   usage: -k <key word> -t <time> [<time end>]
   example: -k beauty -t 2019-5-26
            -k beauty -t 2019-5-16:end
Exit: exit<Enter>

Notice: once detect '-a', all others args except 'exit' would be ignored.
        <time> foamat: <year>-<month>-<day>.
        you can add a '-o' arg to print messages to console in any mode.

>
```



#### 使用示例

##### 简单模式

```
$ .\search.exe -i .\talk.txt -k 日本

2019-5-14:2019-5-26期间检索到消息记录26392条

2019-5-14:2019-5-26期间检索到关键词"日本"232次

发送次数|                                                            |用户名
--------|                                                            |----------
48      |····························································|xxx
40      |··················································          |xxx
36      |·············································               |xxx
22      |···························                                 |xxx
18      |······················                                      |xxx
15      |··················                                          |xxx
14      |·················                                           |xxx
11      |·············                                               |xxx
5       |······                                                      |xxx
5       |······                                                      |xxx
4       |·····                                                       |xxx
3       |···                                                         |xxx
2       |··                                                          |xxx
2       |··                                                          |xxx
2       |··                                                          |xxx
2       |··                                                          |xxx
1       |·                                                           |xxx
1       |·                                                           |xxx
1       |·                                                           |xxx
```

右侧“xxx”表示用户ID名称，此处出于隐私考虑替换



##### 菜单模式

```
>-k 日本 -t 2019-5-20:end

2019-5-20:2019-5-26期间检索到关键词"日本"55次

发送次数|                                                            |用户名
--------|                                                            |----------
10      |····························································|xxx
9       |······················································      |xxx
8       |················································            |xxx
8       |················································            |xxx
5       |······························                              |xxx
3       |··················                                          |xxx
3       |··················                                          |xxx
2       |············                                                |xxx
2       |············                                                |xxx
2       |············                                                |xxx
1       |······                                                      |xxx
1       |······                                                      |xxx
1       |······                                                      |xxx


Press Enter to continue
```



#### To do

- [ ] 制作GUI
- [ ] 完善统计后可将消息打印输出功能



#### P.S

如何导出QQ聊天记录：**QQ/Tim PC客户端**

1. 打开任意聊天界面
2. - **Tim：**输入文本框右上角点击“消息管理”，再选择”消息管理器“
   - **QQ：** 将鼠标指针移动至输入文本框右上角”···“处，选择”消息管理器“
4. 列表内右击群组/个人，选择“导出消息聊天记录”
5. 保存为`.txt`格式