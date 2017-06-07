'''Goal Oriented Behaviour

Clinton Woodward, 2015, cwoodward@swin.edu.au
Works with Python 3+

Please don't share this code without permission.

Simple decision approach.
* Choose the most pressing goal (highest insistence value)
* Find the action that fulfills this "goal" the most (ideally?, completely?)

Goal: Eat (initially = 4)
Goal: Sleep (initially = 3)

Action: get raw food (Eat -= 3)
Action: get snack (Eat -= 2)
Action: sleep in bed (Sleep -= 4)
Action: sleep on sofa (Sleep -= 2)


Notes:
* This version is simply based on dictionaries and functions.

'''
from copy import copy, deepcopy
from time import sleep

VERBOSE = True

# Global goals with initial values
goals = {
    'Eat': 4,
    'Energy': 3,
}

# Global (read-only) actions and effects
actions = {
    'Base': { 'Eat': 0},
    'Eat food': { 'Eat': -3, 'Energy': 2},
    'Eat Snack': { 'Eat': -2, 'Energy': 1},
    'deep sleep': { 'Energy': -4, 'Eat':3 },
    'nap': { 'Energy': -2, 'Eat':2 }
}

def calculate_discontent(action):
    discontent = 0
    for goal in goals:
        goal_change = 0
        for goal_i, change in list(actions[action].items()):
            if goal == goal_i:
                goal_change += change

        new_value = goals[goal] + goal_change
        discontent += goals[goal] * new_value
    
    return discontent
        
def apply_action(action):
    '''Change all goal values using this action. An action can change multiple
    goals (positive and negative side effects).
    Negative changes are limited to a minimum goal value of 0.
    '''
    for goal, change in list(actions[action].items()):
        valid_goal = True
        try:
            goals[goal]
        except KeyError:
            valid_goal = False
        if valid_goal:
            goals[goal] = goals[goal] + change

    for goal in list(goals):
        if goals[goal] < 0:
            goals[goal] = 0


def action_utility(action, goal):
    '''Return the 'value' of using "action" to achieve "goal".

    For example::
        action_utility('get raw food', 'Eat')

    returns a number representing the effect that getting raw food has on our
    'Eat' goal. Larger (more positive) numbers mean the action is more
    beneficial.
    '''
    ### Simple version - the utility is the change to the specified goal

    if goal in actions[action]:
        # Is the goal affected by the specified action?
        return -actions[action][goal]
    else:
        # It isn't, so utility is zero.
        return 0

    ### Extension
    ###
    ###  - return a higher utility for actions that don't change our goal past zero
    ###  and/or
    ###  - take any other (positive or negative) effects of the action into account
    ###    (you will need to add some other effects to 'actions')


def choose_action():
    '''Return the best action to respond to the current most insistent goal.
    '''
    assert len(goals) > 0, 'Need at least one goal'
    assert len(actions) > 0, 'Need at least one action'

    # Find the most insistent goal - the 'Pythonic' way...
    best_goal, best_goal_value = max(list(goals.items()), key=lambda item: item[1])

    # ...or the non-Pythonic way. (This code is identical to the line above.)
    #best_goal = None
    #for key, value in goals.items():
    #    if best_goal is None or value > goals[best_goal]:
    #        best_goal = key

    if VERBOSE: print('BEST_GOAL:', best_goal, goals[best_goal])

    # Find the best (highest utility) action to take.
    # (Not the Pythonic way... but you can change it if you like / want to learn)
    best_action = None
    best_utility = None
    for key, value in actions.items(): 
        # Note, at this point: 
        #  - "key" is the action as a string, 
        #  - "value" is a dict of goal changes (see line 35)

        # Does this action change the "best goal" we need to change?
        if best_goal in value:

            # Do we currently have a "best action" to try? If not, use this one
            if best_action is None:
                ### 1. store the "key" as the current best_action
                best_action = key
                ### 2. use the "action_utility" function to find the best_utility value of this best_action
                best_utility = action_utility(best_action, best_goal)

            # Is this new action better than the current action?
            else: 
                ### 1. use the "action_utility" function to find the utility value of this action
                utility = action_utility(key, best_goal)
                ### 2. If it's the best action to take (utility > best_utility), keep it! (utility and action)    
                if utility > best_utility:
                    best_action = key
                    best_utility = action_utility(best_action, best_goal)
 
    # Return the "best action"
    return best_action

