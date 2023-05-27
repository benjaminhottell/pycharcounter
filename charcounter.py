#!/usr/bin/env python3

#
# PyCharCounter (c) 2023 Benjamin Hottell
#
# Counts the occurrences of each character and prints it in CSV format.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

#
# There is significant code duplication from my other project 'pycsvrewrite'.
# While some code duplication is probably inevitable, I intend on making a
# shared library to reduce this duplication.
#

import sys
import argparse
import csv


VERSION='0.0.0'

def _csv_args_dict(
        delim=None,
        dialect=None):

    ret = {}

    if delim is not None:
        ret['delimiter'] = delim

    if dialect is not None:
        ret['dialect'] = dialect

    return ret

# an exception to represent that the user gave us bad arguments
class UserException(Exception):
    pass


def read_file_or_stdin(path):
    if path is None:
        return sys.stdin
    return open(path, 'r')


def write_file_or_stdout(path):
    if path is None:
        return sys.stdout
    return open(path, 'w')


SPECIAL_DELIMITERS = {
    '\\t': '\t',
    '\\0': '\0',
}


def get_delimiter(delim):
    if delim is None:
        return None

    if delim in SPECIAL_DELIMITERS:
        delim = SPECIAL_DELIMITERS[delim]

    if len(delim) != 1:
        specials = ', '.join(SPECIAL_DELIMITERS.keys())
        raise UserException(
            f"Delimiter must be a 1-character string, or one of: {specials}")

    return delim


def get_dialect(dialect):
    if dialect is None:
        return None

    if not dialect in csv.list_dialects():
        raise UserException('No such dialect: ' + dialect)

    return dialect

# This is a table of C-style escapes for nonprinting or otherwise 'weird'
# characters that may break interoperability with other programs.
_EVIL_KEYS = {
    "\0": "\\0",    # null character
    "\a": "\\a",    # alert, bell
    "\b": "\\b",    # backspace
    "\f": "\\f",    # formfeed (page break)
    "\n": "\\n",    # newline
    "\r": "\\r",    # carriage return
    "\t": "\\t",    # tab
    "\v": "\\v",    # horizontal tab
}

# key is expected to be a one-character string
def escape_evil_key(key):
    if key in _EVIL_KEYS:
        return _EVIL_KEYS[key]

    if not key.isprintable():
        key_hex = f'{ord(key):x}'.zfill(8)
        return f"\\U{key_hex.zfill(8)}"

    return key

def main_no_catch():
    argp = argparse.ArgumentParser()

    argp.add_argument(
        '--version',
        action='store_true', default=False,
        help='print the version and exit')

    argp.add_argument(
        '--output', '-o',
        help="path to write output to (if not specified, write to stdout)")

    argp.add_argument(
        '--input', '-i',
        help="path to read input from (if not specified, read from stdin)")

    argp.add_argument(
        '--output-delimiter', '--od',
        help="specify the delimiter of the output")

    argp.add_argument(
        '--dialects',
        action='store_true', default=False,
        help='list available dialects and exit (see --output-dialect)')

    argp.add_argument(
        '--output-dialect', '--ol',
        help="specify the CSV dialect of the output")

    args = argp.parse_args()

    if args.version:
        print(VERSION)
        return 0

    if args.dialects:
        for x in csv.list_dialects():
            print(x)
        return 0

    char_qtys : "dict[str,int]" = {}

    with read_file_or_stdin(args.input) as in_file:
        for ln in in_file:
            for c in ln:
                char_qtys[c] = char_qtys.get(c, 0) + 1
        

    with write_file_or_stdout(args.output) as out_file:

        csvwriter = csv.writer(out_file, **_csv_args_dict(
            delim=args.output_delimiter,
            dialect=args.output_dialect))

        for key in char_qtys:
            value = str(char_qtys[key])
            key = escape_evil_key(key)
            csvwriter.writerow([key, value])

    return 0


def main():
    try:
        sys.exit(main_no_catch())
    except KeyboardInterrupt as e:
        sys.exit(1)
    except UserException as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

