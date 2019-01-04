from rl.environment import Environment
from rl.agent import Agent
from rl.util import Util

class Engine():
    
    def __init__(self):
        self.state_actions = Util.get_state_actions()
        self.q = Util.create_initial_q(Util.num_rows,  Util.num_cols)

        
    def run(self):
        environment = Environment();
        num_episodes = Util.num_episodes
        for episode in range(1, num_episodes + 1, 1):
            agent = self.create_agent(environment, episode, num_episodes)
            count = 0
            while True:
                count += 1
                prev_state = agent.get_state()
                agent.tick()
                state = agent.get_state()
                #fireTickEvent(new TickEvent(agent, prevState, state));
                if agent.terminal or count == Util.MAX_TICKS:
                    break
            steps = []
            if Util.policy_found(self.q, steps):
                self.print_steps(episode, steps)
                break

    def print_steps(self, episode, steps):
        print('Policy found by single agent at episode ', episode)
        for step in steps:
            print('(' + str(step.state), str(step.action) + '), ', end="")
        print("(" + str(Util.get_goal_state()) + ")");
        
    def create_agent(self, environment, episode, num_episodes):
        return Agent(environment, Util.get_state_actions(), self.q, episode, num_episodes)