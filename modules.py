#-*- coding:utf-8 -*-
import sys
import re
import datetime
from getopt import getopt

SPECIAL = {'80000000': '匿名用户', '50000000': '系统提示'}
WIDTH = int(60)
DATE = str(datetime.date.today()).replace('-', '')

id_re = re.compile(r'(?<=[>)])[^<(]*(?=[<(])')
name_re = re.compile(r'[^(<]*')
title_re = re.compile(r'【[^】]*】')


class Member(object):
    def __init__(self, ID):
        self.name = ''
        self.id = ID
        self.count = 0
        '''
        self.talks = {year:{month:{day:{hour:{minute:{
            second:[times<int>, message<string>]}}}}}}
        '''
        self.talks = {}
        self.lastupdate = []

    #def add_message(self, Time, line):
    #    this = time_dict(self.talks, Time)
    #    this[1] += line

    def new_message(self, name, Time, Msg):
        if Time > self.lastupdate:
            self.name = name if self.id not in SPECIAL else SPECIAL[self.id]
            self.lastupdate = Time
        this = self.talks
        for t in Time[:-1]:
            if t in this:
                pass
            else:
                this[t] = {}
            this = this[t]
        if Time[-1] not in this:
            this[Time[-1]] = [1, Msg]
            self.count += 1
            return
        else:
            if Msg == this[Time[-1]][1]:
                return
            else:
                this[Time[-1]][0] += 1
                this[Time[-1]][1] += Msg
                self.count += 1
                return

    def get_talks(self, date=[], key_word='', regular=False):
        # date = [year<int>, month<int>,...] prefix match
        # return count<int>, message<string>
        times = 0
        talks = ''
        this = time_dict(self.talks, date)
        if this == None:    # at specify date there is nothing
            return 0, ''
        else:
            if key_word == '':
                for Time, message in traversing_dict(this):
                    Time = date + Time
                    Time = '%d-%02d-%02d %02d:%02d:%02d\n' % \
                        (Time[0], Time[1], Time[2],
                         Time[3], Time[4], Time[5])
                    talks += Time + message[1]
                    times += message[0]
                return times, talks
            else:
                if regular:
                    regular = re.compile(r'%s' % key_word, flags=re.MULTILINE)
                    for Time, message in traversing_dict(this):
                        Time = date + Time
                        result = regular.findall(message[1])
                        if len(result) > 0:
                            Time = '%d-%02d-%02d %02d:%02d:%02d\n' % \
                                (Time[0], Time[1], Time[2],
                                 Time[3], Time[4], Time[5])
                            talks += Time + message[1]
                            times += len(result)
                else:
                    for Time, message in traversing_dict(this):
                        Time = date + Time
                        if key_word in message[1]:
                            Time = '%d-%02d-%02d %02d:%02d:%02d\n' % \
                                (Time[0], Time[1], Time[2],
                                 Time[3], Time[4], Time[5])
                            talks += Time + message[1]
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
        # deal with the situation where nickname contains space
        info = info[:2] + [' '.join(info[2:])]
    Time = info[0].split('-')+info[1].split(':')
    Time = [int(s) for s in Time]

    if len(info) < 3:
        print(line + "\nError:No nickname & ID")
        sys.exit(-1)

    pInfo = info[2][:-1]
    ID = id_re.search(pInfo[::-1]).group()
    ID = ID[::-1]
    name = pInfo[:len(pInfo)-len(ID)-2]

    # deal with title, could be used if needed
    title = title_re.search(name)
    if title != None:
        title = title.group()
        name = name.lstrip(title)

    # Time = [year, month, day, hour, minute, second]
    return ID, name, Time


def menu_usage():
    print('\
检索方式：\n\
    [options] <argument> [...]\n\
可用选项：\n\
    -t, --time                      在所指定日期范围内搜索，时间格式示例：190611\n\
        <date begin>[:<date end>]   可用beg代表记录中开始时间，end代表记录结束时间.\n\
    -k, --kwd <key word>            指定关键词，不可与-r共同使用.\n\
    -a, --all                       统计所有信息，会覆盖其他参数（-k -t）.\n\
    -m, --member                    按照成员发言数输出（默认为按日期输出）.\n\
    -r, --regular <pattern>         使用正则表达式搜索，不可与-k共同使用.\n\
    -d, --detail                    添加可输出详细信息.\n\
    -n, --name <name>               查询特定用户发言\n\
    -e, --exit                      退出（或ctrl+c）.\n\
    -h, --help                      显示帮助信息.\n\n\
示例：\n\
    -k 你们 -t end-6:end -n 飞翔的企鹅 -d\n\
    表示在最近1周内查询用户“飞翔的企鹅”包含“你们”的发言，并输出')


