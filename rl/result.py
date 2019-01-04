class Result():
    def __init__(self, reward, next_state, terminal):
        self.reward = reward
        self.next_state = next_state
        self.terminal = terminal