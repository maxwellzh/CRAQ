#!usr/bin/python
#-*- coding:utf-8 -*-
'''
message type:
xxxx-xx-xx xx:xx:xx 【title】NAME(ID)/【title】NAME<Email>
xxxx-xx-xx xx:xx:xx NAME(ID)/NAME<Email>
r'^\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{1,2}:\d{1,2}\s.*(\(\d+\)|<.*>)$'
'''
import os.path as path
import modules
import sys
import re
from getopt import getopt

member = modules.member

def main():
    short_opts = ['-h', '-i:', '-o:', '-k:', '-c', '-r:']
    long_opts = ['help', 'infile', 'outfile', 'kwd', 'count', 'regular']
    opts, _ = getopt(sys.argv[1:], ''.join(short_opts),
                     [long_opts[i]+short_opts[i][2:].replace(':', '=') for i in range(len(long_opts))])

    infile = ''
    outfile = ''
    word = ''
    regular = False
    count_enable = False
    flag_loop = (len(sys.argv[1:]) == 2 and
                 (sys.argv[1] == '-i' or sys.argv[1] == '--'+long_opts[1]))

    for op, value in opts:
        if op in (short_opts[0][:2], '--'+long_opts[0]):    # -h
            modules.usage()
            sys.exit()
        elif op in (short_opts[1][:2], '--'+long_opts[1]):  # -i:
            infile = str(value)
            infile = infile.split('+')
            infile = sorted(infile, key=lambda item: len(item))
        elif op in (short_opts[2][:2], '--'+long_opts[2]):  # -o:
            outfile = str(value)
        elif op in (short_opts[3][:2], '--'+long_opts[3]):  # -k:
            if word != '':
                modules.error(3)
            word = str(value)
        elif op in (short_opts[4][:2], '--'+long_opts[4]):  # -c
            count_enable = True
        elif op in (short_opts[5][:2], '--'+long_opts[5]):  # -r:
            if word != '':
                modules.error(3)
            word = str(value)
            regular = True

    # deal with 'click and run' on windows explorer 
    if len(opts) == 0:
        modules.usage()
        input('Press Enter to continue')
        sys.exit()

    members = {}
    last_talking = None
    count = []
    time_beg = [9999]  # only accurate to day
    time_end = []
    Time = []

    # read and process input file
    is_new = re.compile(r'^\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{1,2}:\d{1,2}\s.*(\(\d+\)|<.*>)$')
    for file in infile:
        if not path.isfile(file):
            modules.error(4)
        elif len(file) < 5 or file[-4:] != '.txt':
            modules.error(5)

        total_lines = modules.get_lines(file)
        out_interval = int(total_lines/100)

        with open(file, 'rt', encoding='utf-8') as fin:
            line_cur = int(0)
            out_line = ''
            for line in fin:
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
                    last_talking = members[ID].new_message(name, Time)
                    break
            for line in fin:
                line_cur += 1
                if is_new.search(line) == None:
                    # not a new message
                    out_line += line
                    continue
                else:
                    # a new message
                    count[-1] += 1
                    last_talking[1] += out_line

                    ID, name, Time = modules.get_info(line)
                    if ID not in members:
                        # a new member
                        members[ID] = member(ID)
                    last_talking = members[ID].new_message(name, Time)
                    out_line = ''

                # not accurate
                if line_cur % out_interval == 0:
                    prop = line_cur/total_lines
                    print('\rReading %s: %.0f%%|%s%s|' % (file, prop*100,
                    '#'*int(80*prop), '-'*int(80*(1-prop))), end='')
            last_talking[1] += out_line
        if Time[:3] > time_end:
            time_end = Time[:3]
    print('\r%s' % (' '*200), end='')
    print('\r%d-%d-%d:%d-%d-%d期间检索到' % (time_beg[0], time_beg[1], time_beg[2],
                                        time_end[0], time_end[1], time_end[2]), end='')
    print('消息记录%d条\n' % (sum(count)))

    # write to output file
    if outfile != '':
        modules.out(members, outfile)

    if count_enable:
        modules.mysearch(members, '', time_beg, time_end)

    if word != '':
        modules.mysearch(members, word, time_beg, time_end, regular=regular)

    # loop menu
    if flag_loop:
        modules.menu_usage()
    while(flag_loop):
        modules.menu(members, time_beg, time_end)

if __name__ == '__main__':
    main()
