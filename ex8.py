import copy
import heapq
from itertools import permutations

INF = float("inf")


class State:

    def __init__(self, path, visited, bound, cost, matrix):
        self.path = path  # List of cities visited
        self.visited = visited  # Set of visited city indices
        self.bound = bound  # Lower bound for this node
        self.cost = cost  # Accumulated path cost
        self.matrix = matrix  # Reduced matrix for this node

    def __lt__(self, other):
        # Best-First Search: priority queue orders by lowest bound
        return self.bound < other.bound


def reduce_matrix(mat):
    """Reduce matrix rows and columns and return (reduced_matrix, reduction_cost)."""
    n = len(mat)
    m = [row[:] for row in mat]
    cost = 0

    # Row reduction
    for i in range(n):
        row_min = min(m[i])
        if row_min and row_min != INF:
            cost += row_min
            m[i] = [x - row_min if x != INF else INF for x in m[i]]

    # Column reduction
    for j in range(n):
        col_min = min(m[i][j] for i in range(n))
        if col_min and col_min != INF:
            cost += col_min
            for i in range(n):
                if m[i][j] != INF:
                    m[i][j] -= col_min

    return m, cost


def compute_lower_bound(parent_node, next_city, n):
    """Compute the lower bound and reduced matrix when moving to next_city."""
    curr_city = parent_node.path[-1]

    # Copy parent's matrix
    new_mat = [row[:] for row in parent_node.matrix]

    # Set row of curr_city and col of next_city to INF
    for j in range(n):
        new_mat[curr_city][j] = INF
    for i in range(n):
        new_mat[i][next_city] = INF

    # Prevent premature return to starting city
    new_mat[next_city][0] = INF

    # Reduce matrix
    reduced_mat, reduction_cost = reduce_matrix(new_mat)

    # Calculate new lower bound
    edge_cost = parent_node.matrix[curr_city][next_city]
    new_bound = parent_node.bound + edge_cost + reduction_cost

    return reduced_mat, new_bound


def tsp_branch_bound(cost_matrix, n):
    """Branch and Bound TSP Solver."""
    # Compute initial reduced matrix and bound
    initial_mat, initial_lb = reduce_matrix(cost_matrix)

    root = State(
        path=[0],
        visited={0},
        bound=initial_lb,
        cost=0,
        matrix=initial_mat,
    )

    Q = []
    heapq.heappush(Q, root)

    best_cost = INF
    best_path = []

    while Q:
        node = heapq.heappop(Q)

        # Prune if bound exceeds or equals best cost found so far
        if node.bound >= best_cost:
            continue

        # Complete tour evaluation
        if len(node.path) == n:
            tour_cost = node.cost + cost_matrix[node.path[-1]][0]
            if tour_cost < best_cost:
                best_cost = tour_cost
                best_path = node.path + [0]
        else:
            # Branching to unvisited cities
            for c in range(n):
                if c not in node.visited:
                    edge_cost = cost_matrix[node.path[-1]][c]
                    if edge_cost == INF:
                        continue

                    new_cost = node.cost + edge_cost
                    new_mat, new_bound = compute_lower_bound(node, c, n)

                    if new_bound < best_cost:
                        new_state = State(
                            path=node.path + [c],
                            visited=node.visited | {c},
                            bound=new_bound,
                            cost=new_cost,
                            matrix=new_mat,
                        )
                        heapq.heappush(Q, new_state)

    return best_path, best_cost


def tsp_brute_force(cost, n):
    """Brute force solver for verification."""
    cities = list(range(1, n))
    best_cost = INF
    best_path = None

    for perm in permutations(cities):
        path = [0] + list(perm) + [0]
        c = sum(cost[path[i]][path[i + 1]] for i in range(n))
        if c < best_cost:
            best_cost = c
            best_path = path

    return best_path, best_cost


# --- Execution ---
if __name__ == "__main__":
    # 5-City Cost Matrix
    cost = [
        [INF, 10, 8, 9, 7],
        [10, INF, 10, 5, 6],
        [8, 10, INF, 8, 9],
        [9, 5, 8, INF, 6],
        [7, 6, 9, 6, INF],
    ]
    n = 5
    cities = ["A", "B", "C", "D", "E"]

    # Display Cost Matrix
    print("5-City TSP - Cost Matrix:")
    print(f'{"":>4}', " ".join(f"{c:>5}" for c in cities))
    for i, row in enumerate(cost):
        r = ["INF" if x == INF else str(x) for x in row]
        print(f"{cities[i]:>4}", " ".join(f"{v:>5}" for v in r))
    print("-" * 35)

    # Solve using Brute Force
    bf_path, bf_cost = tsp_brute_force(cost, n)
    bf_named_path = " -> ".join(cities[i] for i in bf_path)
    print(f"Brute Force Result  : Cost = {bf_cost} | Path = {bf_named_path}")

    # Solve using Branch and Bound
    bb_path, bb_cost = tsp_branch_bound(cost, n)
    bb_named_path = " -> ".join(cities[i] for i in bb_path)
    print(f"Branch & Bound Result: Cost = {bb_cost} | Path = {bb_named_path}")