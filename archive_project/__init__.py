import argparse
import datetime
import os
import pathlib
import subprocess
import sys


def log(message):
    print(message, file=sys.stderr, flush=True)


class UserError(Exception):
    def __init__(self, message, *args):
        super().__init__(message.format(*args))


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('source_paths', nargs='+', type=pathlib.Path)

    return parser.parse_args()


def latest_mtime(root: pathlib.Path):
    def iter_ctimes():
        for dirpath, dirnames, filenames in os.walk(root):
            for i in filenames:
                yield (pathlib.Path(dirpath) / i).lstat().st_mtime

    return max(iter_ctimes())


def main(source_paths):
    for i in source_paths:
        time = datetime.datetime.fromtimestamp(latest_mtime(i))
        dest_dir = pathlib.Path(time.strftime('~/Documents/Archive/%G/%V')).expanduser()

        dest_dir.mkdir(parents=True, exist_ok=True)

        subprocess.check_call(['archive', '-d', str(dest_dir), i])


def entry_point():
    try:
        main(**vars(parse_args()))
    except KeyboardInterrupt:
        log('Operation interrupted.')
        sys.exit(1)
    except UserError as e:
        log(f'error: {e}')
        sys.exit(2)
