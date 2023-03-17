"""
message type:
xxxx-xx-xx xx:xx:xx 【title】NAME(ID)/【title】NAME<Email>
xxxx-xx-xx xx:xx:xx NAME(ID)/NAME<Email>
r'^\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{1,2}:\d{1,2}\s.*(\(\d+\)|<.*>)$'
"""
import os
import argparse
import datetime
import sys
import re

from typing import Iterator, Tuple, List, Union
from modules import RecordData, menu, msgmerge

width = 60
fmt_progress = "\r{}: |{:<" + str(width) + "}|"

match_time = re.compile(r"^\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{1,2}:\d{1,2}$")


def parse_text(file: str, verbose: bool = True) -> Iterator[Tuple[str, str]]:

    is_new = re.compile(
        r"(?<=\n)\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s[^\n(<]*[(<][^)>]*[)>]\n"
    )
    with open(file, "r") as fi:
        data = fi.read()
    info = is_new.findall(data)
    msg = is_new.split(data)
    assert len(info) == len(msg) - 1
    total_len = len(info)
    log_interval = max(1, total_len // width)

    for i, (line, message) in enumerate(zip(info, msg[1:])):
        yield (line, message)
        if verbose and (i + 1) % log_interval == 0:
            print(
                fmt_progress.format(file, int((i + 1) / total_len * width) * "█"),
                end="",
            )
    print(fmt_progress.format(file, width * "█"))
    return


def parse_html(file: str, verbose: bool = True) -> Iterator[Tuple[str, str]]:
    """The html file should be export from
    https://github.com/Yiyiyimu/QQ-History-Backup
    """

    with open(file, "r") as fi:
        content = fi.read()
    content = re.sub(r"<img.+?>", "[image]", content)
    content = re.sub(r"</b>|</br>|-----", "\t", content)
    content = re.sub(r"<.+?>", "", content)
    content = re.sub(r"\t+", "\t", content)
    content = content.split("\t")
    total_len = len(content)
    log_interval = max(1, total_len / 3 // width)
    try:
        for i in range(0, total_len, 3):
            name = content[i]
            _time = content[i + 1]
            if match_time.search(_time) is None:
                name, _time = _time, name
            msg = content[i + 2]

            yield (f"{_time} {name}({name})", msg)
            if verbose and (i + 1) % log_interval == 0:
                print(
                    fmt_progress.format(file, int((i + 1) / total_len * width) * "█"),
                    end="",
                )
    except IndexError:
        pass

    print(fmt_progress.format(file, width * "█"))
    return


def main(args: argparse.Namespace):

    infile = args.infile
    mergefile = args.mergefile

    record = RecordData()

    # read and process input file
    for file in args.infile:
        assert os.path.isfile(file), f"'{file}' is not found."
        if os.path.basename(file).split(".")[-1] == "html":
            parser = parse_html
        else:
            parser = parse_text

        for info, msg in parser(file, False):
            record.add_msg(info, msg)

    print(" 群员数: {} 消息数: {}".format(record.size_group, record.size_msg))

    # Only -i option, enter MENU mode
    if args.mergefile == None:
        print("交互模式")
        try:
            menu(record)
        except KeyboardInterrupt:
            print("")
    else:
        msgmerge(record, mergefile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=("QQ 消息文本搜索"),
        epilog="获取更详细帮助信息: https://github.com/maxwellzh/CRAQ/blob/master/README.md",
    )
    parser._actions[0].help = "显示当前信息."
    parser.add_argument(
        "-i",
        type=str,
        metavar="file",
        nargs="+",
        dest="infile",
        required=True,
        help="指定输入文件，只添加 -i 参数时进入菜单模式.",
    )

    parser.add_argument(
        "-m", type=str, metavar="out-file", dest="mergefile", help="整合消息记录."
    )
    args = parser.parse_args()

    main(args)
