
def tower_of_hanoi(n: int):
    
    def move(n, source, target, auxiliary):
        if n == 1:
            disk = tower[source].pop()
            tower[target].append(disk)
            print(f'move {disk} from {source} to {target}')
            print(tower)
        else:
            move(n-1, source, auxiliary, target)
            move(1,   source, target, auxiliary)
            move(n-1, auxiliary, target, source)
    
    if n <= 0:
        raise ValueError("n must be a positive integer")
    tower = {
        "A": list(range(n, 0, -1)),
        "B": [],
        "C": [],
    }    
    print("Initial state:")
    print(tower)
    print()
    move(n, "A", "C", "B")  # start recursion

# Example
tower_of_hanoi(4)
