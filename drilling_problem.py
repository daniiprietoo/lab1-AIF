from search import Problem
from utils import manhattan_distance
import random


class DrillingRobotProblem(Problem):
    # 8 possible orientations: indices 0-7 correspond to N, NE, E, SE, S, SW, W, NW
    ORIENTATIONS = [
        (-1, 0),  # 0: North (up)
        (-1, 1),  # 1: Northeast
        (0, 1),  # 2: East (right)
        (1, 1),  # 3: Southeast
        (1, 0),  # 4: South (down)
        (1, -1),  # 5: Southwest
        (0, -1),  # 6: West (left)
        (-1, -1),  # 7: Northwest
    ]

    def __init__(self, grid, start, goal):
        self.grid = grid
        self.goal = goal
        initial_state = (
            start[0],
            start[1],
            start[2],
        )  # (x, y, orientation_index)
        super().__init__(initial_state, goal)

    # We can assusme that the grid is rectangular, (from the problem statement)
    def is_valid_position(self, row, column):
        rows = len(self.grid)
        columns = len(self.grid[0])
        return 0 <= row < rows and 0 <= column < columns

    def actions(self, state):
        (row, column, orientation) = state

        actions = ["rotate_left", "rotate_right"]

        delta_row, delta_column = self.ORIENTATIONS[
            orientation
        ]  # Get direction vector from orientation index
        new_row, new_column = row + delta_row, column + delta_column

        if self.is_valid_position(new_row, new_column):
            actions.append("move_forward")

        return actions

    def result(self, state, action):
        (row, column, orientation) = state

        match action:
            case "rotate_left":
                new_orientation = (orientation - 1) % len(self.ORIENTATIONS)
                return (row, column, new_orientation)
            case "rotate_right":
                new_orientation = (orientation + 1) % len(self.ORIENTATIONS)
                return (row, column, new_orientation)
            case "move_forward":
                delta_row, delta_column = self.ORIENTATIONS[orientation]
                new_row, new_column = row + delta_row, column + delta_column
                if self.is_valid_position(new_row, new_column):
                    return (new_row, new_column, orientation)
                else:
                    return state
            case _:
                return state

    def goal_test(self, state):
        """Check if the current state is the goal state."""
        (row, column, orientation) = state
        if (row, column) != (self.goal[0], self.goal[1]):
            return False

        if self.goal[2] is not None:
            return orientation == self.goal[2]

        return True

    def path_cost(self, c, state1, action, state2):
        if action == "move_forward":
            (row, column, _) = state2
            return (
                c + self.grid[row][column]
            )  # moving into a cell has the cost of that cell
        else:
            return c + 1  # rotate actions have a cost of 1

    def h(self, node):
        (row, column, _) = node.state
        (goal_row, goal_column, _) = self.goal
        return manhattan_distance((row, column), (goal_row, goal_column))


def generate_grid(rows, columns):
    return [[random.randint(1, 9) for _ in range(columns)] for _ in range(rows)]


def parse_grid_from_file(file_path):
    grid = []
    with open(file_path, "r") as file:
        line = file.readline().strip()
        rows, _ = map(int, line.split())
        for _ in range(rows):
            line = file.readline().strip()
            grid.append(list(map(int, line.split())))

        line = file.readline().strip()
        start_row, start_column, start_orientation = map(int, line.split())
        start = (start_row, start_column, start_orientation)

        line = file.readline().strip()
        goal_row, goal_column, goal_orientation = map(int, line.split())
        goal = (goal_row, goal_column, goal_orientation)

    return grid, start, goal