def choose_action_goap(max_depth):
    states = [[State(goals, actions), list(actions.keys())[0]]]

    best_action = None
    best_value = 1000000000
    best_plan = []
    VERBOSE = True
    # Tells if the planning has moved back 2 depth levels or more for the right iteration
    moved_back = False
    if VERBOSE: print('Searching...')
    
    changed = True
    # The action from the previous depth, used for when the planning has moved back 2 depth levels or more
    previous_depth_action = states[0][1]
    # The action from the current depth, used for when the planning has moved back 1 depth level
    current_depth_action = list(actions.keys())[0]
    while states:
        # Get the discontentment value the current state can get from the planned action
        current_value = states[-1][0].discontentment(states[-1][1])
        # Apply action
        states[-1][0].apply_action(states[-1][1])

        # if the plan queue has reached the maximum depth, compare to see if the current plan is the best, then pop back one depth level
        if len(states) >= max_depth:
            if current_value < best_value:
                # Set a new best plan and the best action is the first action of the plan queue
                best_action = states[1][1]
                best_value = current_value
                best_plan = [state[1] for state in states if states[1]] + [best_value]

            states.pop()
            continue

        if moved_back:
            # If the planning has popped back 2 depth levels or more, then take the next action of the previous_depth_action
            next_action = get_next_action(previous_depth_action)
        else:
            # If the planning only popped back 1 depth level, then take the next action of the action from the current depth
            next_action = get_next_action(current_depth_action)           
        if next_action:
            new_state = deepcopy(states[-1][0])
            states.append([new_state, None])
            states[-1][1] = next_action

            #new_state.apply_action_reset(next_action)
            if moved_back:
                moved_back = False
            else:
                current_depth_action = next_action

            changed = True
        else:
            # Reset the current depth's action
            current_depth_action = list(actions.keys())[0]
            try:
                # Get the action of the previous depth
                previous_depth_action = states[-1][1]
            except IndexError:
                pass
            # Set moved_back to True to tell that the planning has moved backward 2 levels or more
            moved_back = True
            states.pop()
    # Return the best action
    return best_action

class State(object):
    def __init__(self, goals, actions):
        self.goals = goals
        self.actions = actions
    
    def discontentment(self, action):
        return calculate_discontent(action)

    # Apply action to the state
    def apply_action(self, action):
        for goal, change in list(self.actions[action].items()):
            valid_goal = True
        try:
            self.goals[goal]
        except KeyError:
            valid_goal = False
        if valid_goal:
            self.goals[goal] = self.goals[goal] + change

        for goal in list(self.goals):
            if self.goals[goal] < 0:
                self.goals[goal] = 0

# Get the next action in the actions list, if the parameter given is the last action, return None
def get_next_action(action):
    next_index = list(actions.keys()).index(action) + 1
    try: 
        result = list(actions.keys())[next_index]
    except IndexError:
        return None
    return result
    
#==============================================================================

def print_actions():
    print('ACTIONS:')
    for name, effects in list(actions.items()):
        print(" * [%s]: %s" % (name, str(effects)))

def run_until_all_goals_zero():
    HR = '-'*40
    print_actions()
    print('>> Start <<')
    print(HR)
    running = True
    while running:
        print('GOALS:', goals)
        # What is the best action
        action = choose_action_goap(3)
        print('BEST ACTION:', action)
        # Apply the best action
        apply_action(action)
        print('NEW GOALS:', goals)
        # Stop?
        if all(value == 0 for goal, value in list(goals.items())):
            running = False

        print(HR)
        sleep(1.0)
    # finished
    print('>> Done! <<')

if __name__ == '__main__':
    run_until_all_goals_zero()
