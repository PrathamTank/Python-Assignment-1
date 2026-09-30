import heapq

print("=== Python Module Dependency Resolver ===")

n, e = map(int, input("Enter number of modules and edges: ").split())

modules = []
module_set = set()

print("\nEnter module names:")

for i in range(n):
    name = input(f"Module {i + 1}: ").strip()
    modules.append(name)
    module_set.add(name)

graph = {module: set() for module in modules}
indegree = {module: 0 for module in modules}

print("\nEnter import relationships:")
print("Format: module_a imports module_b")

for i in range(e):
    a, b = input(f"Edge {i + 1}: ").split()

    if b not in graph[a]:
        graph[b].add(a)
        indegree[a] += 1

heap = []

for module in modules:
    if indegree[module] == 0:
        heapq.heappush(heap, module)

order = []

while heap:
    current = heapq.heappop(heap)
    order.append(current)

    for dependent in graph[current]:
        indegree[dependent] -= 1

        if indegree[dependent] == 0:
            heapq.heappush(heap, dependent)

if len(order) == n:
    print("\nValid loading order:")
    print(" ".join(order))

else:
    state = {module: 0 for module in modules}
    parent = {}
    cycle = []

    def find_cycle(node):
        state[node] = 1

        for dependent in graph[node]:

            if state[dependent] == 0:
                parent[dependent] = node

                if find_cycle(dependent):
                    return True

            elif state[dependent] == 1:
                cycle.append(dependent)

                current = node

                while current != dependent:
                    cycle.append(current)
                    current = parent[current]

                cycle.append(dependent)
                cycle.reverse()

                return True

        state[node] = 2
        return False

    for module in sorted(modules):
        if state[module] == 0:
            if find_cycle(module):
                break

    print("\nCYCLE")
    print(" ".join(cycle))