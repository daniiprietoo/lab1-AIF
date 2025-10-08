from drilling_problem import DrillingRobotProblem
from utils import parse_grid_from_file, generate_grid
from search import breadth_first_graph_search, astar_search, depth_first_graph_search
import statistics


def main():
    print("Drilling Robot Search")
    print("1. Run single example test (using exampleMap.txt)")
    print("2. Run single example test (using random n x n grid)")
    print(
        "3. Run performance analysis (for 3x3, 5x5, 7x7, 9x9 maps for all algorithms)"
    )

    choice = input("Your choice (1/2/3): ").strip()

    if choice == "1":
        print("Choose algorithm:")
        print("1. Breadth-first search")
        print("2. Depth-first search")
        print("3. A* search with heuristic")
        print("4. Run all algorithms")
        algo_choice = input("Your choice (1/2/3/4): ").strip()

        algorithms = {
            "1": breadth_first_graph_search,
            "2": depth_first_graph_search,
            "3": astar_search,
        }

        if algo_choice not in algorithms and algo_choice != "4":
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
            return
        if algo_choice == "4":
            test_single_example(breadth_first_graph_search)
            test_single_example(depth_first_graph_search)
            test_single_example(astar_search)
        else:
            test_single_example(algorithms[algo_choice])

    elif choice == "2":
        input_n = input("Enter grid size n for n x n grid: ").strip()
        if input_n and not input_n.isdigit():
            print("Invalid input. Please enter a valid integer.")
            return

        print("Choose algorithm:")
        print("1. Breadth-first search")
        print("2. Depth-first search")
        print("3. A* search with heuristic")
        print("4. Run all algorithms")
        algo_choice = input("Your choice (1/2/3/4): ").strip()

        algorithms = {
            "1": breadth_first_graph_search,
            "2": depth_first_graph_search,
            "3": astar_search,
        }

        if algo_choice not in algorithms and algo_choice != "4":
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
            return
        if algo_choice == "4":
            test_single_example_random(int(input_n), breadth_first_graph_search)
            test_single_example_random(int(input_n), depth_first_graph_search)
            test_single_example_random(int(input_n), astar_search)
        else:
            test_single_example_random(int(input_n), algorithms[algo_choice])

    elif choice == "3":
        input_simulations = input(
            "Number of simulations per map size (default 5): "
        ).strip()
        if input_simulations and not input_simulations.isdigit():
            print("Invalid input. Please enter a valid integer.")
            return
        run_performance_analysis(int(input_simulations))

    else:
        print("Invalid choice. Please enter 1 or 2.")


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
    path = node.path()

    print(
        "Format of the nodes: (depth, g(n) -> accumulated cost, operator, [h(n)] (if h), state)\n"
    )
    for i, current_node in enumerate(path):
        if i == 0:
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
            operator = current_node.action
            print(f"Operator {i}: {operator}")
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


def run_performance_analysis(num_simulations):
    map_dims = [3, 5, 7, 9]
    print("\n")
    print("Comparison of Performance:")
    print("=" * 80)
    print(f"{num_simulations} simulations for each map size: 3x3, 5x5, 7x7, 9x9")
    print("Start: (0,0,0), Goal: (N-1,N-1,8) for each map")
    print("\n")

    for n in map_dims:
        results = run_simulations_for_size(n, num_simulations)
        print_results_table(n, results)


def run_simulations_for_size(n, num_simulations):
    algorithms = [
        ("Breadth-first", breadth_first_graph_search),
        ("Depth-first", depth_first_graph_search),
        ("A* (h)", astar_search),
    ]

    algorithm_results = {name: [] for name, _ in algorithms}

    for _ in range(num_simulations):
        grid, start, goal = generate_grid(n, n)
        problem = DrillingRobotProblem(grid=grid, start=start, goal=goal)

        for algo_name, algo_func in algorithms:
            result = algo_func(problem)

            if result and result.solution:
                # metrics
                d = result.solution.depth  # depth of solution
                g = result.solution.path_cost  # cost of solution path
                explored = result.explored  # number of explored nodes
                frontier = result.frontier  # final frontier size

                algorithm_results[algo_name].append(
                    {"d": d, "g": g, "explored": explored, "frontier": frontier}
                )
            else:
                # No solution found
                algorithm_results[algo_name].append(
                    {
                        "d": -1,  # -1 for no solution
                        "g": -1,
                        "explored": result.explored if result else 0,
                        "frontier": result.frontier if result else 0,
                    }
                )

    return algorithm_results


def calculate_averages(results_list):
    if not results_list:
        return {"d": 0, "g": 0, "explored": 0, "frontier": 0}

    # Calculate averages for successful runs only
    return {
        "d": statistics.mean([r["d"] for r in results_list]),
        "g": statistics.mean([r["g"] for r in results_list]),
        "explored": statistics.mean([r["explored"] for r in results_list]),
        "frontier": statistics.mean([r["frontier"] for r in results_list]),
    }


def print_results_table(n, algorithm_results):
    print(f"Table: Comparative performance of search methods in {n}x{n} maps")
    print(f"{'='*60}")
    print(f"{'Algorithm':<15} {'d':<8} {'g':<10} {'#E':<8} {'#F':<8}")
    print(f"{'-'*60}")

    for algo_name in ["Breadth-first", "Depth-first", "A* (h)"]:
        results = algorithm_results[algo_name]
        averages = calculate_averages(results)

        # Format the output
        d_str = f"{averages['d']:.1f}"
        g_str = f"{averages['g']:.1f}"
        e_str = f"{averages['explored']:.1f}"
        f_str = f"{averages['frontier']:.1f}"

        print(f"{algo_name:<15} {d_str:<8} {g_str:<10} {e_str:<8} {f_str:<8}")

    print(f"{'-'*60}")
    print("\n")


def test_single_example(algorithm):
    grid, start, goal = parse_grid_from_file("exampleMap.txt")
    print("\n")
    print("Generated Grid:")
    for row in grid:
        print(row)
    print("Start:", start)
    print("Goal:", goal)
    print("\n" + "=" * 40 + "\n")

    problem = DrillingRobotProblem(grid=grid, start=start, goal=goal)
    result = algorithm(problem)
    print_solution(result, algorithm.__name__, problem)
    print("\n" + "=" * 40 + "\n")


def test_single_example_random(n, algorithm):
    grid, start, goal = generate_grid(n, n)
    print("\n")
    print("Generated Grid:")
    for row in grid:
        print(row)
    print("Start:", start)
    print("Goal:", goal)
    print("\n" + "=" * 40 + "\n")

    problem = DrillingRobotProblem(grid=grid, start=start, goal=goal)

    result = algorithm(problem)
    print_solution(result, algorithm.__name__, problem)
    print("\n" + "=" * 40 + "\n")


if __name__ == "__main__":
    main()
