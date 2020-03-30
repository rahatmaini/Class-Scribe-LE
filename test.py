import select
import sys
import time


def get_user_input(msg, timeout=5):
    print(msg)
    user_input = []
    stime = time.time()

    while time.time() - stime <= timeout:
        readables, _, _ = select.select([sys.stdin], [], [], 0.1)
        if not readables:
            continue
        chr = readables[0].read(1)
        if chr == '\n':
            return ''.join(user_input)
        user_input.append(chr)

user_input = get_user_input('please insert something:')

if user_input is None:
    print('no user input')
else:
    print('input is %s' % user_input)