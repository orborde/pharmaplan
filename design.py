#! /usr/bin/env python

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
# etc. machine_list.

if __name__ == '__main__':
    import doctest
    import sys

    failures, _ = doctest.testmod()
    if failures != 0:
        sys.exit(-1)
