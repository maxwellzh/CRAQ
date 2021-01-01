import re
import sys
import datetime
import shlex
import argparse
from collections import OrderedDict

SPECIAL = {'80000000': '匿名用户', '50000000': '系统提示'}
WIDTH = int(60)
DATE = str(datetime.date.today()).replace('-', '')

id_re = re.compile(r'(?<=[>)])[^<(]*(?=[<(])')
name_re = re.compile(r'[^(<]*')
title_re = re.compile(r'【[^】]*】')


def get_info(line):
    r'''
    return `(ID, name, Time)` \
    `ID`: string \
    `name`: string \
    `Time`: list
    '''

    info = line.split(' ')
    if len(info) > 3:
        # deal with the situation where nickname contains space
        info = info[:2] + [' '.join(info[2:])]

    # convert time string into list of integers
    Time = info[0].split('-')+info[1].split(':')
    Time = [int(s) for s in Time]

    if len(info) < 3:
        raise ValueError(
            "Invalid format: no nickname and ID \'{}\'".format(line))

    # get the name and ID
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


class RecordData(object):
    def __init__(self) -> None:
        super().__init__()
        self._member = OrderedDict()
        self._msg = []
        self.is_t_sorted = True
        self._countmsg = 0

    @property
    def size_msg(self):
        return self._countmsg

    @property
    def size_group(self):
        return len(self._member.keys())

    @property
    def when_beg(self):
        if not self.is_t_sorted:
            self.sort_time()
        return self._msg[0][0]

    @property
    def when_end(self):
        if not self.is_t_sorted:
            self.sort_time()
        return self._msg[-1][0]

    def sort_time(self):
        self._msg = sorted(self._msg, key=lambda x: x[0])
        for state in self._member.values():
            del state['msg']
            state['msg'] = []
        for i, msg in enumerate(self._msg):
            _, ID, _ = msg
            self._member[ID]['msg'].append(i)
        self.is_t_sorted = True

    def add_msg(self, infoline, msg):
        ID, name, Time = get_info(infoline)

        if ID in self._member:
            self._member[ID]['name'] = name
            self._member[ID]['msg'].append(self.size_msg)
        else:
            self._member[ID] = {
                'name': name,
                'msg': [self.size_msg]
            }

        format_msg = (Time, ID, msg)
        self._msg.append(format_msg)
        self._countmsg += 1

        t_end = self.when_end
        if Time < t_end:
            self.is_t_sorted = False

    def search(self, t_beg, t_end, kwd: str = None, mode='member', ID=None, regular=False, redetails=False) -> str:
        assert t_beg <= t_end
        assert mode in ('member', 'time')
        assert len(t_beg) >= 3 and len(t_end) >= 3
        t_beg, t_end = t_beg[:3], t_end[:3]

        out_str = ''
        if t_beg == t_end:
            out_str += "{}-{}-{}期间检索到".format(*t_beg)
        else:
            out_str += "{}-{}-{}:{}-{}-{}期间检索到".format(*(t_beg + t_end))

        if ID is None:
            member = self._member
        elif ID in self._member:
            member = OrderedDict({ID: self._member[ID]})
        else:
            member = self._member

        iskwd = False if kwd is None else True
        self.sort_time()

        if mode == 'time':
            count = []
            date = []
            count_day = '' if iskwd else 0
            lower, upper = t_beg, date_add(t_beg)

            if len(member.keys()) == 1:
                _msg = [[self._msg[i] for i in state['msg']]
                        for _, state in member.items()]
                _msg = _msg[0]
            else:
                _msg = self._msg

            # this is a trick
            _msg.append((date_add(t_end), None, ''))
            quit_flag = False
            for format_msg in _msg:
                t_msg = format_msg[0][:3]
                if t_msg < lower:
                    continue
                while t_msg >= upper:
                    if iskwd:
                        if regular:
                            reg = re.compile(r'%s' % kwd, flags=re.MULTILINE)
                            result = reg.findall(count_day)
                            count.append(len(result))
                        else:
                            count.append(count_day.count(kwd))
                    else:
                        count.append(count_day)
                    count_day = '' if iskwd else 0
                    date.append('-'.join(['%02d' % x for x in lower]))

                    lower, upper = date_add(lower), date_add(upper)
                    if lower > t_end:
                        quit_flag = True
                        break
                if quit_flag:
                    break
                count_day += format_msg[2] if iskwd else 1
            _msg.pop()

            lower = date_add(lower)
            while lower <= t_end:
                count.append(0)
                date.append(lower)
                lower = date_add(lower)

            if iskwd:
                if regular:
                    out_str += "正则式\'{}\'{}次".format(kwd, sum(count))
                else:
                    out_str += "关键词\'{}\'{}次".format(kwd, sum(count))
            else:
                out_str += "消息{}条".format(sum(count))

            count_zero = 0
            tmp_str = ''
            max_count = max(count)
            if max_count == 0:
                return out_str

            widstr = str(WIDTH-9) if kwd else str(WIDTH-8)
            widcount = str(len(str(max_count)))
            out_str = (
                "  {:^"+widstr+"}    {:^8}    {:^2}\n").format(out_str, '日期', '次数')
            crossline = '-'*(len(out_str)+12)
            out_str = crossline + '\n' + out_str + crossline + '\n'
            format_str = "  {:>"+widstr+"}    {:^10}    {:^"+widcount+"}\n"

            for i, j in zip(count, date):
                if i == 0:
                    count_zero += 1
                    tmp_str += format_str.format(
                        proportion_visualize(i, max_count), j, i)
                elif tmp_str != '':
                    if count_zero > 2:
                        len_str = "%d" % len(crossline)
                        tmp_str = ("{:^"+len_str+"}\n").format("...")
                    tmp_str += format_str.format(
                        proportion_visualize(i, max_count), j, i)
                    out_str += tmp_str
                    count_zero = 0
                    tmp_str = ''
                else:
                    out_str += format_str.format(
                        proportion_visualize(i, max_count), j, i)
                    count_zero = 0
                    tmp_str = ''
            out_str += crossline + '\n'
        else:

            count_member = {key: 0 for key in member.keys()}

            lower, upper = t_beg, date_add(t_end)

            outmsg = {key: [] for key in member.keys()}

            if t_beg == self.when_beg[:3] and t_end == self.when_end[:3]:
                if not iskwd:
                    for ID, state in member.items():
                        count_member[ID] = len(state['msg'])
                        outmsg[ID] = state['msg']
                else:
                    if regular:
                        reg = re.compile(r'%s' % kwd, flags=re.MULTILINE)
                    for ID, state in member.items():
                        for id_msg in state['msg']:
                            msg = self._msg[id_msg][2]
                            if regular:
                                result = reg.findall(msg)
                                C = len(result)
                            else:
                                C = msg.count(kwd)

                            if C > 0:
                                if redetails:
                                    outmsg[ID].append(id_msg)
                                count_member[ID] += C
            elif not iskwd:
                for ID, state in member.items():
                    for id_msg in state['msg']:
                        format_msg = self._msg[id_msg]
                        t_msg = format_msg[0][:3]
                        if t_msg < lower or t_msg >= upper:
                            continue
                        count_member[ID] += 1
                        if redetails:
                            outmsg[ID].append(id_msg)
            else:
                if regular:
                    reg = re.compile(r'%s' % kwd, flags=re.MULTILINE)
                for ID, state in member.items():
                    for id_msg in state['msg']:
                        format_msg = self._msg[id_msg]
                        t_msg = format_msg[0][:3]
                        if t_msg < lower or t_msg >= upper:
                            continue
                        if regular:
                            result = reg.findall(format_msg[2])
                            C = len(result)
                        else:
                            C = format_msg[2].count(kwd)

                        if C > 0:
                            if redetails:
                                outmsg[ID].append(id_msg)
                            count_member[ID] += C

            total = sum(count_member.values())
            if kwd:
                if regular:
                    out_str += "正则式\'{}\'{}次".format(kwd, total)
                else:
                    out_str += "关键词\'{}\'{}次".format(kwd, total)
            else:
                out_str += "消息{}条".format(total)

            max_count = max(count_member.values())
            if max_count == 0:
                return out_str

            count_member = sorted(count_member.items(),
                                  key=lambda item: item[1], reverse=True)

            widstr = WIDTH-9 if kwd else WIDTH-8    # 8 chinese characters
            widthname = max([len(self._member[x]['name'])
                             for x, _ in count_member])
            widcount = len(str(max_count))
            out_str = ("  {:^{}}    {:^{}}    {}\n").format(
                out_str, widstr, '次数', widcount-2,  '昵称')
            crossline = '-'*(len(out_str)+12)
            out_str = crossline + '\n' + out_str + crossline + '\n'
            format_str = "  {:>"+str(widstr)+"}    {:^" + \
                str(widcount)+"}    {}\n"

            for k, (i, j) in enumerate(count_member):
                if WIDTH * j // max_count == 0:
                    out_str += format_str.format(proportion_visualize(
                        sum([x for _, x in count_member[k:]]), max_count), sum([x for _, x in count_member[k:]]),  '其他')
                    break
                else:
                    out_str += format_str.format(proportion_visualize(
                        j, max_count), j,  self._member[i]['name'])
            out_str += crossline + '\n'

            if redetails:
                for ID in outmsg:
                    if len(outmsg[ID]) == 0:
                        continue
                    out_str += '{:^{}}\n'.format("{}发送了{}次".format(
                        self._member[ID]['name'], len(outmsg[ID])), len(crossline)-4)
                    out_str += crossline + '\n'
                    for i in outmsg[ID]:
                        Time, ID, messages = self._msg[i]
                        out_str += '{:4d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d} {}({})\n{}'.format(
                            *Time, self._member[ID]['name'], ID, messages)
                    out_str += crossline + '\n'
        return out_str


