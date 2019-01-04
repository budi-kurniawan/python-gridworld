from time import time

def test_single_agent():
    from rl.engine import Engine
    engine = Engine()
    engine.run()


if __name__ == '__main__':
    from rl.util import Util
    start = time()
    Util.num_cols = 50
    Util.num_rows = 50
    Util.num_episodes = 15000
    for i in range(5):
        test_single_agent()

#     sa = Util.get_state_actions()
#     print(sa[1])
#     for i in range(len(Util.get_state_actions()[1])):
#         print(i)
#             for i in range(len(self.state_actions[state])):

    end = time()
    print('Execution time:', end - start, 'seconds')
    print('Average time:', (end - start)/5, 'seconds')
    
    