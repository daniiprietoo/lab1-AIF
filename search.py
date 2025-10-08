from utils import *
from collections import deque

class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [
            self.child_node(problem, action) for action in problem.actions(self.state)
        ]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(
            next_state,
            self,
            action,
            problem.path_cost(self.path_cost, self.state, action, next_state),
        )
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)


class Result:
    def __init__(self, solution=None, explored=0, frontier=0, last_node=None):
        self.solution = solution
        self.explored = explored
        self.frontier = frontier
        self.last_node = last_node


def breadth_first_graph_search(problem):
    """
    Search all the nodes at the present depth prior to
    moving on to the nodes at the next depth level.
    """
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return Result(solution=node, explored=0, frontier=0, last_node=node)

    frontier = deque([node])
    explored = set()
    while frontier:
        node = frontier.popleft()
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
                if problem.goal_test(child.state):
                    return Result(
                        solution=child,
                        explored=len(explored),
                        frontier=len(frontier),
                        last_node=child,
                    )
    return Result(
        solution=None, explored=len(explored), frontier=len(frontier), last_node=None
    )


def depth_first_graph_search(problem):
    """
    Search the deepest nodes in the search tree first.
    Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    Does not get trapped by loops.
    If two paths reach a state, only use the first one.
    """
    frontier = [Node(problem.initial)]  # Stack

    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return Result(
                solution=node,
                explored=len(explored),
                frontier=len(frontier),
                last_node=node,
            )
        explored.add(node.state)
        frontier.extend(
            child
            for child in node.expand(problem)
            if child.state not in explored and child not in frontier
        )
    return Result(
        solution=None, explored=len(explored), frontier=len(frontier), last_node=None
    )


def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""

    f = memoize(f, "f")
    node = Node(problem.initial)
    frontier = PriorityQueue("min", f)
    frontier.append(node)
    frontier_size = 1
    explored = set()
    while frontier:
        frontier_size = len(frontier)
        node = frontier.pop()
        if problem.goal_test(node.state):
            return Result(
                solution=node,
                explored=len(explored),
                frontier=len(frontier),
                last_node=node,
            )
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return Result(
        solution=None, explored=len(explored), frontier=frontier_size, last_node=None
    )


def astar_search(problem, h=None):
    """
    A* search: f(n) = g(n) + h(n). Uses best-first graph search.
    """
    h = memoize(h or problem.h, "h")
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))
