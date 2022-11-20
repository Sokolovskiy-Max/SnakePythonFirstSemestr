import shelve


class Saves:
    def __init__(self):
        self.file = shelve.open('data')

    def save(self):
        self.file['Info'] = self.info
        self.file['Number'] = 42

    def get(self,name):
        try:
            return self.file[name]
        except KeyError:
            return 0

    def add(self, name, value):
        self.file[name] = value

    def __del__(self):
        self.file.close()
