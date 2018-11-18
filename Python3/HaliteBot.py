#!/usr/bin/env python3
# Python 3.6

import hlt
from hlt import constants
from hlt.positionals import Direction

from collections import defaultdict
import random

import logging


class ShipStates:
    Collecting = "Collecting"
    Depositing = "Depositing"


class HaliteBot:
    def __init__(self):
        game = hlt.Game()
        game.ready("vise")

        self.game = game

        self.ship_spawn_value = (constants.MAX_TURNS / 2)
        self.halite_return_value = (9 * constants.MAX_HALITE / 10)
        self.mining_prioritization_value = 3

        self.direction_order = Direction.get_all_cardinals()
        self.direction_order.append(Direction.Still)
        self.ship_states = defaultdict(lambda: ShipStates.Collecting)

        logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

    def run(self):
        while True:

            self.game.update_frame()

            me = self.game.me
            game_map = self.game.game_map
            my_ships = me.get_ships()

            command_queue = []

            for ship in my_ships:

                if ship.halite_amount >= self.halite_return_value:
                    self.ship_states[ship.id] = ShipStates.Depositing

                if self.ship_states[ship.id] is ShipStates.Collecting:
                    move = self.mine_halite(ship)
                    if move is not None:
                        command_queue.append(move)

                elif self.ship_states[ship.id] is ShipStates.Depositing:
                    move = self.move_home(ship)
                    if move is not None:
                        command_queue.append(move)

            conditions = [self.game.turn_number <= self.ship_spawn_value,
                          me.halite_amount >= constants.SHIP_COST,
                          not game_map[me.shipyard].is_occupied]
            if all(conditions):
                command_queue.append(me.shipyard.spawn())

            # Send your moves back to the game environment, ending this turn.
            self.game.end_turn(command_queue)

    def prioritize_mining(self, halite_prio_dict):
        halite_prio_dict[Direction.Still] = halite_prio_dict[Direction.Still] \
                                            * self.mining_prioritization_value

        return halite_prio_dict

    def decide_movement(self, halite_prio_dict, ship):
        if max(halite_prio_dict.values()) is 0:
            move = self.get_random_direction(ship)
        else:
            move = max(halite_prio_dict, key=halite_prio_dict.get)

        return move

    def get_random_direction(self, ship=None):
        direction_list = Direction.get_all_cardinals()
        direction = random.choice(direction_list)

        if ship is not None:
            if ship.position.directional_offset(direction) == self.game.me.shipyard.position:
                direction_list.remove(direction)
                direction = random.choice(direction_list)

        return direction

    def mine_halite(self, ship):
        position_options = ship.position.get_surrounding_cardinals() + [ship.position]
        g_map = self.game.game_map

        position_dict = {}
        halite_prio_dict = {}

        for n, direction in enumerate(self.direction_order):
            position_dict[direction] = position_options[n]

        for direction in position_dict:
            position = position_dict[direction]
            halite_amount = g_map[position].halite_amount
            halite_prio_dict[direction] = halite_amount

        halite_prio_dict = self.prioritize_mining(halite_prio_dict)

        move_position = self.decide_movement(halite_prio_dict, ship)

        source = g_map[ship.position]
        destination = g_map[ship.position.directional_offset(move_position)]
        safe_move = g_map.get_safe_move(source, destination)

        if safe_move is not None:
            g_map[ship.position.directional_offset(safe_move)].mark_unsafe(ship)
            move = ship.move(safe_move)
        else:
            if ship.position == self.game.me.shipyard.position:
                for direction in self.direction_order:
                    destination = g_map[ship.position.directional_offset(direction)]
                    safe_move = g_map.get_safe_move(source, destination)
                    if safe_move is not None:
                        g_map[ship.position.directional_offset(safe_move)].mark_unsafe(ship)
                        return ship.move(safe_move)

                move = ship.move(self.get_random_direction())
            else:
                move = None

        return move

    def move_home(self, ship):
        me = self.game.me
        g_map = self.game.game_map
        move = None

        if ship.position == me.shipyard.position:
            self.ship_states[ship.id] = ShipStates.Collecting
        else:
            movement = g_map.get_safe_move(g_map[ship.position], g_map[me.shipyard.position])
            if movement is not None:
                g_map[ship.position.directional_offset(movement)].mark_unsafe(ship)
                move = ship.move(movement)
            else:
                move = None

        return move
