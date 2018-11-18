#!/usr/bin/env python3

import pydevd
pydevd.settrace('localhost', port=2222, stdoutToServer=False, stderrToServer=False)

import HaliteBot

if __name__ == '__main__':
    bot = HaliteBot.HaliteBot()
    bot.run()