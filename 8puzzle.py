import heapq

class PuzzleNode:
    def __init__(self, state, parent=None, move=""):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __lt__(self, other):
        return (self.depth + self.heuristic()) < (other.depth + other.heuristic())

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))

    def __repr__(self):
        return f"Depth: {self.depth}\nMove: {self.move}\nState:\n{self.state}\n"

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j

    def get_children(self):
        blank_row, blank_col = self.find_blank()
        children = []
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in moves:
            new_row, new_col = blank_row + dr, blank_col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_state = [row[:] for row in self.state]
                new_state[blank_row][blank_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[blank_row][blank_col]
                children.append(PuzzleNode(new_state, self, f"Move tile {self.state[new_row][new_col]} {dr, dc}"))
        return children

    def heuristic(self):
        # Manhattan distance heuristic
        goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0:
                    value = self.state[i][j]
                    goal_row, goal_col = divmod(value - 1, 3)
                    distance += abs(i - goal_row) + abs(j - goal_col)
        return distance

def solve_puzzle(initial_state):
    start_node = PuzzleNode(initial_state)
    heap = [start_node]
    visited = set()

    while heap:
        current_node = heapq.heappop(heap)
        if current_node.state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
            path = []
            while current_node:
                path.append(current_node)
                current_node = current_node.parent
            return path[::-1]
        
        visited.add(current_node)
        children = current_node.get_children()
        for child in children:
            if child not in visited:
                heapq.heappush(heap, child)

    return None

# Example usage:
initial_state = [
    [1, 2, 3],
    [4, 0, 5],
    [7, 8, 6]
]

solution = solve_puzzle(initial_state)
if solution:
    for index, node in enumerate(solution):
        print(f"Step {index + 1}:")
        print(node)
else:
    print("No solution found.")