def proportion_visualize(this, max_count):
    if max_count == 0:
        width_this = int(0)
    else:
        width_this = int(this/max_count*WIDTH)
    return '%s%s' % (' '*(WIDTH-width_this), '#'*width_this)


def date_add(Time, days=1):
    # return Time + days(could be any integer)
    if days == 0:
        return Time
    year, month, day = Time
    projection = [31, 28, 31, 30, 31, 30,
                  31, 31, 30, 31, 30, 31]
    is_leap = (year % 4 == 0 and year % 100 != 0 or
               year % 400 == 0)
    projection[1] = 29 if is_leap else 28

    if days > 0:
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
        return date_add([year, month, day], days-1)
    else:
        if day - 1 == 0:
            if month == 1:
                year -= 1
                month = 12
                day = 31
            else:
                month -= 1
                day = projection[month-1]
        else:
            day -= 1
        return date_add([year, month, day], days+1)


def get_lines(file_name):
    count = 0
    if type(file_name) == str:
        with open(file_name, 'rb') as file:
            while True:
                buffer = file.read(8192*1024)
                if not buffer:
                    break
                count += buffer.count('\n')
    else:
        file = file_name
        while True:
            buffer = file.read(8192*1024)
            if not buffer:
                break
            count += buffer.count('\n')
        file.seek(0)
    return int(count)


def mysearch(members, keyword, time_beg, time_end, method='members', regular=False, redetails=False):
    members_count = {}
    members_lines = {}

    if redetails:
        method = 'members'
    out_str = '> '
    if time_beg == time_end:
        out_str += '%d-%d-%d期间检索到' % (time_beg[0], time_beg[1], time_beg[2])
    else:
        out_str += '%d-%d-%d:%d-%d-%d期间检索到' % (time_beg[0], time_beg[1], time_beg[2],
                                               time_end[0], time_end[1], time_end[2])
    date_list = []
    time_cur = time_beg
    while(time_cur <= time_end):
        date_list.append(time_cur)
        time_cur = date_add(time_cur)

    for ID in members.keys():
        members_count[ID] = []
        members_lines[ID] = ''
        for date in date_list:
            count, lines = members[ID].get_talks(date, keyword, regular)
            members_count[ID].append(count)
            members_lines[ID] += lines

    headline = '|%s|' % ('-'*WIDTH)
    part_1st = None
    part_2nd = None
    part_3rd = None
    max_count = 0
    total = 0
    if method == 'timeline':
        date_count = []
        for i in range(len(date_list)):
            date_list[i] = '-'.join(['%02d' % x for x in date_list[i]])
            date_count.append(0)
        for i in range(len(date_list)):
            for ID in members_count.keys():
                date_count[i] += members_count[ID][i]
            if date_count[i] > max_count:
                max_count = date_count[i]

        total = sum(date_count)
        if total == 0:
            headline = ''
            part_1st = []
            part_2nd = []
            part_3rd = []
        else:
            headline = headline + '   日期   |次数'
            part_1st = date_count
            part_2nd = date_list
            part_3rd = date_count
    elif method == 'members':
        if redetails:
            for ID in members_count.keys():
                members_count[ID] = sum(members_count[ID])
                if members_count[ID] > 0:
                    print('%s' % '='*50)
                    print('%s<%s>[%d]' %
                          (members[ID].name, ID, members_count[ID]))
                    print('%s' % '='*50)
                    print(members_lines[ID])
            return
        width_max = 4
        for ID in members.keys():
            members_count[ID] = sum(members_count[ID])
            if members_count[ID] == 0:
                members_count.pop(ID)
                members_lines.pop(ID)
            else:
                total += members_count[ID]

        if len(members_count) > 0:
            ID_ordered = sorted(members_count.keys(), key=lambda
                                item: members_count[item], reverse=True)
            max_count = members_count[ID_ordered[0]]
            width_max = max([4, len(str(max_count))])

        if total == 0:
            headline = ''
            part_1st = []
            part_2nd = []
            part_3rd = []
        else:
            headline = headline + ('次数%s|用户名' % (' '*(width_max-4)))
            part_1st = [members_count[ID] for ID in ID_ordered]
            part_2nd = ['%d%s' % (x, ' '*(width_max-len(str(x))))
                        for x in part_1st]
            part_3rd = [members[x].name for x in ID_ordered]
    else:
        error(1)

    if len(part_1st) != len(part_2nd) or \
            len(part_1st) != len(part_3rd):
        error(2)

    if regular:
        out_str += '正则式\'%s\'%d次\n' % (keyword, total)
    elif keyword != '':
        out_str += '关键词\'%s\'%d次\n' % (keyword, total)
    else:
        out_str += '消息%d条\n' % total
    print(out_str+headline)
    for i in range(len(part_1st)):
        print('|%s|%s|%s' % (proportion_visualize(part_1st[i], max_count),
                             part_2nd[i], part_3rd[i]))


