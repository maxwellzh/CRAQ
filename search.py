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

member = modules.member
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
    last_msg = None
    count = []
    time_beg = [9999]  # only accurate to day
    time_end = []
    Time = []

    # read and process input file
    is_new = re.compile(r'^\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{1,2}:\d{1,2}\s.*(\(\d+\)|<.*>)$')
    for f in infile:
        with f as file:
            total_lines = modules.get_lines(file)
            out_interval = int(total_lines/100)

            line_cur = int(0)
            out_line = ''

            # First deal with useless head lines
            for line in file:
                line_cur += 1
                if is_new.search(line) == None:
                    continue
                else:
                    count.append(1)
                    ID, name, Time = modules.get_info(line)
                    if Time[:3] < time_beg:
                        time_beg = Time[:3]
                    if ID not in members:
                        members[ID] = member(ID)
                    last_msg = members[ID].new_message(name, Time)
                    break

            # Deal with main text
            for line in file:
                line_cur += 1
                if is_new.search(line) == None:
                    # not a new message
                    out_line += line
                    continue
                else:
                    # a new message
                    count[-1] += 1
                    last_msg[1] += out_line

                    ID, name, Time = modules.get_info(line)
                    if ID not in members:
                        # a new member
                        members[ID] = member(ID)
                    last_msg = members[ID].new_message(name, Time)
                    out_line = ''

                # not accurate
                if line_cur % out_interval == 0:
                    prop = line_cur/total_lines
                    print('\rReading: %.0f%%|%s%s|' % (prop*100,
                    '#'*int(80*prop), '-'*int(80*(1-prop))), end='')
            last_msg[1] += out_line
        if Time[:3] > time_end:
            time_end = Time[:3]
    print('\r%s' % (' '*200), end='')
    print('\r%d-%d-%d:%d-%d-%d期间检索到' % (time_beg[0], time_beg[1], time_beg[2],
                                        time_end[0], time_end[1], time_end[2]), end='')
    print('消息记录%d条\n' % (sum(count)))


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
