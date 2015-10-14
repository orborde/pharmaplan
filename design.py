#! /usr/bin/env python

import collections

ROTATIONS = set([0, 90, 180, 270])

# TODO: This is a group-theoretic correct way of doing this, but
# probably an inefficient one. Remember to profile! :)
def rotate(row, col, angle):
    """
    >>> rotate(10, 5, 0)
    (10, 5)
    >>> rotate(10, 5, 90)
    (5, -10)
    >>> rotate(10, 5, 180)
    (-10, -5)
    >>> rotate(10, 5, 270)
    (-5, 10)
    """
    assert angle in ROTATIONS
    while angle > 0:
        angle -= 90
        row, col = col, -row
    return row, col


# MACHINE SPECIFICATIONS
#
# A machine may be either a process step OR a belt tile. Each machine
# is represented as a potential "move" through the space of the
# factory floor. This "move" has two parts:
#
# - A set of tiles that will be marked as occupied, either by the
#   machine itself or by a belt tile, and
# - A destination to which the cursor will move to place the next machine.

Machine = collections.namedtuple('Machine',
                                 ['name', 'marks', 'destination'])

# A machine's input tile (the tile from which the input draws, not the
# one containing the arrow) is always the origin of the machine's
# geometry. The input tile should always be left unmarked by the move;
# its marking is expected to happen as a result of the prior machine
# placement.
#
# The output tile will always be marked as a belt tile. Thus, machines
# can be chained directly if there is only one belt tile connecting
# them (as opposed to placing "belt" machines between them).
#
# For example, the Dissolver's specification looks like this:

DISSOLVER = Machine(
    name = 'Dissolver',
    marks = [(1,  0, 'D'),   # Place a D tile below current.
             (1, -1, 'D'),   # Place a D southwest of current.
             (0, -1, 'B')],  # Place a B(elt) west of current.
    destination = (0, -1))   # Move 1 tile west.

# A Belt is represented as another possible machine:

BELT = Machine(
    name = 'Belt',
    marks = [(0, 1, 'B')],   # Place a B(elt) to the east.
    destination = (0, 1))    # Move to the newly placed B.


# More machine definitions follow...
EVAPORATOR = Machine(
    name = 'Evaporator',
    marks = [(1, 0, 'E'),
             (1, 1, 'E'),
             (1, 2, 'B')],
    destination = (1, 2))


MACHINES = [DISSOLVER, BELT, EVAPORATOR]

# Check for bonehead mistakes in the machine specifications.
def machine_valid(m):
    # Are all the mark tiles unique?
    marks = set( (r,c) for r,c,_ in m.marks )
    if len(marks) != len(m.marks): return False

    # Does the destination get marked with a belt?
    belt_marked = False
    for r,c,mark in m.marks:
        if mark == 'B':
            if (r,c) != m.destination:
                return False
            belt_marked = True
            break
    if not belt_marked: return False

    # Is the input tile clear?
    for r,c,_ in m.marks:
        if (r,c) == (0,0): return False

    return True

assert all(machine_valid(m) for m in MACHINES)


def search_internal(
        board, machine_list, goal,
        placements, position, next_machine_index):

    # Have we placed all the machines?
    if next_machine_index == len(machine_list):
        # Check whether we've reached the goal.
        if goal == position:
            yield placements
        return

    # Attempt to place the next machine at the current position.
    for angle in ROTATIONS:
        placement_extn, new_position = place_machine(
            position, angle, machine_list[next_machine_index])

        # Do any of the newly placed machine tiles overlap something
        # else placed so far?
        if placement_collides(placements, placement_extn):
            continue

        # What about hitting wall tiles?
        if placement_hits_wall(placement_extn, board):
            continue

        new_placement = placements + placement_extn

        succ = search_internal(
            board, machine_list, goal,
            new_placement, new_position, next_machine_index + 1)
        for soln in succ:
            yield soln


# TODO: Call search() with a machine, belt, machine, belt,
# etc. machine_list. Unless there's only one belt between each
# machine, in which case you don't need to.

if __name__ == '__main__':
    import doctest
    import sys

    failures, _ = doctest.testmod()
    if failures != 0:
        sys.exit(-1)
