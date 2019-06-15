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
from re import search, sub
from getopt import getopt
#import matplotlib.pyplot as plt

member = modules.member

#plt.rcParams['font.sans-serif'] = ['SimHei']
#plt.rcParams['axes.unicode_minus'] = False


def main():
    short_opts = ['-h', '-i:', '-o:', '-k:', '-c', '-r:']
    long_opts = ['help', 'infile', 'outfile', 'kwd', 'count', 'regular']
    opts, _ = getopt(sys.argv[1:], ''.join(short_opts),
                     [long_opts[i]+short_opts[i][2:].replace(':', '=') for i in range(len(long_opts))])
    #print(sys.argv[1:])
    infile = ''
    outfile = ''
    kwd = ''
    count_enable = False
    regular = ''
    #flag_loop = True
    flag_loop = (len(sys.argv[1:]) == 2 and
                 (sys.argv[1] == '-i' or sys.argv[1] == '--'+long_opts[1]))

    for op, value in opts:
        #print(op[2:], long_opts[1])
        if op in (short_opts[0][:2], '--'+long_opts[0]):    # -h
            modules.usage()
            sys.exit()
        elif op in (short_opts[1][:2], '--'+long_opts[1]):  # -i:
            infile = str(value)
        elif op in (short_opts[2][:2], '--'+long_opts[2]):  # -o:
            outfile = str(value)
        elif op in (short_opts[3][:2], '--'+long_opts[3]):  # -k:
            kwd = str(value)
        elif op in (short_opts[4][:2], '--'+long_opts[4]):  # -c
            count_enable = True
        elif op in (short_opts[5][:2], '--'+long_opts[5]):  # -r:
            regular = str(value)
        else:  # useless just for debug
            print('Unknown args \'%s\'' % (op))
            modules.usage()
            sys.exit()

    # deal with 'click and run' on windows explorer 
    if len(opts) == 0:
        modules.usage()
        input('Press Enter to continue')
        sys.exit()

    if len(kwd) > 0 and len(regular) > 0:
            print('\'-k\'(--kwd)和\'-r\'(--regular)参数不可同时使用!')
            sys.exit()

    members = {}
    member_talking = None
    count = 0
    beg_time = []  # only accurate to day
    end_time = []
    Time = []

    # read and process input file
    if not path.isfile(infile):
        print('File .\\\'%s\' not exist!' % (infile))
        sys.exit()
    elif len(infile) < 5 or infile[-4:] != '.txt':
        print('Input file supposed to be .txt format.')
        sys.exit()

    num_lines = modules.get_lines(infile)
    out_interval = int(num_lines/100)

    with open(infile, 'rt', encoding='utf-8') as chat_record:
        line_cur = int(0)
        for line in chat_record:
            is_new = search(
                r'^\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{1,2}:\d{1,2}\s.*(\(\d+\)|<.*>)$', line) == None
            if is_new:
                # not a new message
                if member_talking != None:
                    member_talking.add_message(Time, line)
                else:   # irrelevant lines at the beginning
                    continue
            else:
                # a new message
                count += 1
                ID, name, Time = modules.get_info(line)
                if count == 1:
                    beg_time = Time[:3]
                if ID not in members:
                    # a new member
                    members[ID] = member(ID)

                members[ID].new_message(name, Time)
                member_talking = members[ID]
            line_cur += 1
            if line_cur % out_interval == 0:
                prop = line_cur/num_lines
                print('\rReading: %.0f%%|%s%s|' % (prop*100,
                                                   '#'*int(80*prop), '-'*int(80*(1-prop))), end='')

        end_time = Time[:3]

    print('\r%s' % (' '*100), end='')
    print('\r%d-%d-%d:%d-%d-%d期间检索到' % (beg_time[0], beg_time[1], beg_time[2],
                                        end_time[0], end_time[1], end_time[2]), end='')
    print('消息记录%d条\n' % (count))

    # write to output file
    if outfile != '':
        with open(outfile, 'wt', encoding='utf-8') as file_dealed:
            max_len = 0
            for ID in members.keys():
                if len(ID) > max_len:
                    max_len = len(ID)
            file_dealed.write('QQ ID/Email%sQQ NAME\n' % (' '*(max_len-9)))
            for ID in members.keys():
                file_dealed.write('%s%s%s\n' % (ID, ' '*(max_len-len(ID)+2), members[ID].name))
            file_dealed.write('\n')
            for ID in members.keys():
                file_dealed.write('%s' % '='*50)
                file_dealed.write('\nQQ ID/Email: %s\n' % (ID))
                file_dealed.write('QQ NAME: %s\n' % (members[ID].name))
                file_dealed.write('%s' % '='*50)
                file_dealed.write('\n')
                for Time, line in modules.traversing_dict(members[ID].talks):
                    Time = '%d-%02d-%02d %02d:%02d:%02d\n' % \
                        (Time[0], Time[1], Time[2], Time[3], Time[4], Time[5])
                    file_dealed.write(Time)
                    file_dealed.write(line[1])

    if count_enable:
        modules.print_all(members)

    if kwd != '':
        modules.by_members(members, kwd, beg_time, end_time)
    
    if regular != '':
        modules.by_regular(members, regular, beg_time, end_time)

    # loop menu
    if flag_loop:
        modules.menu_usage()
    while(flag_loop):
        modes = ''
        while(modes == ''):
            modes = str(input('>'))
        modes = modes.split(' ')
        short_opts_menu = ['-t:', '-k:', '-a', '-m', '-e', '-r:', '-d']
        long_opts_menu = ['time', 'kwd', 'all', 'member', 'exit', 'regular', 'detail']
        long_opts_menu = ['--'+x for x in long_opts_menu]
        opts, _ = getopt(modes, ''.join(short_opts_menu),
                         [long_opts_menu[i]+short_opts_menu[i][2:].replace(':', '=') for i in range(len(long_opts_menu))])
        kwd = ''
        regular = ''
        lower_bound = beg_time
        upper_bound = end_time
        all_flag = False
        member_flag = False
        if_print = False

        for op, value in opts:
            if op in (short_opts_menu[0][:2], '--'+long_opts_menu[0]):  # -t:
                Time = value.split(':')
                for i in range(min([2, len(Time)])):
                    Time[i] = sub('beg', ('%d%02d%02d' % \
                        (beg_time[0], beg_time[1], beg_time[2]))[2:], Time[i])
                    Time[i] = sub('end', ('%d%02d%02d' % \
                        (end_time[0], end_time[1], end_time[2]))[2:], Time[i])
                    
                    if len(Time[i]) > 6:
                        days = int(Time[i][6:])
                    else:
                        days = 0
                    
                    date = [2000+int(Time[i][:2]), int(Time[i][2:4]), int(Time[i][4:6])]
                    Time[i] = modules.date_add(date, days)

                if len(Time) == 1:
                    Time = Time*2
                lower_bound = Time[0]
                upper_bound = Time[1]
            elif op in (short_opts_menu[1][:2], '--'+long_opts_menu[1]):    # -k:
                kwd = value
            elif op in (short_opts_menu[2][:2], '--'+long_opts_menu[2]):    # -a
                all_flag = True
            elif op in (short_opts_menu[3][:2], '--'+long_opts_menu[3]):    # -m
                member_flag = True
            elif op in (short_opts_menu[4][:2], '--'+long_opts_menu[4]):    # -e
                sys.exit()
            elif op in (short_opts_menu[5][:2], '--'+long_opts_menu[5]):    # -r:
                regular = value
            elif op in (short_opts_menu[6][:2], '--'+long_opts_menu[6]):
                if_print = True
        
        if lower_bound > upper_bound:
            print('注意时间顺序')
            continue

        if len(kwd) > 0 and len(regular) > 0:
            print('\'-k\'(--kwd)和\'-r\'(--regular)参数不可同时使用!')
            continue
        
        if regular != '':
            modules.by_regular(members, regular, lower_bound, upper_bound, if_print)
            continue
        elif if_print:
            print('\'-d\'选项仅在正则搜索下可用')
            continue

        if member_flag:
            if all_flag:
                modules.print_all(members)
            else:
                modules.by_members(
                    members, kwd, lower_bound, upper_bound)
        else:
            if all_flag:
                modules.by_timeline(members, '', lower_bound, upper_bound)
            else:
                modules.by_timeline(members, kwd, lower_bound, upper_bound)

if __name__ == '__main__':
    main()
