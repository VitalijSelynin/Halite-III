#!/usr/bin/env python3

import SVMBot


class SVMBotAggressive(SVMBot.SVMBot):
    def __init__(self):
        super().__init__("MyBot.svc")


if __name__ == '__main__':
    bot = SVMBotAggressive()
    bot.run()
