#-*- coding:utf-8 -*-
from re import search

SPECIAL = {'80000000':'匿名用户', '50000000':'系统提示'}
WIDTH = int(60)
BUILD = '20190612'

class member(object):
    def __init__(self, ID):
        self.name = ''
        self.id = ID
        self.count = 0
        '''
        self.talks = {year:{month:{day:{hour:{minute:{
            second:[times<int>, message<string>]}}}}}}
        '''
        self.talks = {}

    def add_message(self, Time, line):
        this = time_dict(self.talks, Time)
        this[1] += line

    def new_message(self, name, Time):
        self.name = name if self.id not in SPECIAL else SPECIAL[self.id]

        this = self.talks
        for t in Time[:-1]:
            if t in this:
                pass
            else:
                this[t] = {}
            this = this[t]
        if Time[-1] not in this:
            this[Time[-1]] = [0, '']

        this = time_dict(self.talks, Time)
        this[0] += 1
        self.count += 1

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
    name = search(r'.*(?=(\(|<))', info[2]).group()
    # deal with title, could be used if needed
    title = search(r'【.*】', name)
    if title != None:
        title = title.group()
        name = name.lstrip(title)
    
    ID = search(r'(?<=\()(.(?!\())*(?=\)$)|(?<=<)(.(?!<))*(?=>$)', info[2]).group()

    # Time = [year, month, day, hour, minute, second]
    return ID, name, Time


def usage():
    '''
    print('\nVersion: %s' % (BUILD))
    print('Usage:\n    search.exe -i <input file> [options] [...]\n')
    print('General Options:')
    print('    -i, --input_loc <path>\tLocation of input file.')
    print('    -o, --output_loc <path>\tLocation of output file.')
    print('    -k, --key_word <string>\tThe key word to search.')
    print('    -c, --count_enable\t\tEnable count of messages.')
    print('    -h, --help\t\t\tShow this info.\n')
    print('Notice: if there is only \'-i\' option, program would run on menu mode.')
    print('        (which is more suggested and flexible.)\n')
    print('For more help, visit\nhttps://github.com/maxwellzh/CRAQ/blob/master/README.md\n')
    '''
    print('\n发布版本：%s' % (BUILD))
    print('使用方式：\n    search.exe -i <input file> [options] [...]\n')
    print('可用选项：')
    print('    -i, --input_loc <path>\t指定输入文件位置，只添加-i参数时进入菜单模式（推荐）.')
    print('    -o, --output_loc <path>\t指定输出文件位置.')
    print('    -k, --key_word <string>\t指定关键词.')
    print('    -c, --count_enable\t\t消息统计.')
    print('    -h, --help\t\t\t展示帮助信息（本信息）.\n')
    print('使用示例：')
    print('    search.exe -i chatting.txt\n')
    print('获取更详细帮助信息，请访问项目：\nhttps://github.com/maxwellzh/CRAQ/blob/master/README.md\n')

def menu_usage():
    '''
    print('Search modes support:')
    print('1. Search all chatting history.')
    print('   usage: -a')
    print('2. Search chatting history specify by a key word or time duration.')
    print('   usage: -k <key word> -t <time> [<time end>]')
    print('   example: -k beauty -t 2019-5-26')
    print('            -k beauty -t 2019-5-16:end')
    print('Exit: exit<Enter>\n')
    print('Notice: once detect \'-a\', all others args except \'exit\' would be ignored.')
    print('        default output is by timeline, use \'-m\' for by members.')
    print('        <time> foamat: <year>-<month>-<day>.')
    print('        you can add a \'-o\' arg to print messages to console in any mode.\n')
    '''
    print('\
检索方式：\n\
    [options] <argument> [...]\n\
可用选项：\n\
    -t <date begin>[:<date end>]    在所指定日期范围内搜索，时间格式：<年>-<月>-<日>\n\
                                    可用beg代表记录中开始时间，end代表记录结束时间.\n\
    -k <key word>                   指定关键词.\n\
    -a                              统计所有信息，会覆盖其他参数（-k -t）.\n\
    -m                              按照成员发言数输出（默认为按日期输出）.\n\
    exit                            退出（或ctrl+c）.\n')

