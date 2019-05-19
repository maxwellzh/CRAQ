'''
message type:
2019-xx-xx xx:xx:xx NAME(QQ_ID)
'''
import sys
import re
import operator
import getopt


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
            for message in traversing_dict(self.talks):
                if key_word in message:
                    result += message
                    times += 1
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
                for message in traversing_dict(this[date[-1]]):
                    result += message
                    times += 1
                return times, result
            else:
                return times, result


def traversing_dict(Dict):
    if type(Dict) is not dict:
        return Dict
    for _, value in Dict.items():
        if type(value) is not dict:
            yield value
        else:
            for x in traversing_dict(value):
                yield x


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
        info = info[:2] + [''.join(info[2:])]
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
    print("-i[--file_input_loc]\t\tlocation of input file")
    print("-o[--file_output_loc]\t\tlocation of output file")
    print("-k[--key_word]\t\t\tthe key word to search")
    print("-c[--enable_count]\t\tenable count of messages Default: False")


def proportion_visualize(total, this, max_count):
    proportion = float(this/total)
    width = int(60*proportion)
    #return '占比%-5.2f%% %s%s' % (proportion*100, '.'*width, ' '*int(60*(max_count-this)/total))
    return '%s%s ' % ('.'*width, ' '*int(60*(max_count-this)/total))


def main():
    opts, _ = getopt.getopt(sys.argv[1:], '-h-i:-o:-k:-c:', ['help',
                                                             'file_input_loc', 'file_output_loc', 'key_word', 'enable_count'])
    file_loc_input = ''
    file_loc_output = ''
    key_word = ''
    enable_count = False

    for op, value in opts:
        if op == "-i" or op == "--file_input_loc":
            file_loc_input = str(value)
        elif op == "-o" or op == "--file_output_loc":
            file_loc_output = str(value)
        elif op == "-k" or op == "--key_word":
            key_word = str(value)
        elif op == "-c" or op == "--enable_count":
            enable_count = True if value == 'True' else False
        elif op == "-h" or op == "--help":
            usage()
            sys.exit()

    members = {}
    member_talking = None
    count = 0
    max_count = int(0)

    with open(file_loc_input, 'rt', encoding='utf-8') as chat_record:
        for line in chat_record:
            if line[:4] != '2019' or (line[-2] != ')' and line[-2] != '>'):
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
                member_talking = members[ID]

    count_all = int(0)
    count_ID = {}
    for ID in members.keys():
        count_ID[ID], talks = members[ID].get_talks(
            method='key word', key_word=key_word)
        max_count = max([max_count, count_ID[ID]])
        if talks != '':
            count_all += count_ID[ID]

    print("\n检索消息记录%d条" % (count))
    if enable_count:
        for ID in members.keys():
            print('发消息%d%s条\t%s\t%s' %
                  (members[ID].count, ' '*(len(str(count))-len(str(members[ID].count))), proportion_visualize(count, members[ID].count, count/2), members[ID].name))

    print("\n关键词\"%s\"出现%d次\n" % (key_word, count_all))
    for ID in count_ID.keys():
        if count_ID[ID] != 0:
            print("发送\"%s\"次数%d%s\t%s\t%s" % (
                key_word, count_ID[ID], ' '*(len(str(max_count))-len(str(count_ID[ID]))), proportion_visualize(count_all, count_ID[ID], max_count), members[ID].name))
    print('\n')

    if len(file_loc_output) > 0:
        with open(file_loc_output, 'wt', encoding='utf-8') as file_dealed:
            for ID in members.keys():
                file_dealed.write('QQ ID/EMAIL: %s\n' % (ID))
                file_dealed.write('QQ NAME: %s\n' % (members[ID].name))
                for line in traversing_dict(members[ID].talks):
                    #print(date)
                    file_dealed.write(line)


if __name__ == "__main__":
    main()
