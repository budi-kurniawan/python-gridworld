from threading import Lock
from rl.action import Action
lock = Lock()

class Util:
    num_episodes = 10
    num_rows = 8
    num_cols = 8
    MAX_TICKS = 20000
    MIN_VALUE = -99999999
    actions = [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]
    state_actions = None
    
    @staticmethod
    def state_to_row_column(state, num_cols):
        return state // num_cols, state % num_cols

    @staticmethod
    def get_goal_state():
        return Util.num_rows * Util.num_cols - 1
    
    @staticmethod
    def get_effective_epsilon(episode, num_episodes, epsilon):
        if num_episodes == 1:
            return epsilon;
        else:
            return (num_episodes - episode) * epsilon / (num_episodes - 1)
        
    @staticmethod
    def get_state_actions():
        with lock:
            if Util.state_actions is not None:
                return Util.state_actions
            else:
                num_states = Util.num_rows * Util.num_cols
                topBoxActions = [Action.DOWN, Action.LEFT, Action.RIGHT]
                bottomBoxActions = [Action.UP, Action.LEFT, Action.RIGHT]
                leftBoxActions = [Action.UP, Action.DOWN, Action.RIGHT]
                rightBoxActions = [Action.UP, Action.DOWN, Action.LEFT]
                topLeftBoxActions = [Action.DOWN, Action.RIGHT]
                topRightBoxActions = [Action.DOWN, Action.LEFT]
                bottomLeftBoxActions = [Action.UP, Action.RIGHT]
                bottomRightBoxActions = [Action.UP, Action.LEFT]
        
                Util.state_actions = [] #[[0 for i in range(num_states)] for j in range(len(Util.actions))]
                sa = Util.state_actions
                
                for i in range(num_states):
                    if i == 0:
                        sa.append(bottomLeftBoxActions)
                    elif i == Util.num_cols - 1:
                        sa.append(bottomRightBoxActions) 
                    elif i == num_states - 1:
                        sa.append(topRightBoxActions)
                    elif i  == num_states - Util.num_cols:
                        sa.append(topLeftBoxActions)
                    elif i < Util.num_cols - 1:
                        sa.append(bottomBoxActions)
                    elif i > num_states - Util.num_cols:
                        sa.append(topBoxActions)
                    elif i % Util.num_cols == 0:
                        sa.append(leftBoxActions)
                    elif i % Util.num_cols == Util.num_cols - 1:
                        sa.append(rightBoxActions)
                    else:
                        sa.append(Util.actions)
                return Util.state_actions
    
    @staticmethod
    def create_initial_q(num_rows, num_cols):
        pass
'''    public static QEntry[][] createInitialQ(int numRows, int numCols) {
        int numStates = numRows * numCols;
        QEntry[][] q = new QEntry[numStates][actions.length];
        for (int i = 0; i < numStates; i++) {
            for (int j = 0; j < actions.length; j++) {
                q[i][j] = new QEntry();
            }
        }
        int[][] stateActions = getStateActions();
        // set q[state][disallowedAction] to -Double.MAX_VALUE and q[state][allowedAction] to 0
        for (int state = 0; state < numStates; state++) {
            for (int i = 0; i < actions.length; i++) {
                q[state][i].value = -Double.MAX_VALUE;
            }
            int[] actions = stateActions[state];
            for (int a : actions) {
                q[state][a].value = 0;
            }
        }
        return q;
    }
''' 