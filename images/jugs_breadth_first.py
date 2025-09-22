import jugs as jg
import sys

def solver_breadth_first(jugs, goal):
    def get_actions(jugs, visited):
        actions = []
        while True:
            action = visited[jugs]
            if action is None:
                break
            actions.append(action)
            jugs.undo_action(action)
        return actions[::-1] # reverse the order

    visited = {jugs: None}
    generation = [jugs]
    generation_count = 0
    while generation:
        print(f'generation{generation_count}: ', generation)
        next_generation = []
        for jugs in generation:
            actions = jugs.all_actions()
            for action in actions:
                new_jugs = jugs.copy()
                goal_reached = new_jugs.do_action(action, goal)
                if new_jugs not in visited:
                    print(jugs, action, '->', new_jugs)
                    visited[new_jugs] = action # remember the action to get to new_jugs
                    next_generation.append(new_jugs)
                if goal_reached:
                    return get_actions(new_jugs, visited)
        generation_count += 1
        generation = next_generation
    return None

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python jugs_breadth_first.py <goal> <capacities(comma separated)>")
        sys.exit(1)
    goal = int(sys.argv[1])
    capacities = tuple(int(x) for x in sys.argv[2].split(','))
    jugs = jg.Jugs(capacities)
    print('Goal is to get a jug with', goal, 'liters.')
    print('We start with jugs:', jugs)
    solution_actions = solver_breadth_first(jugs, goal)
    if solution_actions:
        jg.print_solution(jugs, solution_actions)
    else:
        print('No solution found')