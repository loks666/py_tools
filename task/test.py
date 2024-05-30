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


if __name__ == '__main__':
    # Task 3: Path to Next
    print("\nTask 3: Path to Next")
    print(path_to_next([['E', 'D'], ['E', 'X']]))  # Expected: ['u']
    print(path_to_next([['E', 'D'], ['E', 'E'], ['E', 'X']]))  # Expected: ['u', 'u']
    print(path_to_next([['D', 'E'], ['E', 'X']]))  # Expected: []
