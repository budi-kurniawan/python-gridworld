class QEntry():
    def __init__(self, value = 0.0):
        self.value = value
        self.counter = 0
    
    def update(self, value, counter):
        self.value = value
        self.counter = counter