#!/usr/bin/env python3


class SvmSupervisor:
    def __init__(self):
        self.shipyardMoveThreshold = 3

    def check_shipyard(self, me, ship, planned_movement):
        if ship.position != me.shipyard.position:
            return planned_movement
