### 处理QQ聊天记录

#### 介绍

检索出聊天记录内某关键词出现次数，及每个发言成员发言中出现该词次数，目前程序中1次发言最多计数1次.

开发环境 Python `3.6.7`

目前仅支持`.txt`文本格式，使用方式

```
$python .\chat_cal.py -h
-i[--file_input_loc]            location of input file
-o[--file_output_loc]           location of output file
-k[--key_word]                 the key word to search
-c[--enable_count]              enable count of messages Default: False
```



#### 使用示例

```
$python .\chat_cal.py -i .\talk.txt -k 这个

检索消息记录13331条

关键词"这个"出现126次

发送"这个"次数7         ...                     xxxxxxxx
发送"这个"次数6         ..                      xxx
发送"这个"次数10        ....                    xxx
发送"这个"次数7         ...                     xxxxx
发送"这个"次数2                                 xxxxx
发送"这个"次数6         ..                      xxxxxx
发送"这个"次数2                                 xxxxx
发送"这个"次数1                                 xxxxxxx
发送"这个"次数43        ....................    xxxx
发送"这个"次数15        .......                 xxxxxxxxx
发送"这个"次数3         .                       xxxxxx
发送"这个"次数3         .                       xxxxxxxx
发送"这个"次数5         ..                      xxx
发送"这个"次数2                                 xxxx
发送"这个"次数2                                 xxxxx
发送"这个"次数3         .                       xxxx
发送"这个"次数2                                 xxxxxxxxx
发送"这个"次数2                                 xxxx
发送"这个"次数1                                 xxx
发送"这个"次数1                                 xxx
发送"这个"次数1                                 xxxx
发送"这个"次数1                                 xxxxxxxx
发送"这个"次数1                                 xxx
```

右侧“xxx”表示用户ID名称，此处出于隐私考虑替换



#### P.S

如何导出QQ聊天记录：

1. 打开任意对话框界面
2. 在输入文本框右上角点击“消息管理”旁下箭头
3. 选择“消息管理器”
4. 列表内右击群组/个人，选择“导出消息聊天记录”
5. 保存为`.txt`格式