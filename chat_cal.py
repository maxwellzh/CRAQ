#!usr/bin/python
#-*- coding:utf-8 -*-
'''
message type:
2019-xx-xx xx:xx:xx NAME(QQ_ID)
'''
import sys
import os.path as path
import re
import operator
import getopt
import datetime as dt
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
SPECIAL = {"80000000":"匿名用户", "50000000":"系统提示"}

class member(object):
    def __init__(self, ID, name):
        self.name = name if ID not in SPECIAL else SPECIAL[ID]
        self.id = ID
        self.count = 0
        '''
        self.talks = {year:{month:{day:{hour:{minute:{
            second:[times<int>, message<string>]}}}}}}
        '''
        self.talks = {}

    def add_message(self, Time, line):
        this = self.talks
        for t in Time[:-1]:
            if t in this:
                pass
            else:
                this[t] = {}
            this = this[t]
        if Time[-1] not in this:
            this[Time[-1]] = [0, '']

        this = self.talks[Time[0]][Time[1]][Time[2]
                                            ][Time[3]][Time[4]][Time[5]]
        this[0] += 1
        this[1] += line

    def new_message(self, name, Time):
        self.name = name if self.id not in SPECIAL else SPECIAL[self.id]
        this = time_dict(self.talks, Time)
        if this != None:
            this[0] += 1
        else:
            return

    def get_talks(self, date=[], key_word=''):
        # date = [year<int>, month<int>,...] prefix match
        # return count<int>, message<string>
        times = 0
        talks = ''
        this = time_dict(self.talks, date)
        if this == None:    # at specify date there is nothing
            return 0, ''
        else:
            if key_word == '':
                for _, message in traversing_dict(this):
                    talks += message[1]
                    times += message[0]
                return times, talks
            else:
                for _, message in traversing_dict(this):
                    if key_word in message[1]:
                        talks += message[1]
                    times += message[1].count(key_word)
                return times, talks

def traversing_dict(Dict):
    # yield date, pointer
    # date: [year<int>, month<int>, ...]
    if type(Dict) is not dict:
        return Dict
    for key, value in Dict.items():
        if type(value) is not dict:
            yield [key], value
        else:
            for key_x, x in traversing_dict(value):
                yield [key] + key_x, x

def time_dict(talks, Time):
    # return pointer specified by Time
    # return [times<int>, message<string>]
    if len(Time) == 0:
        return talks
    if Time[0] in talks:
        if len(Time) == 1:
            return talks[Time[0]]
        else:
            return time_dict(talks[Time[0]], Time[1:])
    else:
        None


def get_info(line):
    # return ID<string>, name<string>, Time<list>

    info = line.split(' ')
    if len(info) > 3:
        info = info[:2] + [' '.join(info[2:])]
    Time = info[0].split('-')+info[1].split(':')
    Time = [int(s) for s in Time]
    #print(Time)
    name = re.search(r".*(\(|<)", info[2]).group()[:-1]
    ID = re.search(r"(\(|<)(.(?!(\(|<)))*(\)|>)$", info[2]).group()[1:-1]
    if len(ID) == 0:
        ID = re.search(r"<.*>", info[2]).group()[1:-1]

    # Time = [year, month, day, hour, minute, second]
    return ID, name, Time


def usage():
    print(
        "\nUsage:\n  python chat_cal.py -i <input file> [options] [...]\n")
    print("General Options:")
    print("  -i, --input_loc <path>\tLocation of input file.")
    print("  -o, --output_loc <path>\tLocation of output file.")
    print("  -k, --key_word <string>\tThe key word to search.")
    print("  -c, --count_enable\t\tEnable count of messages.")
    print("  -h, --help\t\t\tShow this info.\n")
    print("Notice: if there is only \'-i\' option, program would run on menu mode.")
    print("        (which is more suggested and flexible.)\n-")


def proportion_visualize(this, max_count):

    width_this = int(this/max_count*50)
    width_max = int(50)

    return "%s%s" % ('.'*width_this, ' '*(width_max-width_this))

def date_add_day(Time):
    # return Time + 1day
    year, month, day = Time
    projection = [31, 29, 31, 30, 31, 30,\
                  31, 31, 30, 31, 30, 31]
    is_leap = (year % 4 == 0 and year % 100 != 0 or
                year % 400 == 0)
    projection[1] = 28 if is_leap else 29
    if projection[month-1] < day + 1:
        if month == 12:
            year += 1
            month = 1
            day = 1
        else:
            month += 1
            day = 1
    else:
        day += 1
    return [year, month, day]

def print_analysis(members, key_word, time_beg, time_end, flag = False):
    # print messages under developing
    max_count_word = int(0)
    count_ID = {}
    count_all = 0
    for ID in members.keys():
        time_cur = time_beg
        count_ID[ID] = 0
        while(time_cur <= time_end):
            count_cur, _ = members[ID].get_talks(date=time_cur, key_word=key_word)
            count_ID[ID] += count_cur
            time_cur = date_add_day(time_cur)
        max_count_word = max([max_count_word, count_ID[ID]])
        count_all += count_ID[ID]

    print("\n%d-%d-%d:%d-%d-%d期间检索到" % (time_beg[0], time_beg[1], time_beg[2],\
            time_end[0], time_end[1], time_end[2]), end='')
    if key_word == '':
        print("消息%d条\n" % (count_all))
    else:
        print("关键词\"%s\"%d次\n" % (key_word, count_all))
    key_word = ("发送\"%s\"" % (key_word)) if key_word != '' else ("发送消息")
    for ID in count_ID.keys():
        if count_ID[ID] != 0:
            print("%s次数%d%s  %s\t%s" % (
                key_word, count_ID[ID], ' ' *
                (len(str(max_count_word))-len(str(count_ID[ID]))),
                proportion_visualize(count_ID[ID], max_count_word), members[ID].name))
    print('\n')

