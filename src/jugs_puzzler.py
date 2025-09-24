import jugs as jg
import sys

def solver_breadth_first(jugs, goal):
    seen_contents = set()
    visited = set()
    generation = [jugs]
    gen_count = 0
    last_new_content = None
    last_new_content_gen = -1
    no_new_content_count = 0
    while generation:
        #print(f'generation {gen_count} size: ', len(generation))
        next_generation = []
        new_contents = set()
        for jugs in generation:
            actions = jugs.all_actions()
            for action in actions:
                new_jugs = jugs.copy()
                goal_reached = new_jugs.do_action(action, goal)
                contents_set = set(new_jugs.content)
                new_contents |= contents_set - seen_contents
                seen_contents |= contents_set
                #print(jugs, action, '->', new_jugs)
                if new_jugs not in visited:
                    visited.add(new_jugs)
                    next_generation.append(new_jugs)
                #if goal_reached:
                #    return get_actions(new_jugs, visited)
        if new_contents:
            #print('gen:', gen_count,'new contents:', new_contents)
            last_new_content = new_contents
            last_new_content_gen = gen_count
        else:
            no_new_content_count += 1
            if no_new_content_count > 1:
                #print('No new content found in last few generations, stopping')
                break
        generation = next_generation
        gen_count += 1
    return last_new_content, last_new_content_gen, gen_count

def find_next_hardest_jugs_config(start_capacities, add_step):
    
    last_step = 2*(start_capacities[-1] - start_capacities[-2])
    best_gen = 0
    best_capacities = None
    best_content = None
    for step in range(last_step, last_step + add_step + 1):
        capacities = start_capacities.copy()
        capacities.append(start_capacities[-1] + step)
        jugs = jg.Jugs(tuple(capacities))
        print('Trying jugs:', jugs)
        new_content, generation, max_gen = solver_breadth_first(jugs, -1)
        print('Last new content:', new_content, 'found in generation', generation, '/', max_gen)
        if generation > best_gen:
            best_gen = generation
            best_capacities = capacities
            best_content = new_content
            print('*********************  New best:', best_gen, 'with capacities', capacities)
    print('best_gen:', best_gen)
    print('best_capacities:', ','.join(map(str, best_capacities)))
    print('best_content:', best_content)
    return best_capacities, best_content, best_gen

def find_hard_jugs_config():
    capacities = [3, 5]
    add_step = 25
    for _ in range(3):
        new_cap, content, gen = find_next_hardest_jugs_config(capacities, add_step)
        print('new capacities:', new_cap, 'content:', content, 'gen:', gen)
        capacities = new_cap


if __name__ == '__main__':
    find_hard_jugs_config()
    #print('Last new content:', new_content, 'found in generation', generation, '/', max_gen)
    #if solution_actions:
    #    jg.do_actions_and_print(jugs, solution_actions)