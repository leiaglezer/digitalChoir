class DummyRightHand:
    def __init__(self):
        print("Dummy Right Hand Init")
        self.x = 0
        self.y = 0
        self.isConnected = False

    def run(self):
        print("Starting dummy glove")
        self.isConnected = True
    
    def getCoords(self):
        self.x = 0
        self.y = 0
        return (self.x, self.y)

    def getData(self, data_type):
        if data_type == "isConnected":
            return 1
        return 0

    def getGesture(self):
        return []

    def isConnected(self):
        return self.isConnected