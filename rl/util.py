from threading import Lock
lock = Lock()

class Util:
    from rl.action import Action
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
        from rl.action import Action
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
        from rl.qentry import QEntry
        num_states = num_rows * num_cols
        q = [[QEntry(Util.MIN_VALUE) for _ in range(len(Util.actions))] for _ in range(num_states)]
        state_actions = Util.get_state_actions()
        # set q[state][disallowedAction] to -Double.MAX_VALUE and q[state][allowedAction] to 0
        for state in range(num_states):
            actions = state_actions[state]
            for a in actions:
                q[state][a].value = 0
        return q
    
    @staticmethod
    def policy_found(q, steps):
        from rl.environment import Environment
        from rl.agent import Agent
        from rl.stateaction import StateAction
        environment = Environment()
        agent = Agent(environment, Util.get_state_actions, q, 1, 1)
        maxStepsAllowed = Util.num_cols + Util.num_rows
        
        stepsToGoal = 0
        while stepsToGoal < maxStepsAllowed:
            stepsToGoal += 1
            prevState = agent.get_state()
            agent.test();
            action = agent.get_action()
            if prevState != Util.MIN_VALUE:
                steps.append(StateAction(prevState, action));
            
            if agent.get_state() == Util.get_goal_state():
                return True
            if agent.terminal:
                return False
        return agent.get_state() == Util.get_goal_state()