def proportion_visualize(this, max_count):
    if max_count == 0:
        width_this = int(0)
    else:
        width_this = int(this/max_count*WIDTH)
    return '%s%s' % (' '*(WIDTH-width_this), '#'*width_this)

def date_add_day(Time):
    # return Time + 1day
    year, month, day = Time
    projection = [31, 28, 31, 30, 31, 30,\
                  31, 31, 30, 31, 30, 31]
    is_leap = (year % 4 == 0 and year % 100 != 0 or
                year % 400 == 0)
    projection[1] = 29 if is_leap else 28
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
    count_ID = {}
    count_all = 0
    #talks = ''
    for ID in members.keys():
        time_cur = time_beg
        count_ID[ID] = 0
        while(time_cur <= time_end):
            count_cur, _ = members[ID].get_talks(date=time_cur, key_word=key_word)
            count_ID[ID] += count_cur
            #talks += line
            time_cur = date_add_day(time_cur)
        if count_ID[ID] == 0:
            count_ID.pop(ID)
        else:
            count_all += count_ID[ID]

    ID_ordered = sorted(count_ID.keys(), key=lambda item:count_ID[item], reverse=True)
    
    out_str = ''
    if time_beg == time_end:
        out_str += '%d-%d-%d期间检索到' % (time_beg[0], time_beg[1], time_beg[2])
    else:
        out_str += '%d-%d-%d:%d-%d-%d期间检索到' % (time_beg[0], time_beg[1], time_beg[2],\
                time_end[0], time_end[1], time_end[2])
    if key_word == '':
        out_str += '总消息%d条' % (count_all)
    else:
        out_str += '关键词\'%s\'%d次' % (key_word, count_all)

    if len(count_ID) > 0 :
        max_count = count_ID[ID_ordered[0]]
    else:
        return
    print('|%s' % (out_str))
    
    width_max = max(len(str(max_count)), 4)
    print('|%s|次数%s|用户名' % ('-'*WIDTH, ' '*(width_max-4)))

    for ID in ID_ordered:
        print('|%s|%d%s|%s' % (proportion_visualize(count_ID[ID], max_count), 
            count_ID[ID], ' ' *(width_max-len(str(count_ID[ID]))), members[ID].name))

def print_timeline(members, key_word, time_beg, time_end):
    count_date = {}
    time_cur = time_beg
    while(time_cur <= time_end):
        date = ['%02d' % x for x in time_cur]
        count_date['-'.join(date)] = 0
        time_cur = date_add_day(time_cur)

    for ID in members.keys():
        for date in count_date.keys():
            Time = [int(x) for x in date.split('-')]
            count_cur, _ = members[ID].get_talks(date=Time, key_word=key_word)
            count_date[date] += count_cur
    
    max_count = max(count_date.values())

    width_max = max(len(str(max_count)), 4)
    print('|%s|   日期   |次数%s' % ('-'*WIDTH, ' '*(width_max-4)))

    for date in count_date.keys():
        print('|%s|%s|%d%s' % (proportion_visualize(count_date[date], max_count), date,
            count_date[date], ' ' *(width_max-len(str(count_date[date])))))

def print_all(members):
    ID_ordered = sorted(members.keys(), key=lambda item:members[item].count, reverse=True)
    max_count = members[ID_ordered[0]].count
    width_max = max(len(str(max_count)), 4)

    print('|%s|次数%s|用户名' % ('-'*WIDTH, ' '*(width_max-4)))
    for ID in ID_ordered:
        print('|%s|%d%s|%s' % (proportion_visualize(members[ID].count, max_count),
            members[ID].count, ' '*(width_max-len(str(members[ID].count))), members[ID].name))

def get_lines(file_name):
    count = 0
    with open(file_name, 'rb') as f:
        while True:
            buffer = f.read(8192*1024)
            if not buffer:
                break
            count += buffer.count('\n'.encode())
    return int(count)