#!usr/bin/python
#-*- coding:utf-8 -*-
'''
message type:
xxxx-xx-xx xx:xx:xx 【title】NAME(ID)/【title】NAME<Email>
xxxx-xx-xx xx:xx:xx NAME(ID)/NAME<Email>
r'^\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{1,2}:\d{1,2}\s.*(\(\d+\)|<.*>)$'
'''
import os.path as path
import argparse
import datetime
import modules
import sys
import re
import time

Member = modules.Member
VERSION = str(datetime.date.today()).replace('-', '')
parser = argparse.ArgumentParser(description=("QQ消息文本搜索[%s]" % VERSION), 
    epilog="获取更详细帮助信息：https://github.com/maxwellzh/CRAQ/blob/master/README.md")
parser._actions[0].help="显示当前信息."
parser.add_argument("-i", help="指定输入文件，只添加-i参数时进入菜单模式（推荐）.", 
    metavar="in-file", type=argparse.FileType('rt'), nargs='+', dest="infile")
parser.add_argument("-o", help="指定输出文件.", metavar="out-file", 
    type=argparse.FileType('wt'), dest="outfile")
search_group = parser.add_mutually_exclusive_group()
search_group.add_argument("-k", help="指定关键词，不与-r同时使用.",
    action="store", dest="keyword")
search_group.add_argument("-r", help="使用正则表达式搜索，不与-k同时使用.",
    action="store", dest="regular")
search_group.add_argument("-c", "--count", help="消息统计.", action="store_true",
    default=False, dest="count")
parser.add_argument("-v", "--version", help="显示当前程序版本", action="version",
    version=VERSION)


def main():
    args = parser.parse_args()
    # No argument error
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        exit(-1)
    # Not specify input file but ask for behavior like "-k, -r..."
    if args.infile==None:
        print("未指定输入文件.")
        exit(-1)

    infile = args.infile
    outfile = args.outfile
    keyword = args.keyword
    regular = args.regular
    count_enable = args.count

    members = {}
    count = 0
    time_beg = [9999]  # only accurate to day
    time_end = []
    Time = []

    # read and process input file
    t_beg = time.process_time()
    is_new = re.compile(r'\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{1,2}:\d{1,2}\s.*\n')
    for f in infile:
        with f as file:
            data = file.read()
            #print(data[:300])
            info = is_new.findall(data)
            msg = is_new.split(data)
            for i in range(len(info)):
                ID, name, Time = modules.get_info(info[i])
                if ID not in members:
                    # a new member
                    members[ID] = Member(ID)
                members[ID].new_message(name, Time, msg[i+1])
            #print(info==None)
            _, _, Time = modules.get_info(info[0])
            if Time[:3] < time_beg:
                time_beg = Time[:3]
            _, _, Time = modules.get_info(info[-1])
            if Time[:3] > time_end:
                time_end = Time[:3]

            count+=len(info)
    t_end = time.process_time()
    print('%d-%d-%d:%d-%d-%d期间检索到消息记录%d条' % (time_beg[0], time_beg[1], time_beg[2],
                                        time_end[0], time_end[1], time_end[2], count))
    print("time=%f" % (t_end - t_beg))
    if outfile != None:
        modules.out(members, outfile)
    if count_enable:
        modules.mysearch(members, '', time_beg, time_end)
    elif keyword != None:
        modules.mysearch(members, keyword, time_beg, time_end, regular=False)
    elif regular != None:
        modules.mysearch(members, regular, time_beg, time_end, regular=True)

    # Only -i option, enter MENU mode
    if not args.count and args.keyword==None and args.outfile==None and args.regular==None:
        modules.menu_usage()
        while True:
            modules.menu(members, time_beg, time_end)

if __name__ == '__main__':
    main()
