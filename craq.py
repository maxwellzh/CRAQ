
'''
message type:
xxxx-xx-xx xx:xx:xx 【title】NAME(ID)/【title】NAME<Email>
xxxx-xx-xx xx:xx:xx NAME(ID)/NAME<Email>
r'^\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{1,2}:\d{1,2}\s.*(\(\d+\)|<.*>)$'
'''
import os.path as path
import argparse
import datetime
import sys
import re
from modules import RecordData, menu, msgmerge

VERSION = str(datetime.date.today()).replace('-', '')
parser = argparse.ArgumentParser(description=("QQ消息文本搜索[%s]" % VERSION),
                                 epilog="获取更详细帮助信息：https://github.com/maxwellzh/CRAQ/blob/master/README.md")
parser._actions[0].help = "显示当前信息."
parser.add_argument("-i", type=str,
                    metavar="in-file",  nargs='+', dest="infile",
                    help="指定输入文件，只添加-i参数时进入菜单模式（推荐）.")

parser.add_argument("-m", type=str, metavar="out-file", dest="mergefile",
                    help="整合消息记录.")

parser.add_argument("-v", "--version", help="显示当前程序版本", action="version",
                    version=VERSION)


def main():
    args = parser.parse_args()
    # No argument error
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(-1)
    # Not specify input file but ask for behavior like "-k, -r..."
    if args.infile is None:
        print("未指定输入文件.")
        sys.exit(-1)

    infile = args.infile
    mergefile = args.mergefile

    record = RecordData()

    # read and process input file
    is_new = re.compile(
        r'(?<=\n)\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s[^\n(<]*[(<][^)>]*[)>]\n'
    )
    print("Reading...")
    width = '60'
    for file in infile:

        with open(file, 'r') as fi:
            data = fi.read()
            info = is_new.findall(data)
            msg = is_new.split(data)
            assert len(info) == len(msg) - 1
            total_len = len(info)
            log_interval = total_len//60
            for i, (line, message) in enumerate(zip(info, msg[1:])):
                record.add_msg(line, message)
                if i % log_interval == log_interval - 1:
                    print(("\r{}: |{:<"+width+"}|").format(file,
                                                           (i+1)*60//total_len * '█'), end='')
        print(" 群员数: {} 消息数: {}".format(record.size_group, record.size_msg))

    # Only -i option, enter MENU mode
    if args.mergefile == None:
        print("交互模式")
        menu(record)
    else:
        msgmerge(record, mergefile)


if __name__ == '__main__':
    main()
