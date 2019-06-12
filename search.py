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
from re import search
from getopt import getopt
#import matplotlib.pyplot as plt

member = modules.member

#plt.rcParams['font.sans-serif'] = ['SimHei']
#plt.rcParams['axes.unicode_minus'] = False

def main():
    opts, _ = getopt(sys.argv[1:], '-h-i:-o:-k:-c',
                            ['help', 'input_loc', 'output_loc', 'key_word', 'count_enable'])
    #print(sys.argv[1:])
    input_loc = ''
    output_loc = ''
    key_word = ''
    count_enable = False
    flag_loop = len(sys.argv[1:]) == 2

    for op, value in opts:
        if op == '-i' or op == '--input_loc':
            input_loc = str(value)    
        elif op == '-o' or op == '--output_loc':
            output_loc = str(value)
        elif op == '-k' or op == '--key_word':
            key_word = str(value)
        elif op == '-c' or op == '--count_enable':
            count_enable = True
        elif op == '-h' or op == '--help':
            modules.usage()
            sys.exit()
        else:
            print('Unknown args \'%s\'' % (op))
            modules.usage()
            sys.exit()
    if len(opts) == 0:
        modules.usage()
        input('Press Enter to continue')
        sys.exit()

    members = {}
    member_talking = None
    count = 0
    beg_time = []  # only accurate to day
    end_time = []
    Time = []

    # read and process input file
    if not path.isfile(input_loc):
        print('File %s not exist!' % (input_loc))
        sys.exit()
    elif len(input_loc) < 5 or input_loc[-4:] != '.txt':
        print('Input file supposed to be .txt format.')
        sys.exit()

    num_lines = modules.get_lines(input_loc)
    out_interval = int(num_lines/100)

    with open(input_loc, 'rt', encoding='utf-8') as chat_record:
        line_cur = int(0)
        for line in chat_record:
            is_new = search(r'^\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{1,2}:\d{1,2}\s.*(\(\d+\)|<.*>)$', line) == None
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
                print('\rReading: %.0f%%|%s%s|' % (prop*100, \
                    '#'*int(80*prop), '-'*int(80*(1-prop))), end='')
            
        end_time = Time[:3]

    print('\r%s' % (' '*100), end='')
    print('\r%d-%d-%d:%d-%d-%d期间检索到' % (beg_time[0], beg_time[1], beg_time[2],\
            end_time[0], end_time[1], end_time[2]), end='')
    print('消息记录%d条\n' % (count))


    # write to output file
    if len(output_loc) > 0:
        with open(output_loc, 'wt', encoding='utf-8') as file_dealed:
            file_dealed.write('QQ ID/Email%sQQ NAME\n' % (' '*4))
            for ID in members.keys():
                file_dealed.write('%s\t%s\n' % (ID, members[ID].name))
            file_dealed.write('\n')
            for ID in members.keys():
                file_dealed.write('QQ ID/Email: %s\n' % (ID))
                file_dealed.write('QQ NAME: %s\n' % (members[ID].name))
                for Time, line in modules.traversing_dict(members[ID].talks):
                    Time = [str(x) for x in Time]
                    Time = Time[0]+'-'+Time[1]+'-'+Time[2] + \
                        ' '+Time[3]+':'+Time[4]+':'+Time[5] + '\n'
                    file_dealed.write(Time)
                    file_dealed.write(line[1])

    if count_enable:
        modules.print_all(members)

    if key_word != '':
        modules.print_analysis(members, key_word, beg_time, end_time)

    # loop menu
    if flag_loop:
        modules.menu_usage()
    while(flag_loop):
        modes = ''
        flag_print = False
        while(modes == ''):
            modes = str(input('>'))
        modes = modes.split(' ')
        if 'exit' == modes[0]:
            sys.exit()
        else:
            key_word = ''
            lower_bound = beg_time
            upper_bound = end_time
        if '-a' in modes:
            if '-m' in modes:
                modules.print_all(members)
            else:
                modules.print_timeline(members, '', lower_bound, upper_bound)
        else:
            if '-k' in modes:
                index_word = modes.index('-k') + 1
                if len(modes) <= index_word:
                    print('>\'-k\' option argument lost.\n')
                    continue
                key_word = modes[index_word]
                del modes[index_word-1:index_word+1]
            if '-t' in modes:
                index_t = modes.index('-t') + 1
                if len(modes) > index_t:
                    Time = modes[modes.index('-t') + 1].split(':')
                    for i in range(len(Time)):
                        if 'beg' == Time[i]:
                            Time[i] = beg_time
                        elif 'end' == Time[i]:
                            Time[i] = end_time
                        else:
                            Time[i] = Time[i].split('-')
                            Time[i] = [int(x) for x in Time[i]]
                    if len(Time) == 1:
                        Time = Time*2
                    lower_bound = Time[0] if Time[0] > beg_time else beg_time
                    upper_bound = Time[1] if Time[1] < end_time else end_time
            if '-o' in modes:
                flag_print = True
            if '-m' in modes:
                modules.print_analysis(members, key_word, lower_bound, upper_bound, flag_print)
            else:
                modules.print_timeline(members, key_word, lower_bound, upper_bound)

if __name__ == '__main__':
    main()