def print_all(members, max_count):
    for ID in members.keys():
            print("发消息%d%s  次数\t%s\t%s" %
                  (members[ID].count, ' '*(len(str(max_count))-len(str(members[ID].count))),
                      proportion_visualize(members[ID].count, max_count), members[ID].name))

def main():
    opts, _ = getopt.getopt(sys.argv[1:], "-h-i:-o:-k:-c",
                            ["help", "input_loc", "output_loc", "key_word", "count_enable"])
    input_loc = ''
    output_loc = ''
    key_word = ''
    count_enable = False
    flag_loop = len(sys.argv[1:]) == 2

    for op, value in opts:
        if op == "-i" or op == "--input_loc":
            input_loc = str(value)
            if not path.isfile(input_loc):
                print("File %s not exist!" % (input_loc))
                sys.exit()
            elif len(input_loc) < 5 or input_loc[-4:] != ".txt":
                print("Input file supposed to be .txt format.")
                sys.exit()
        elif op == "-o" or op == "--output_loc":
            output_loc = str(value)
        elif op == "-k" or op == "--key_word":
            key_word = str(value)
        elif op == "-c" or op == "--count_enable":
            count_enable = True
        elif op == "-h" or op == "--help":
            usage()
            sys.exit()
        else:
            print("Unknown args \"%s\"" % (op))
            usage()
            sys.exit()
    

    members = {}
    member_talking = None
    count = 0
    max_count_message = int(0)
    beg_time = [9999]  # only accurate to day
    end_time = [0]

    # read and process input file
    with open(input_loc, "rt", encoding="utf-8") as chat_record:
        for line in chat_record:
            if line[:2] != "20" or (line[-2] != ')' and line[-2] != '>'):
                # not a new message
                if member_talking != None:
                    member_talking.add_message(Time, line)
                else:   # irrelevant lines at the beginning
                    continue
            else:
                # a new message
                count += 1
                ID, name, Time = get_info(line)
                beg_time = Time[:3] if Time[:3] < beg_time else beg_time
                end_time = Time[:3] if Time[:3] > end_time else end_time
                if ID in members:
                    # an old member
                    members[ID].new_message(name, Time)
                else:
                    # a new member
                    members[ID] = member(ID, name)

                #members[ID].add_message(Time)
                members[ID].count += 1
                max_count_message = max([max_count_message, members[ID].count])
                member_talking = members[ID]

    print("\n%d-%d-%d:%d-%d-%d期间检索到" % (beg_time[0], beg_time[1], beg_time[2],\
            end_time[0], end_time[1], end_time[2]), end='')
    print("消息记录%d条" % (count))


    # write to output file
    if len(output_loc) > 0:
        with open(output_loc, "wt", encoding="utf-8") as file_dealed:
            file_dealed.write("QQ ID/EMAIL%sQQ NAME\n" % (' '*4))
            for ID in members.keys():
                file_dealed.write("%s\t%s\n" % (ID, members[ID].name))
            file_dealed.write('\n')
            for ID in members.keys():
                file_dealed.write("QQ ID/EMAIL: %s\n" % (ID))
                file_dealed.write("QQ NAME: %s\n" % (members[ID].name))
                for Time, line in traversing_dict(members[ID].talks):
                    Time = [str(x) for x in Time]
                    Time = Time[0]+'-'+Time[1]+'-'+Time[2] + \
                        ' '+Time[3]+':'+Time[4]+':'+Time[5] + '\n'
                    file_dealed.write(Time)
                    file_dealed.write(line[1])

    if count_enable:
        print_all(members, max_count_message)

    if key_word != '':
        print_analysis(members, key_word, beg_time, end_time)

    # loop menu
    while(flag_loop):
        print("Search modes support:")
        print("1. Search all chatting history.")
        print("   usage: -a")
        print("2. Search chatting history specify by a key word or time duration.")
        print("   usage: -k <key word> -t <time> [<time end>]")
        print("   example: -k beauty -t 2019-5-26")
        print("            -k beauty -t 2019-5-16:end")
        print("Exit: exit<Enter>\n")
        print("Notice: once detect \'-a\', all others args except 'exit' would be ignored.")
        print("        <time> foamat: <year>-<month>-<day>.")
        print(
            "        you can add a \'-o\' arg to print messages to console in any mode.\n")

        modes = ''
        flag_print = False
        while(modes == ''):
            modes = str(input(">"))
        modes = modes.split(' ')
        if "exit" == modes[0]:
            sys.exit()
        else:
            key_word = ''
            lower_bound = beg_time
            upper_bound = end_time
        if "-a" in modes:
            print_all(members, max_count_message)
        else:
            if "-k" in modes:
                index_word = modes.index("-k") + 1
                key_word = modes[index_word]
                del modes[index_word-1:index_word+1]
            if "-t" in modes:
                Time = modes[modes.index("-t") + 1].split(':')
                for i in range(len(Time)):
                    if "begin" == Time[i]:
                        Time[i] = beg_time
                    elif "end" == Time[i]:
                        Time[i] = end_time
                    else:
                        Time[i] = Time[i].split('-')
                        Time[i] = [int(x) for x in Time[i]]
                if len(Time) == 1:
                    Time = Time*2
                lower_bound = Time[0] if Time[0] > beg_time else beg_time
                upper_bound = Time[1] if Time[1] < end_time else end_time
            if "-o" in modes:
                flag_print = True
            print_analysis(members, key_word, lower_bound, upper_bound, flag_print)
        input('Press Enter to continue')

if __name__ == "__main__":
    main()