def out(members, outfile):
    line_cur = 0
    max_len = 0
    count = 0
    if type(outfile) == str:
        with open(outfile, 'wt', encoding='utf-8') as file:
            print('Writing to %s:' % outfile)
            for ID in members.keys():
                count += members[ID].count
                if len(ID) > max_len:
                    max_len = len(ID)
            file.write('QQ ID/Email%sQQ NAME\n' % (' '*(max_len-9)))
            for ID in members.keys():
                file.write('%s%s%s\n' %
                           (ID, ' '*(max_len-len(ID)+2), members[ID].name))
            file.write('\n')
            for ID in members.keys():
                file.write('%s' % '='*50)
                file.write('\nQQ ID/Email: %s\n' % (ID))
                file.write('QQ NAME: %s\n' % (members[ID].name))
                file.write('%s' % '='*50)
                file.write('\n')
                for Time, line in traversing_dict(members[ID].talks):
                    Time = '%d-%02d-%02d %02d:%02d:%02d\n' % \
                        (Time[0], Time[1], Time[2], Time[3], Time[4], Time[5])
                    file.write(Time)
                    file.write(line[1])
                line_cur += members[ID].count
                prop = line_cur/count
                print('\r%.0f%%|%s%s|' %
                      (prop*100, '#'*int(80*prop), '-'*int(80*(1-prop))), end='')
    else:
        with outfile as file:
            print('Writing:')
            for ID in members.keys():
                count += members[ID].count
                if len(ID) > max_len:
                    max_len = len(ID)
            file.write('QQ ID/Email%sQQ NAME\n' % (' '*(max_len-9)))
            for ID in members.keys():
                file.write('%s%s%s\n' %
                           (ID, ' '*(max_len-len(ID)+2), members[ID].name))
            file.write('\n')
            for ID in members.keys():
                file.write('%s' % '='*50)
                file.write('\nQQ ID/Email: %s\n' % (ID))
                file.write('QQ NAME: %s\n' % (members[ID].name))
                file.write('%s' % '='*50)
                file.write('\n')
                for Time, line in traversing_dict(members[ID].talks):
                    Time = '%d-%02d-%02d %02d:%02d:%02d\n' % \
                        (Time[0], Time[1], Time[2], Time[3], Time[4], Time[5])
                    file.write(Time)
                    file.write(line[1])
                line_cur += members[ID].count
                prop = line_cur/count
                print('\r%.0f%%|%s%s|' % (prop*100, '#'*int(80*prop),
                                          '-'*int(80*(1-prop))), end='')


def msgmerge(members, outfile):
    # content = [[Time, ID, Msg], ...]
    # Time = [Year, Month, Day, Hour, Minute, Second]
    # ID = 'Name(ID)'
    # Msg = '...'
    content = []
    print("Merging...")
    for Person in members.values():
        for Time, line in traversing_dict(Person.talks):
            content.append([Time, "%s(%s)" % (Person.name, Person.id), line])
    content = sorted(content, key=lambda item: item[0])
    with outfile as file:
        file.write('MSG merged at %s.\n\n' % DATE)
        for msg in content:
            file.write('%d-%02d-%02d %02d:%02d:%02d %s\n%s' %
                       (msg[0][0], msg[0][1], msg[0][2], msg[0][3], msg[0][4], msg[0][5], msg[1], msg[2][1]))


