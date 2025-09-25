from drilling_problem import DrillingRobotProblem, parse_grid_from_file
from search import breadth_first_graph_search, astar_search, depth_first_graph_search


def main():
    grid, start, goal = parse_grid_from_file("exampleMap.txt")
    print("Generated Grid:")
    for row in grid:
        print(row)
    print("Start:", start)
    print("Goal:", goal)
    print("\n" + "=" * 40 + "\n")

    problem = DrillingRobotProblem(grid=grid, start=start, goal=goal)
    test_all_algos(problem)


def print_solution(result, algorithm_name, problem):
    print(f"Results using {algorithm_name.upper()}:")

    if result.solution is None:
        print("No solution found.")
        if result.last_node:
            print("Path to last examined node:")
            print_path(result.last_node, algorithm_name, problem)
    else:
        print("Solution found!\n")
        print_path(result.solution, algorithm_name, problem)

    print(f"Total number of items in explored list: {result.explored}")
    print(f"Total number of items in frontier: {result.frontier}")


def print_path(node, algorithm_name, problem):
    """Print the path in the required format: (d, g(n), op, [h(n),] S)"""
    path = node.path()

    for i, current_node in enumerate(path):
        if i == 0:
            # Starting node - no operator
            if algorithm_name.lower() == "astar_search":
                h_value = problem.h(current_node)
                print(
                    f"Node {i} (starting node): ({current_node.depth}, {current_node.path_cost}, None, {h_value}, {current_node.state})\n"
                )
            else:
                print(
                    f"Node {i} (starting node): ({current_node.depth}, {current_node.path_cost}, None, {current_node.state})\n"
                )
        else:
            # Show the operator that led to this node
            operator = current_node.action
            print(f"Operator {i}: {operator}")

            # Show the resulting node
            if algorithm_name.lower() == "astar_search":
                h_value = problem.h(current_node)
                if i == len(path) - 1:
                    print(
                        f"Node {i} (final node): ({current_node.depth}, {current_node.path_cost}, {operator}, {h_value}, {current_node.state})\n"
                    )
                else:
                    print(
                        f"Node {i}: ({current_node.depth}, {current_node.path_cost}, {operator}, {h_value}, {current_node.state})\n"
                    )
            else:
                if i == len(path) - 1:
                    print(
                        f"Node {i} (final node): ({current_node.depth}, {current_node.path_cost}, {operator}, {current_node.state})\n"
                    )
                else:
                    print(
                        f"Node {i}: ({current_node.depth}, {current_node.path_cost}, {operator}, {current_node.state})\n"
                    )


def test_all_algos(problem):
    algorithms = [breadth_first_graph_search, depth_first_graph_search, astar_search]

    for algo in algorithms:
        result = algo(problem)
        print_solution(result, algo.__name__, problem)
        print("\n" + "=" * 40 + "\n")


if __name__ == "__main__":
    main()
