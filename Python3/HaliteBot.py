#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging


class HaliteBot:
    def __init__(self):
        game = hlt.Game()
        game.ready("vise")

        self.game = game

        self.shipSpawnThreshold = constants.MAX_TURNS / 2

        logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

    def run(self):
        while True:

            self.game.update_frame()

            me = self.game.me
            game_map = self.game.game_map

            command_queue = []

            for ship in me.get_ships():
                if game_map[ship.position].halite_amount < (9 * constants.MAX_HALITE / 10) or ship.is_full:
                    command_queue.append(
                        ship.move(
                            random.choice([Direction.North, Direction.South, Direction.East, Direction.West])))
                else:
                    command_queue.append(ship.stay_still())

            # If the game is in the first 200 turns and you have enough halite, spawn a ship.
            # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
            if self.game.turn_number <= self.shipSpawnThreshold and me.halite_amount >= constants.SHIP_COST \
                    and not game_map[me.shipyard].is_occupied:
                command_queue.append(me.shipyard.spawn())

            # Send your moves back to the game environment, ending this turn.
            self.game.end_turn(command_queue)
