DIR_UP = "u"
DIR_DOWN = "d"
DIR_LEFT = "l"
DIR_RIGHT = "r"


def find_vacuuminator(world):
    for i in range(len(world)):
        for j in range(len(world[i])):
            if world[i][j] == 'X':
                return i, j
    return -1, -1


def path_to_next(world):
    x, y = find_vacuuminator(world)
    directions = [('u', -1, 0), ('r', 0, 1), ('d', 1, 0), ('l', 0, -1)]
    best_path = []
    for direction, dx, dy in directions:
        nx, ny = x + dx, y + dy
        while 0 <= nx < len(world) and 0 <= ny < len(world[0]):
            if world[nx][ny] == 'W':
                break
            if world[nx][ny] == 'D':
                best_path = [direction] * (abs(nx - x) + abs(ny - y))
                return best_path
            nx += dx
            ny += dy
    return best_path


def clean_path(world):
    # get the start position of the Vacuumunator
    start = -1, -1
    for i in range(len(world)):
        for j in range(len(world[i])):
            if world[i][j] == "X":
                start = (i, j)
                break
        if start != (-1, -1):
            break

    path = []
    current_pos = start
    stack = []

    while True:
        dirt_path = path_to_next(world)

        if not dirt_path:
            # no more dirt to clean, start backtracking
            if not stack:
                break  # All dirt has been cleaned
            else:
                # Go back and check for missed dirt
                backtrack = stack.pop()
                # Update the current position
                for move in backtrack:
                    world[current_pos[0]][current_pos[1]] = "E"
                    if move == DIR_UP:
                        current_pos = (current_pos[0] + 1, current_pos[1])
                        path.append(DIR_DOWN)
                    elif move == DIR_DOWN:
                        current_pos = (current_pos[0] - 1, current_pos[1])
                        path.append(DIR_UP)
                    elif move == DIR_LEFT:
                        current_pos = (current_pos[0], current_pos[1] + 1)
                        path.append(DIR_RIGHT)
                    elif move == DIR_RIGHT:
                        current_pos = (current_pos[0], current_pos[1] - 1)
                        path.append(DIR_LEFT)
                    world[current_pos[0]][current_pos[1]] = "X"
                continue  # Continue to find new dirt during backtracking
        else:
            # Set the start position to empty
            world[current_pos[0]][current_pos[1]] = "E"

            # Follow the path to clean the dirt
            stack.extend(dirt_path)
            path.extend(dirt_path)

            # Update the current position
            for move in dirt_path:
                if move == DIR_UP:
                    current_pos = (current_pos[0] - 1, current_pos[1])
                elif move == DIR_DOWN:
                    current_pos = (current_pos[0] + 1, current_pos[1])
                elif move == DIR_LEFT:
                    current_pos = (current_pos[0], current_pos[1] - 1)
                elif move == DIR_RIGHT:
                    current_pos = (current_pos[0], current_pos[1] + 1)
            # set the new start position as Vacuumunator
            world[current_pos[0]][current_pos[1]] = "X"

    return path
