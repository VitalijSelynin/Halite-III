#!/usr/bin/env python3

import pydevd
pydevd.settrace('localhost', port=2222, stdoutToServer=False, stderrToServer=False)

import SVMBot


class SvmBot(SVMBot.SVMBot):
    def __init__(self):
        super().__init__("MyBot.svc")


if __name__ == '__main__':
    bot = SvmBot()
    bot.run()
