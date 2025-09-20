import jugs as jg

def print_breadth_first_solution(jugs, visited):
    solution = []
    solution.append(str(jugs))
    while True:
        action = visited[jugs]
        if action is None:
            break
        solution.append('- ' + to_string(action))
        jugs.undo_action(action)
        solution.append(str(jugs))
    for line in solution[::-1]: # print in reverse order
        print(line)


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
    while generation:
        print('generation: ', generation)
        next_generation = []
        for jugs in generation:
            actions = jugs.all_actions()
            for action in actions:
                new_jugs = jugs.copy()
                goal_reached = new_jugs.do_action(action, goal)
                print(jugs, action, '->', new_jugs)
                if new_jugs not in visited:
                    visited[new_jugs] = action # remember the action to get to new_jugs
                    next_generation.append(new_jugs)
                if goal_reached:
                    return get_actions(new_jugs, visited)
        generation = next_generation
    return None

if __name__ == '__main__':
    goal = 4
    print('Goal is to get a jug with', goal, 'liters')
    jugs = jg.Jugs((3, 5))
    print('We start with jugs:',jugs)
    solution_actions = solver_breadth_first(jugs, goal)
    jg.do_actions_and_print(jugs, solution_actions)