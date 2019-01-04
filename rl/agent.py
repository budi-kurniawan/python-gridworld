from rl.environment import Environment
from rl.util import Util
import environment

class Agent():
    state = Util.MIN_VALUE
    terminal = False
    environment = None
    ALPHA = 0.7
    GAMMA = 0.9
    EPSILON = 0.3
    
    def __init__(self, Environment, state_actions, q, episode, num_episodes):
        self.environment = environment
        self.state_actions = state_actions
        self.q = q
        self.episode = episode
        self.num_episodes = num_episodes
    
        if num_episodes == 1:
            self.effectiveEpsilon = Agent.EPSILON
        else:
            self.effectiveEpsilon = (num_episodes - episode) * Agent.EPSILON / (num_episodes - 1);

    
    def get_state(self):
        return 1
    
    def tick(self):
        self.learn()
    
    def learn(self):
        if self.state == Util.MIN_VALUE:
            self.state = 0;
        else:
            prev_state = self.state;
            action = self.get_explore_exploit_action(prev_state)
            result = self.environment.submit(prev_state, action)
            self.state = result.nextState
            self.reward = result.reward
            self.terminal = result.terminal
            oldValue = self.get_q_value(prev_state, action)
            newValue = (1 - self.ALPHA) * oldValue + self.ALPHA * (self.reward + self.GAMMA * self.get_max_q(self.state))
            self.update_q_value(prev_state, action, newValue)
        
    def get_explore_exploit_action(self, prev_state):
        pass

    def get_q_value(self, prev_state, action):
        return 1
    
    def get_max_q(self, state):
        return 2
    
    def update_q_value(self, prev_state, action, new_value):
        pass