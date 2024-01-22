from domain.base.singleton import Singleton

class Config(metaclass=Singleton):
    def __init__(self):
        self.precision = 2
        self.unit = 'THB'
