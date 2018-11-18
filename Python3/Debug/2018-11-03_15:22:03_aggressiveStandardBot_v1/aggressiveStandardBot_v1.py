#!/usr/bin/env python3

import SVMBot


class SVMBotAggressive(SVMBot.SVMBot):
    def __init__(self):
        super().__init__("./Debug/2018-11-03_15:22:03_aggressiveStandardBot_v1/SVMBotAggressive.svc")


if __name__ == '__main__':
    bot = SVMBotAggressive()
    bot.run()
