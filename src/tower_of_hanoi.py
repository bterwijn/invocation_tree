
def move(towers, n, source, target, auxiliary):
    if n == 1:
        disk = towers[source].pop()
        towers[target].append(disk)
        print(f'move {disk} from {source} to {target}')
        print(towers)
    else:
        move(towers, n-1, source, auxiliary, target)
        move(towers, 1,   source, target, auxiliary)
        move(towers, n-1, auxiliary, target, source)
    
def tower_of_hanoi(n: int):
    if n <= 0:
        raise ValueError("n must be a positive integer")
    towers = {
        "A": list(range(n, 0, -1)),
        "B": [],
        "C": [],
    }    
    print("Initial state:")
    print(towers)
    print()
    move(towers, n, "A", "C", "B")  # start recursion

# Example
tower_of_hanoi(4)
