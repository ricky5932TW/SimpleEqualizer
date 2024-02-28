class TxtOp:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, 'r') as file:
            return file.read()

    def write(self, text):
        with open(self.path, 'w') as file:
            file.write(text)