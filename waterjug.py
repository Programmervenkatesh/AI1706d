from collections import deque

class State:
    def __init__(self, jug_a, jug_b):
        self.jug_a = jug_a
        self.jug_b = jug_b
        self.path = []

    def __eq__(self, other):
        return self.jug_a == other.jug_a and self.jug_b == other.jug_b

    def __hash__(self):
        return hash((self.jug_a, self.jug_b))

def pour(state, action, capacity_a, capacity_b):
    if action == 'fillA':
        return State(capacity_a, state.jug_b)
    elif action == 'fillB':
        return State(state.jug_a, capacity_b)
    elif action == 'emptyA':
        return State(0, state.jug_b)
    elif action == 'emptyB':
        return State(state.jug_a, 0)
    elif action == 'pourAB':
        total = state.jug_a + state.jug_b
        return State(min(total, capacity_a), max(0, min(total, capacity_b)))
    elif action == 'pourBA':
        total = state.jug_a + state.jug_b
        return State(max(0, min(total, capacity_a)), min(total, capacity_b))

def water_jug_problem(capacity_a, capacity_b, target):
    initial_state = State(0, 0)
    queue = deque([initial_state])
    visited = set()

    while queue:
        current_state = queue.popleft()
        if current_state.jug_a == target or current_state.jug_b == target:
            return current_state.path + [(current_state.jug_a, current_state.jug_b)]

        visited.add(current_state)
        actions = ['fillA', 'fillB', 'emptyA', 'emptyB', 'pourAB', 'pourBA']
        for action in actions:
            new_state = pour(current_state, action, capacity_a, capacity_b)
            if new_state not in visited:
                new_state.path = current_state.path + [(current_state.jug_a, current_state.jug_b)] + [action]
                queue.append(new_state)

    return None

# Example usage:
capacity_jug_a = 4
capacity_jug_b = 3
target_amount = 2

solution = water_jug_problem(capacity_jug_a, capacity_jug_b, target_amount)
if solution:
    print(f"Solution found to measure {target_amount} liters:")
    for step in solution:
        print(step)
else:
    print("No solution found.")
