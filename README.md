### 处理QQ聊天记录

#### 介绍

检索出某段时间内聊天记录内某关键词出现次数，及每个发言成员发言中出现该词次数.

开发环境 Python `3.6.7`

目前仅支持`.txt`文本格式，使用方式

```
$ python .\chat_cal.py -h

Usage:
  python chat_cal.py -i <input file> [options] [...]

General Options:
  -i, --input_loc <path>        Location of input file.
  -o, --output_loc <path>       Location of output file.
  -k, --key_word <string>       The key word to search.
  -c, --count_enable            Enable count of messages.
  -h, --help                    Show this info.

Notice: if there is only '-i' option, program would run on menu mode.
        (which is more suggested and flexible.)

```
`-i`指定输入文件位置
`-o`指定输出文件位置
`-k`关键词检索
`-c`启用总消息记录

菜单模式

```
$ python chat_cal.py -i .\group\talk.txt

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
$python .\chat_cal.py -i .\talk.txt -k 日本

2019-5-14:2019-5-26期间检索到消息记录26392条

2019-5-14:2019-5-26期间检索到关键词"日本"232次

发送"日本"次数5   .....                                                 xxx
发送"日本"次数48  ..................................................    xxx
发送"日本"次数40  .........................................             xxx
发送"日本"次数1   .                                                     xxx
发送"日本"次数4   ....                                                  xxx
发送"日本"次数2   ..                                                    xxx
发送"日本"次数15  ...............                                       xxx
发送"日本"次数2   ..                                                    xxx
发送"日本"次数2   ..                                                    xxx
发送"日本"次数36  .....................................                 xxx
发送"日本"次数18  ..................                                    xxx
发送"日本"次数22  ......................                                xxx
发送"日本"次数11  ...........                                           xxx
发送"日本"次数3   ...                                                   xxx
发送"日本"次数1   .                                                     xxx
发送"日本"次数5   .....                                                 xxx
发送"日本"次数2   ..                                                    xxx
发送"日本"次数1   .                                                     xxx
发送"日本"次数14  ..............                                        xxx
```

右侧“xxx”表示用户ID名称，此处出于隐私考虑替换

##### 菜单模式

```
>-k 日本 -t 2019-5-20:end

2019-5-20:2019-5-26期间检索到关键词"日本"55次

发送"日本"次数3   ...............                                       xxx
发送"日本"次数8   ........................................              xxx
发送"日本"次数10  ..................................................    xxx
发送"日本"次数1   .....                                                 xxx
发送"日本"次数2   ..........                                            xxx
发送"日本"次数2   ..........                                            xxx
发送"日本"次数5   .........................                             xxx
发送"日本"次数1   .....                                                 xxx
发送"日本"次数9   .............................................         xxx
发送"日本"次数2   ..........                                            xxx
发送"日本"次数1   .....                                                 xxx
发送"日本"次数3   ...............                                       xxx
发送"日本"次数8   ........................................              xxx


Press Enter to continue
```



#### To do

- [ ] 添加整体/成员聊天消息数随时间增长图
- [ ] 制作GUI
- [ ] ~~统计词频时排除聊天记录中的@人名~~
- [ ] ~~将Time类型修改为datetime.dateime~~
- [ ] 完善功能

#### P.S

如何导出QQ聊天记录：

1. 打开任意对话框界面
2. 在输入文本框右上角点击“消息管理”旁下箭头
3. 选择“消息管理器”
4. 列表内右击群组/个人，选择“导出消息聊天记录”
5. 保存为`.txt`格式