def proportion_visualize(this, max_count):
    if max_count == 0:
        width_this = int(0)
    else:
        width_this = int(this/max_count*WIDTH)
    return ("{:>{}}").format('█'*width_this, WIDTH)


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


def msgmerge(record: RecordData, outfile):
    # content = [[Time, ID, Msg], ...]
    # Time = [Year, Month, Day, Hour, Minute, Second]
    # ID = 'Name(ID)'
    # Msg = '...'
    print("合并中...")
    msg = record._msg
    with open(outfile, 'w') as fo:
        fo.write('MSG merged at %s.\n\n' % DATE)
        for Time, ID, messages in msg:
            fo.write('%d-%02d-%02d %02d:%02d:%02d %s(%s)\n%s' %
                     (*Time, record._member[ID]['name'], ID, messages))
    print('文件合并完毕: {}'.format(outfile))


def menu(record: RecordData):

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', type=str, default='', metavar='time', dest='time',
                        help="在指定日期范围内搜索，示例：1.190611 2.<date begin>[:<date end>]")
    parser.add_argument('-k', type=str, default='', metavar='word', dest='kwd',
                        help="指定关键词，不可与-r共同使用.")
    parser.add_argument('-r', type=str, default='', metavar='pattern', dest='reg',
                        help="使用正则表达式搜索，不可与-k共同使用.")
    parser.add_argument('-a', action="store_true", default=False, dest='isall',
                        help="统计所有信息，会覆盖其他参数（-k -r -t）.")
    parser.add_argument('-m', action="store_true", default=False, dest='ismem',
                        help="按照成员发言数输出（默认为按日期输出）.")
    parser.add_argument('-d', action="store_true", default=False, dest='require_details',
                        help="输出详细信息.")
    parser.add_argument('-n', type=str, default=None, dest='name', metavar='name|ID',
                        help="查询特定用户发言.")
    parser.add_argument('-e', action="store_true", default=False, dest='exit',
                        help=" 退出（或Ctrl+c）.")
    parser._actions[0].help = "显示当前信息."
    parser.print_help()

    while True:
        argstring = ''
        while(argstring == ''):
            sys.stdin.flush()
            sys.stdout.flush()
            argstring = input('>>> ')
        try:
            args = parser.parse_args(shlex.split(argstring))
        except SystemExit:
            continue

        if args.exit:
            return

        if args.isall:
            outstr = record.search(
                record.when_beg, record.when_end, mode='time')
            print(outstr)
            continue

        if args.reg != '' and args.kwd != '':
            print("不能同时使用正则表达式-r和关键词检索-k.")
            continue

        regular = True if args.reg != '' else False

        keyword = None
        if args.kwd != '':
            keyword = args.kwd

        if args.reg != '':
            keyword = args.reg

        t_beg, t_end = record.when_beg, record.when_end
        if args.time != '':
            '''
            190511
            190305:190412
            :190412
            190305:
            :-5
            +10:
            190305:190412+5
            '''
            def _gettime(t, default_date):
                if '-' in t:
                    date, adder = (' '+t).split('-')
                    date = date.strip()
                    if date == '':
                        date = default_date
                    else:
                        date = [2000+int(date[:2]),
                                int(date[2:4]), int(date[4:6])]
                    adder = int(adder)
                    return date_add(date[:3], -adder)
                elif '+' in t:
                    date, adder = (' '+t+' ').split('+')
                    date, adder = date.strip(), adder.strip()

                    if date != '' and len(date) < len(adder):
                        date, adder = adder, date

                    if date == '':
                        date = default_date
                    else:
                        date = [2000+int(date[:2]),
                                int(date[2:4]), int(date[4:6])]
                    adder = int(adder)
                    return date_add(date[:3], adder)
                elif t == '':
                    return default_date
                else:
                    return [2000+int(t[:2]), int(t[2:4]), int(t[4:6])]

            if ':' in args.time:
                ts = args.time.split(':')
                t_beg, t_end = _gettime(ts[0], t_beg), _gettime(ts[1], t_end)
            else:
                t_beg, t_end = _gettime(
                    args.time, t_beg), _gettime(args.time, t_end)

        if args.name is not None:
            if args.name in record._member:
                name = args.name
            else:
                L = [ID for ID, state in record._member.items()
                     if state['name'] == args.name]
                if len(L) == 0:
                    print("记录中没找到群员: {}".format(args.name))
                    continue
                elif len(L) > 1:
                    print("有{}名群员都叫做: {}".format(len(L), args.name))
                    print("{}".format('  '.join(L)))
                    continue
                else:
                    name = L[0]
        else:
            name = None

        if args.ismem:
            outstr = record.search(
                t_beg, t_end, kwd=keyword, ID=name, regular=regular, redetails=args.require_details)
        else:
            outstr = record.search(t_beg, t_end, kwd=keyword, ID=name,
                                   mode='time', regular=regular, redetails=args.require_details)

        print(outstr)
        continue
