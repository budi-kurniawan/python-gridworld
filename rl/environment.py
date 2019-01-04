from rl.util import Util
from rl.action import Action
from rl.result import Result

class Environment():
    wells = [3, 7, 13, 19, 29, 37, 43, 53, 61, 71, 79, 89]
    
    def __init__(self):
        self.gridworld = [[0 for x in range(Util.num_cols)] for y in range(Util.num_rows)]
        self.gridworld[Util.num_rows - 1][Util.num_cols - 1] = 1 # goal state
        num_states = Util.num_rows * Util.num_cols
        wells = Environment.wells
        for i in range(len(wells)):
            state = wells[i]
            if state + 1 > num_states:
                break
            row, col = Util.state_to_row_column(state, Util.num_cols)
            self.gridworld[row][col] = -1
        self.max_state = Util.num_rows * Util.num_cols - 1
    
    def submit(self, state, action):
        next_state = 0
        if action == Action.UP:
            next_state = state + Util.num_cols
            if next_state > self.max_state:
                next_state = state
        elif action == Action.DOWN:
            next_state = state - Util.num_cols
            if next_state < 0:
                next_state = state
        elif action == Action.LEFT:
            next_state = state if state % Util.num_cols == 0 else state - 1
        elif action == Action.RIGHT:
            next_state = state if (state + 1) % Util.num_cols == 0 else state + 1
        else:
            next_state = -1
            print("Invalid action")
        
        row = next_state // Util.num_cols
        col = next_state % Util.num_cols
        reward = self.gridworld[row][col];
        if reward == 0.0:
            reward = -0.1
        terminal = reward == 1 or reward == -1
        return Result(reward, next_state, terminal)