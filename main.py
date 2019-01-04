from rl.agent import Agent
from rl.engine import Engine
from time import time
from rl.util import Util

def test_single_agent():
    engine = Engine()
    engine.run()


if __name__ == '__main__':
    start = time()
    Util.num_cols = 4
    Util.num_rows = 4
    Util.num_episodes = 2
    #test_single_agent()
    
    
    #print(Util.get_state_actions())
    end = time()
    print('Execution time:', end - start, 'seconds')