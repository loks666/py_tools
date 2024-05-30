def make_move(world, direction):
    x, y = find_vacuuminator(world)
    dx, dy = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}.get(direction, (0, 0))
    nx, ny = x + dx, y + dy
    if 0 <= nx < len(world) and 0 <= ny < len(world[0]) and world[nx][ny] != 'W':
        if world[nx][ny] == 'D':
            world[nx][ny] = 'E'
        world[x][y], world[nx][ny] = world[nx][ny], 'X'
    return world


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
    path = []
    start_positions = find_vacuuminator(world)
    visited = set()  # To keep track of visited positions

    # Clean all visible dirt first
    while True:
        next_path = path_to_next(world)
        if not next_path:
            break
        path += next_path
        for move in next_path:
            world = make_move(world, move)
            visited.add((find_vacuuminator(world)))  # Mark the new position as visited

    # Backtracking to start position and scanning for new dirt
    current_position = find_vacuuminator(world)
    while current_position != start_positions:
        # Move towards start position if no new dirt is found
        move_towards_start = calculate_move_towards_start(current_position, start_positions)
        world = make_move(world, move_towards_start)
        path.append(move_towards_start)
        current_position = find_vacuuminator(world)

    # After backtracking, start a new cleaning cycle if there's any dirt left
    while True:
        next_path = path_to_next(world)
        if not next_path:
            break
        path += next_path
        for move in next_path:
            world = make_move(world, move)
            visited.add((find_vacuuminator(world)))  # Mark the new position as visited

    return path


def calculate_move_towards_start(current, start):
    if current[0] > start[0]:
        return 'u'
    elif current[0] < start[0]:
        return 'd'
    elif current[1] > start[1]:
        return 'l'
    elif current[1] < start[1]:
        return 'r'


if __name__ == '__main__':
    # Task 3: Path to Next
    print("\nTask 3: Path to Next")
    print(path_to_next([['E', 'D'], ['E', 'X']]))  # Expected: ['u']
    print(path_to_next([['E', 'D'], ['E', 'E'], ['E', 'X']]))  # Expected: ['u', 'u']
    print(path_to_next([['D', 'E'], ['E', 'X']]))  # Expected: []

    # Task 4: Clean Path
    print("\nTask 4: Clean Path")
    print(clean_path([['E', 'D'], ['E', 'E'], ['E', 'X']]))  # Expected: ['u', 'u', 'd', 'd']
    print(clean_path([['D', 'D'], ['E', 'E'], ['E', 'X']]))  # Expected: ['u', 'u', 'l', 'r', 'd', 'd']
    print(clean_path([['E', 'D', 'E'], ['X', 'D', 'D'], ['E', 'E', 'E']]))  # Expected: ['r', 'u', 'd', 'r', 'l', 'l']
    print(clean_path(
        [['E', 'D', 'E'], ['X', 'D', 'E'], ['E', 'D', 'E']]))  # Expected: ['r', 'u', 'd', 'd', 'u', 'u', 'd', 'l']
    print(clean_path([['E', 'D', 'D'], ['D', 'E', 'E'],
                      ['D', 'E', 'X']]))  # Expected: ['u', 'u', 'l', 'r', 'd', 'l', 'l', 'd', 'u', 'r', 'r', 'd']
