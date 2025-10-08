from utils import euclidean_distance, is_in
import random


class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


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
        self.grid_min_hardness = min(min(row) for row in grid)
        super().__init__(initial_state, goal)

    # grid is rectangular, (from the problem statement)
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
        row, column, orientation = state
        goal_row, goal_column, goal_orientation = self.goal

        if (row, column) != (goal_row, goal_column):
            return False
        if goal_orientation == 8:  # 8 means orientation is not relevant
            return True
        return orientation == goal_orientation

    def path_cost(self, c, state1, action, state2):
        # c is the cummulative cost to reach state1
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
        euclidean_dist = euclidean_distance((row, column), (goal_row, goal_column))

        return euclidean_dist * self.grid_min_hardness