def menu(members, time_beg, time_end):
    modes = ''
    while(modes == ''):
        modes = str(input('> '))
    modes = re.findall(r'(?<=").*(?=")|(?!"|\s)\S*', modes)
    modes = modes[:-1]
    short_opts_menu = ['-t:', '-k:', '-a', '-m', '-e', '-r:', '-d', '-n:', '-h']
    long_opts_menu = ['time', 'kwd', 'all', 'member',
                      'exit', 'regular', 'detail', 'name', 'help']
    long_opts_menu = ['--'+x for x in long_opts_menu]
    opts, _ = getopt(modes, ''.join(short_opts_menu),
                     [long_opts_menu[i]+short_opts_menu[i][2:].replace(':', '=') for i in range(len(long_opts_menu))])
    keyword = ''
    lower_bound = time_beg
    upper_bound = time_end
    method = 'timeline'
    regular = False
    redetails = False
    this = members

    for op, value in opts:
        if op in (short_opts_menu[0][:2], '--'+long_opts_menu[0]):  # -t:
            method = 'timeline'
            Time = value.split(':')
            for i in range(min([2, len(Time)])):
                Time[i] = re.sub('beg', ('%d%02d%02d' %
                                         (time_beg[0], time_beg[1], time_beg[2]))[2:], Time[i])
                Time[i] = re.sub('end', ('%d%02d%02d' %
                                         (time_end[0], time_end[1], time_end[2]))[2:], Time[i])

                if len(Time[i]) > 6:
                    days = int(Time[i][6:])
                else:
                    days = 0

                date = [2000+int(Time[i][:2]), int(Time[i]
                                                   [2:4]), int(Time[i][4:6])]
                Time[i] = date_add(date, days)

            if len(Time) == 1:
                Time = Time*2
            lower_bound = Time[0]
            upper_bound = Time[1]
        elif op in (short_opts_menu[1][:2], '--'+long_opts_menu[1]):    # -k:
            if keyword != '':
                error(3)
            keyword = value
        elif op in (short_opts_menu[2][:2], '--'+long_opts_menu[2]):    # -a
            keyword = ''
            lower_bound = time_beg
            upper_bound = time_end
            regular = False
            redetails = False
            this = members
        elif op in (short_opts_menu[3][:2], '--'+long_opts_menu[3]):    # -m
            method = 'members'
        elif op in (short_opts_menu[4][:2], '--'+long_opts_menu[4]):    # -e
            sys.exit(0)
        elif op in (short_opts_menu[5][:2], '--'+long_opts_menu[5]):    # -r:
            if keyword != '':
                error(3)
            keyword = value
            regular = True
        elif op in (short_opts_menu[6][:2], '--'+long_opts_menu[6]):    # -d
            redetails = True
        elif op in (short_opts_menu[7][:2], '--'+long_opts_menu[7]):    # -n:
            for ID in members.keys():
                if members[ID].name == value:
                    this = {ID: members[ID]}
                    break
            if this == members:
                error(10)
                return
        elif op in (short_opts_menu[8][:2], '--'+long_opts_menu[8]):    # -h
            menu_usage()
            return

    if len(opts) == 0:
        error(6)
        menu_usage()
        return
    if lower_bound > upper_bound:
        error(7)
        return

    mysearch(this, keyword, lower_bound,
             upper_bound, method, regular, redetails)


def error(err):
    err_dict = {
        0: 'mysearch(): redetail should always be with regular.',
        1: 'mysearch(): method not support.',
        2: 'mysearch(): length of part 1 2 3 should be equal.',
        3: 'main(): \'-k\'(--kwd)和\'-r\'(--regular)参数不可同时使用.',
        4: 'main(): 输入文件位置无效.',
        5: 'main(): 输入文件非.txt格式.',
        6: '> 输入参数有误',
        7: '> 注意时间顺序',
        8: '',
        9: '> \'-d\'选项仅在正则搜索下可用.',
        10: '> 找不到指定用户（若用户名含有空格请用英文引号括起来）'
    }
    print(err_dict[err])
    if err in range(6):
        sys.exit(-1)
