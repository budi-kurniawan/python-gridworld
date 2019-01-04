class Result():
    reward = 0.0
    next_state = 0
    terminal = False

    def __init__(self, reward, next_state, terminal):
        self.reward = reward
        self.next_state = next_state
        self.terminal = terminal
