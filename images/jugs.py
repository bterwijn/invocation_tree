import copy

class Jugs:
    def __init__(self, jugs_capacity):
        self.content = [0]*len(jugs_capacity)
        self.capacity = jugs_capacity

    def __len__(self):
        return len(self.capacity)
    
    def __repr__(self):
        return ' '.join([f'{self.content[i]}/{cap}' for i,cap in enumerate(self.capacity)])
    
    def fill_action(self, jug_index):
        delta = self.capacity[jug_index] - self.content[jug_index]
        return (jug_index, delta) if delta != 0 else None

    def empty_action(self, jug_index):
        delta = -self.content[jug_index]
        return (jug_index, delta) if delta != 0 else None

    def pour_action(self, from_jug, to_jug):
        delta = min(self.capacity[to_jug] - self.content[to_jug], self.content[from_jug])
        return (from_jug, to_jug, delta) if delta != 0 else None

    def all_actions(self):
        actions = []
        for i in range(len(self)):
            a = self.fill_action(i)
            if a:
                actions.append(a)
            a = self.empty_action(i)
            if a:
                actions.append(a)
            for j in range(len(self)):
                if i != j:
                    a = self.pour_action(i, j)
                    if a:
                        actions.append(a)
        return actions
    
    def do_action(self, action, goal):
        def action_helper(jug_index, delta, goal):
            goal_reached = False
            content = self.content[jug_index]
            content += delta
            self.content[jug_index] = content
            if content == goal:
                goal_reached = True
            return goal_reached

        if len(action) == 2:
            return action_helper(action[0], action[1], goal)
        else:
            if action == (1, 0, 1):
                pass
            goal1 = action_helper(action[0], -action[2], goal)
            goal2 = action_helper(action[1],  action[2], goal)
            return goal1 or goal2

    def undo_action(self, action):
        if len(action) == 2:
            self.content[action[0]] -= action[1]
        else:
            self.content[action[0]] += action[2]
            self.content[action[1]] -= action[2]    

    def copy(self):
        return copy.deepcopy(self)
    
    def __eq__(self, other):
        if len(self) != len(other):
            return False
        # assuming 'goal' and 'capacity' are equal
        return all(self.content[i] == other.content[i] for i in range(len(self)))

    def __hash__(self):
        return hash(tuple(self.content))

def to_string(action):
    if len(action) == 2:
        jug_index, delta = action
        if delta > 0:
            return f'Fill jug {jug_index} with {delta}'
        else:
            return f'Empty jug {jug_index} with {delta}'
    else:
        from_jug, to_jug, delta = action
        return f'Pour {delta} from jug {from_jug} to jug {to_jug}'

def print_solution(jugs, visited):
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
                    print_solution(new_jugs, visited)
                    return
        generation = next_generation
    return None


goal = 4
print('Goal is to get a jug with', goal, 'liters')
jugs = Jugs((3, 5))
print('We start with jugs:',jugs)

solver_breadth_first(jugs, goal)
