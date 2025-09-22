import invocation_tree as ivt
import jugs as jg

def solver_depth_first(jugs, goal):

    def solver_depth_first_recursive(jugs, goal, jugs_hist, action_hist):
        actions = jugs.all_actions()
        for action in actions:
            goal_reached = jugs.do_action(action, goal)
            if jugs not in jugs_hist:
                jugs_hist.add(jugs.copy())
                action_hist.append(action)
                if goal_reached:
                    return action_hist
                result = solver_depth_first_recursive(jugs, goal, jugs_hist, action_hist)   
                if result:
                    return result
                action_hist.pop()
                jugs_hist.remove(jugs)
            jugs.undo_action(action)
        return None 

    jugs_hist = {jugs}
    action_hist = []
    return solver_depth_first_recursive(jugs.copy(), goal, jugs_hist, action_hist)

if __name__ == '__main__':
    goal = 4
    print('Goal is to get a jug with', goal, 'liters')
    jugs = jg.Jugs((3, 5))
    print('We start with jugs:',jugs)
    tree = ivt.blocking()
    tree.hide_vars.add('solver_depth_first_recursive.jugs_hist')
    tree.hide_vars.add('solver_depth_first_recursive.action_hist')
    tree.ignore_calls.add('re:Jugs.*')
    solution_actions = tree(solver_depth_first, jugs, goal)
    #solution_actions = solver_depth_first( jugs, goal)
    jg.print_solution(jugs, solution_actions)
