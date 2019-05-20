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

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class member(object):
    def __init__(self, ID, name):
        self.name = name if ID != '80000000' else '匿名用户'
        self.id = ID
        self.count = 0
        '''
        self.talks = {
          year:{
              month:{
                  day:{
                      hour:{
                          minute:{
                              second:{}
                                 }
                           }
                      }
                    }
               }
        }
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
            this[Time[-1]] = ''

        #time_dict(self.talks, Time)
        self.talks[Time[0]][Time[1]][Time[2]
                                     ][Time[3]][Time[4]][Time[5]] += line

    def new_name(self, name):
        self.name = name if self.id != '80000000' else '匿名用户'

    def get_talks(self, method='date', date=[], key_word=''):
        times = 0
        if method == 'key word':
            result = ''
            for _, message in traversing_dict(self.talks):
                if key_word in message:
                    result += message
                times += message.count(key_word)
                #print(key)
                #sys.exit()
            return times, result
        elif method == 'date':
            this = self.talks
            result = ''
            for t in date[:-1]:
                if t in this:
                    pass
                else:
                    return times, result
                this = this[t]
            if date[-1] in this:
                for _, message in traversing_dict(this[date[-1]]):
                    result += message
                    times += 1
                return times, result
            else:
                return times, result
        else:
            print("member.get_talks(...) got an illegal arg.")
            sys.exit()


def traversing_dict(Dict):
    if type(Dict) is not dict:
        return Dict
    for key, value in Dict.items():
        if type(value) is not dict:
            yield str(key), value
        else:
            for key_x, x in traversing_dict(value):
                yield str(key)+'-'+key_x, x


def time_dict(talks, Time):
    if len(Time) == 0:
        return
    if Time[0] in talks:
        if len(Time) == 1:
            return
        time_dict(talks[Time[0]], talks[1:])
    else:
        if len(Time) == 1:
            talks[Time[0]] = ''
            return
        talks[Time[0]] = {}
        time_dict(talks[Time[0]], talks[1:])


def get_info(line):
    info = line.split(' ')
    if len(info) > 3:
        info = info[:2] + [' '.join(info[2:])]
    Time = info[0].split('-')+info[1].split(':')
    Time = [int(s) for s in Time]
    #print(Time)
    name = re.search(r'.*(\(|<)', info[2]).group()[:-1]
    ID = re.search(r'(\(|<).*(\)|>)', info[2]).group()[1:-1]
    if len(ID) == 0:
        ID = re.search(r'<.*>', info[2]).group()[1:-1]

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


def proportion_visualize(total, this, max_count):

    proportion = float(this/total)
    #width_this = int(60*proportion)
    #width_max = int(60*max_count/total)
    width_this = int(this/max_count*50)
    width_max = int(50)

    return '%s%s' % ('.'*width_this, ' '*(width_max-width_this))

def timer(Time, unit, step):
    Time = dt.datetime(Time[0], Time[1], Time[2], \
        Time[3], Time[4], Time[5])
    UNIT = {
        'day': 0,
        'hour': 0,
        'minute': 0,
        'second': 0}
    if unit not in UNIT:
        print("Timer unit input error in timer(...).")
        sys.exit()
    else:
        UNIT[unit] += step
    Time += dt.timedelta(days=UNIT['day'],\
                hours=UNIT['hour'],\
                    minutes=UNIT['minute'],\
                        seconds=UNIT['second'])
    Time = [
        Time.year,
        Time.month,
        Time.day,
        Time.hour,
        Time.minute,
        Time.second
    ]

    return Time

def main():
    opts, _ = getopt.getopt(sys.argv[1:], '-h-i:-o:-k:-c', \
        ['help', 'input_loc', 'output_loc', 'key_word', 'count_enable'])
    file_loc_input = ''
    file_loc_output = ''
    key_word = ''
    enable_count = False

    for op, value in opts:
        if op == "-i" or op == "--input_loc":
            file_loc_input = str(value)
            if not path.isfile(file_loc_input):
                print("File %s not exist!" % (file_loc_input))
                sys.exit()
            elif len(file_loc_input) < 5 or file_loc_input[-4:] != '.txt':
                print("Input file supposed to be .txt format.")
                sys.exit()
        elif op == "-o" or op == "--output_loc":
            file_loc_output = str(value)
        elif op == "-k" or op == "--key_word":
            key_word = str(value)
        elif op == "-c" or op == "--count_enable":
            enable_count = True
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
    max_count_word = int(0)
    max_count_message = int(0)

    with open(file_loc_input, 'rt', encoding='utf-8') as chat_record:
        for line in chat_record:
            if line[:2] != '20' or (line[-2] != ')' and line[-2] != '>'):
                # not a new message
                if member_talking != None:
                    member_talking.add_message(Time, line)
                else:
                    continue
            else:
                # a new message
                count += 1
                ID, name, Time = get_info(line)
                if ID in members:
                    # an old member
                    members[ID].new_name(name)
                else:
                    # a new member
                    members[ID] = member(ID, name)

                #members[ID].add_message(Time)
                members[ID].count += 1
                max_count_message = max([max_count_message, members[ID].count])
                member_talking = members[ID]

    print("\n检索消息记录%d条" % (count))
    if enable_count:
        for ID in members.keys():
            print('发消息%d%s条\t%s\t%s' %
                  (members[ID].count, ' '*(len(str(count))-len(str(members[ID].count))),
                      proportion_visualize(count, members[ID].count, max_count_message), members[ID].name))

    if key_word != '':
        count_all = int(0)
        count_ID = {}
        for ID in members.keys():
            count_ID[ID], talks = members[ID].get_talks(
                method='key word', key_word=key_word)
            max_count_word = max([max_count_word, count_ID[ID]])
            if talks != '':
                count_all += count_ID[ID]

        print("\n关键词\"%s\"出现%d次\n" % (key_word, count_all))
        for ID in count_ID.keys():
            if count_ID[ID] != 0:
                print("发送\"%s\"次数%d%s\t%s\t%s" % (
                    key_word, count_ID[ID], ' ' *
                    (len(str(max_count_word))-len(str(count_ID[ID]))),
                    proportion_visualize(count_all, count_ID[ID], max_count_word), members[ID].name))
        print('\n')

    if len(file_loc_output) > 0:
        with open(file_loc_output, 'wt', encoding='utf-8') as file_dealed:
            for ID in members.keys():
                file_dealed.write('QQ ID/EMAIL: %s\n' % (ID))
                file_dealed.write('QQ NAME: %s\n' % (members[ID].name))
                for Time, line in traversing_dict(members[ID].talks):
                    Time = Time.split('-')
                    Time = Time[0]+'-'+Time[1]+'-'+Time[2] + \
                        ' '+Time[3]+':'+Time[4]+':'+Time[5] + '\n'
                    file_dealed.write(Time)
                    file_dealed.write(line)
    
    '''
    #_, who = next(iter(members.items()))
    #Time, _ = next(traversing_dict(who.talks))
    who = members['2589500860']
    Time = [2019, 5, 14, 9, 28, 33]
    #Time = [int(x) for x in Time.split('-')]
    #print(Time)
    units = ['year', 'month', 'day',\
        'hour', 'minute', 'second']
    length_time = 8000
    unit = 'minute'
    index_unit = units.index(unit)
    vec_x = []
    vec_y = []
    for _ in range(length_time):
        times, _ = who.get_talks(method='date', date=Time[:index_unit+1])
        vec_y.append(times)
        vec_x.append(str(Time[index_unit]))
        Time = timer(Time, unit, 1)
        #print(vec_y)
    #print(vec_x)
    Time_beg = [str(x) for x in timer(Time, unit, -length_time)[:index_unit+1]]
    Time_end = [str(x) for x in Time[:index_unit+1]]
    plt.plot(vec_y)
    plt.grid()
    plt.xlabel("time/%s" % (unit))
    plt.title("%s发言数量[%s]-[%s]" %\
         (who.name, '-'.join(Time_beg), '-'.join(Time_end)))
    plt.show()
    '''


if __name__ == "__main__":
    main()
