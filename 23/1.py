from collections import defaultdict
import re
from math import inf
from pprint import pprint
from dataclasses import dataclass
from typing import Literal, Optional, Union, cast
from heapq import heappop, heappush

Amphipod = Union[Literal["A"], Literal["B"], Literal["C"], Literal["D"]]
GridPoint = tuple[int, int]
HOME_ROOM: dict[Amphipod, int] = {"A": 2, "B": 4, "C": 6, "D": 8}
HOMES = set(HOME_ROOM.values())
COST: dict[Amphipod, int] = {"A": 1, "B": 10, "C": 100, "D": 1000}

#  X 0 2 4 6 8 0 ->
# Y #############
# 0 #...........#
# 1 ###B#C#B#D###
# 2   #A#D#C#A#
# 3   #########
# |    2 4 6 8
# V


def parse_state(start_str: str, part2: bool):
    """
    Parse locations in our coordinates of amphipods
    """
    start_order = re.findall(r"[ABCD]", start_str)
    locs = dict()
    i = 0
    for vert in [1, 2, 3, 4] if part2 else [1, 2]:
        for horiz in [2, 4, 6, 8]:
            locs[(horiz, vert)] = start_order[i]
            i += 1
    return locs


@dataclass
class State:
    population: dict[GridPoint, Amphipod]
    max_size: int = 2

    def pod_is_home(self, loc: GridPoint) -> bool:
        """
        Is the amphipod at its destination ?
        """
        if loc not in self.population:
            return False

        return loc[1] > 0 and loc[0] == HOME_ROOM[self.population[loc]]

    @property
    def finished(self) -> bool:
        return all(self.pod_is_home(pod) for pod in self.population.keys())

    @property
    def frozen(self) -> str:
        return "|".join(f"{k}:{v}" for k, v in sorted(self.population.items()))

    def __lt__(self, _) -> bool:
        return False

    def get_move_new_state(self, src: GridPoint, dst: GridPoint) -> "State":
        new_pop = self.population.copy()  # Copy state
        new_pop[dst] = new_pop.pop(src)  # Move pod from src to dst

        return State(new_pop, self.max_size)

    def get_move_cost(self, src: GridPoint, dst: GridPoint) -> int:
        assert ((a := self.population.get(src)) is None) ^ (
            (b := self.population.get(dst)) is None
        )
        step_cost = COST[cast(Amphipod, a or b)]

        # Horizontal distance + both vertical distancces
        return (src[1] + dst[1] + abs(src[0] - dst[0])) * step_cost

    def do_move(self, src: GridPoint, dst: GridPoint) -> tuple[int, "State"]:
        return (self.get_move_cost(src, dst), self.get_move_new_state(src, dst))

    def can_move(self, horiz: int, vert: int) -> bool:
        """Checks if the amphipod can leave its room"""
        if vert < 2:
            return True

        return all(self.population.get((horiz, i)) is None for i in range(1, vert))

    def check_hallway_movements(
        self, start: GridPoint, direction: int
    ) -> tuple[bool, list[tuple[int, "State"]]]:
        """
        Returns a tuple of:
         * whether the path to the pod's home is blocked
         * All possible states stemming from valid moves in the hallway
        """

        valid_moves = []
        h = start[0]
        home_free = False

        while 1 <= h <= 9:  # Stay in the hallway
            h = h + direction

            # Have we found the pods room ?
            if h == HOME_ROOM[self.population[start]]:
                home_free = True
                continue

            if h in HOMES:
                # Can't stop in front of another home
                continue

            if (h, 0) in self.population:
                # another amphipod is blocking the way
                break

            valid_moves.append(self.do_move(start, (h, 0)))

        return home_free, valid_moves

    def is_hallway_clear_to_home(self, h: int, target_h: int) -> bool:
        direction = 1 if target_h > h else -1
        while h != target_h:
            h += direction  # Move towards home
            if (h, 0) in self.population:  # Another pod is blocking the way
                return False

        return True

    def check_vertical_movement(
        self, start: GridPoint, target_h: int
    ) -> Optional[tuple[int, "State"]]:
        # Check that there is a clear path from start to home and if pod can enter home i.e.:
        #  - All the other pods in the home must be home
        #  - There is an empty spot

        target_v = None
        for potential_v in range(self.max_size, 0, -1):  # Check going down into room
            potential_loc = (target_h, potential_v)
            if potential_loc in self.population:
                # There is a pod of the same type that's ok
                if self.pod_is_home(potential_loc):
                    continue

                # There is a pod of a different type we cannot enter home
                break

            # There is an empty spot!
            target_v = potential_v
            break

        # There is no way to get home
        if target_v is None:
            return None

        return self.do_move(start, (target_h, target_v))

    def get_next_states(self) -> list[tuple[int, "State"]]:
        next_states = []

        for loc, pod in self.population.items():  # Loop over amphipods
            h, v = loc

            if not self.can_move(h, v):  # If the pod cannot move yet ignore it
                continue

            if self.pod_is_home(loc) and all(
                self.pod_is_home((h, i)) for i in range(v + 1, self.max_size + 1)
            ):  # Pod is home and all the other ones below it as well
                continue

            # Generate moves
            can_reach_home = None
            next_pod_states = []

            if v > 0:  # i.e. the pod is in a house
                for direction in [-1, 1]:
                    found_home, generated_states = self.check_hallway_movements(
                        loc, direction
                    )
                    can_reach_home = can_reach_home or found_home
                    next_pod_states += generated_states

            # The pod is in the hallway
            target_h = HOME_ROOM[pod]
            if can_reach_home is None:
                can_reach_home = self.is_hallway_clear_to_home(h, target_h)

            if not can_reach_home:  # Add possible moves to states and go to next pod
                next_states += next_pod_states
                continue

            if (home_state := self.check_vertical_movement(loc, target_h)) is not None:
                next_states.append(home_state)
            else:
                next_states += next_pod_states

        return next_states


def djikstra(start_state: "State") -> int:
    queue: list[tuple[int, "State"]] = [(0, start_state)]
    visited = set()
    distances = defaultdict(lambda: inf, {start_state.frozen: 0})

    while len(queue) > 0:  # Queue is not empty
        cost, current_state = heappop(queue)

        if current_state.frozen in visited:
            continue

        if current_state.finished:
            return cost

        visited.add(current_state.finished)

        for next_cost, next_state in current_state.get_next_states():
            if next_state.frozen in visited:
                continue

            total_cost = cost + next_cost
            if total_cost < distances[next_state.frozen]:
                distances[next_state.frozen] = total_cost
                heappush(queue, (total_cost, next_state))

    raise RuntimeError("No solution found...")


if __name__ == "__main__":
    print("Day 01:")
    with open("./data.txt", "r") as f:
        state = State(parse_state(f.read(), part2=False))

    with open("./data2.txt", "r") as f:
        state2 = State(parse_state(f.read(), part2=True), max_size=4)

    print(f"\t- 1: {djikstra(state)}")
    print(f"\t- 2: {djikstra(state2)}")
