### 处理QQ聊天记录

#### 介绍

检索出聊天记录内某关键词出现次数，及每个发言成员发言中出现该词次数.

开发环境 Python `3.6.7`

目前仅支持`.txt`文本格式，使用方式

```
$python .\chat_cal.py -h
usage:
python ./chat_cal.py [-i file_i | -o file_o | -k word | -c]

-i[--file_input_loc]            location of input file
-o[--file_output_loc]           location of output file
-k[--key_word]                  the key word to search
-c[--enable_count]              enable count of messages

-h[--help]              to show this info
```
`-i`指定输入文件位置
`-o`指定输出文件位置
`-k`关键词检索
`-c`启用总消息记录


#### 使用示例

```
$python .\chat_cal.py -i .\talk.txt -k 日本

检索消息记录13754条

关键词"日本"出现163次

发送"日本"次数2         ..                                                      xxx
发送"日本"次数40        ..................................................      xxx
发送"日本"次数30        .....................................                   xxx
发送"日本"次数4         .....                                                   xxx
发送"日本"次数12        ...............                                         xxx
发送"日本"次数2         ..                                                      xxx
发送"日本"次数28        ...................................                     xxx
发送"日本"次数13        ................                                        xxx
发送"日本"次数13        ................                                        xxx
发送"日本"次数9         ...........                                             xxx
发送"日本"次数1         .                                                       xxx
发送"日本"次数2         ..                                                      xxx
发送"日本"次数2         ..                                                      xxx
发送"日本"次数1         .                                                       xxx
发送"日本"次数4         .....                                                   xxx
```

右侧“xxx”表示用户ID名称，此处出于隐私考虑替换

#### To do

- [ ] 添加整体/成员聊天消息数随时间增长图

- [ ] 制作GUI

- [ ] 统计词频时排除聊天记录中的@人名

- [ ] ~~将Time类型修改为datetime.dateime~~

- [ ] 修改数据结构以提升性能

  当前数据结构：

  ```
  member->time->message
  ```

  下一步预期改进

  ```
  time->message<-member
  time:{year:{month:{...{second:[message0, message1, ...]}}}
  message:['a message'(dtype=str)]
  member.talk = [messageA, messageB,...]
  ```

  

#### P.S

如何导出QQ聊天记录：

1. 打开任意对话框界面
2. 在输入文本框右上角点击“消息管理”旁下箭头
3. 选择“消息管理器”
4. 列表内右击群组/个人，选择“导出消息聊天记录”
5. 保存为`.txt`格式