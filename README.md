##### 处理QQ聊天记录

检索出聊天记录内某关键词出现次数，及每个发言成员发言中出现该词次数，目前程序中1次发言最多计数1次.

目前仅支持`.txt`文本格式，使用方式

```
python .\chat_cal.py <resource file> <key word> [output file] 
```

`<resource file>`指定输入文件位置

`<key word>`指定检索关键词

`[output file]`可选参数，设置处理后输出文件位置