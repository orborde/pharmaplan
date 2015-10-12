#! /usr/bin/env python

ROTATIONS = [0, 90, 180, 270]

def search_internal(
        board, machine_list, goal,
        path_so_far, position, next_machine_index):

    # Have we placed all the machines?
    if next_machine_index == len(machine_list):
        # Check whether we've reached the goal.
        if goal == position:
            yield path_so_far
        return

    # Attempt to place the next machine at the current position.
    for angle in ROTATIONS:
        path_extn, new_position = place_machine(
            position, angle, machine_list[next_machine_index])

        # Do any of the newly placed machine tiles overlap something
        # else placed so far?
        if path_collides(path_so_far, path_extn):
            continue

        # What about hitting wall tiles?
        if path_hits_wall(path_extn, board):
            continue

        succ = search_internal(
            board, machine_list, goal,
            new_path, new_position, next_machine_index + 1)
        for soln in succ:
            yield soln


# TODO: Call search() with a machine, belt, machine, belt,
# etc. machine_list.
