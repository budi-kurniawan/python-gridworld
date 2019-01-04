from rl.environment import Environment
from rl.util import Util
import random
from random import randint

class Agent():
    ALPHA = 0.7
    GAMMA = 0.9
    EPSILON = 0.3
    
    def __init__(self, environment, state_actions, q, episode, num_episodes):
        self.environment = environment
        self.state_actions = state_actions
        self.q = q
        self.episode = episode
        self.num_episodes = num_episodes
        self.state = Util.MIN_VALUE
        self.action = 0
        self.terminal = False
        
        if num_episodes == 1:
            self.effectiveEpsilon = Agent.EPSILON
        else:
            self.effectiveEpsilon = (num_episodes - episode) * Agent.EPSILON / (num_episodes - 1);

    
    def get_state(self):
        return self.state
    
    def get_action(self):
        return self.action
    
    def tick(self):
        self.learn()
    
    def learn(self):
        if self.state == Util.MIN_VALUE:
            self.state = 0;
        else:
            prev_state = self.state;
            action = self.get_explore_exploit_action(prev_state)
            self.action = action
            result = self.environment.submit(prev_state, action)
            self.state = result.next_state
            self.reward = result.reward
            self.terminal = result.terminal
            oldValue = self.get_q_value(prev_state, action)
            newValue = (1 - self.ALPHA) * oldValue + self.ALPHA * (self.reward + self.GAMMA * self.get_max_q(self.state))
            self.update_q_value(prev_state, action, newValue)

    def test(self):
        if self.state == Util.MIN_VALUE:
            self.state = 0;
        else:
            self.action = self.get_exploit_action(self.state)
            result = self.environment.submit(self.state, self.action);
            self.state = result.next_state;
            self.reward = result.reward;
            self.terminal = result.terminal;
        
    def get_explore_exploit_action(self, state):
        if random.random() < self.effectiveEpsilon:
            return self.get_random_action(state)
        else:
            return self.get_exploit_action(state)
    
    def get_random_action(self, state):
        # returns 0, 1, ... (n-1) randomly, where n is the number of elements in Action
        index = randint(0, len(self.state_actions[state]) - 1)
        return self.state_actions[state][index];
    
    def get_exploit_action(self, state):
        # exploit, return an action with the highest value
        # if there is more than one action with the same highest value, randomly select from those actions
        maxValue = Util.MIN_VALUE
        actionValues = []
        state_actions = Util.get_state_actions()
        for i in range(len(state_actions[state])):
            action = state_actions[state][i]
            value = self.get_q_value(state, action)
            actionValues.append(value)
            if value > maxValue:
                maxValue = value
            
        ''' find out how many actions have the same value '''
        topActionIndexes = []
        for i in range(len(state_actions[state])):
            if maxValue == actionValues[i]:
                topActionIndexes.append(i)
                
        randomIndex = randint(0, len(topActionIndexes) - 1)
        randomActionWithHighestValue = state_actions[state][topActionIndexes[randomIndex]]
        return randomActionWithHighestValue;

    def get_q_value(self, state, action):
        return self.q[state][action].value;
    
    def get_max_q(self, state):
        max_value = Util.MIN_VALUE;
        for i in range(len(self.state_actions[state])):
            action = self.state_actions[state][i]
            value = self.get_q_value(state, action)
            if value > max_value:
                max_value = value
        return max_value;
    
    def update_q_value(self, state, action, value):
        if self.q[state][action].value == Util.MIN_VALUE:
            raise Exception("Updating q, state" + str(state) + ", action:" + str(action) + ", value:" + str(value))
        self.q[state][action].value = value;