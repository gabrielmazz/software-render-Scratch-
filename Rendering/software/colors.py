
from random import randint

class Colors:
    
    def __init__(self):
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.CYAN = (0, 255, 255)
        self.MAGENTA = (255, 0, 255)
        self.SILVER = (192, 192, 192)
        self.GRAY = (102, 105, 115)
        self.MAROON = (128, 0, 0)
        self.OLIVE = (128, 128, 0)
        self.DARK_GREEN = (0, 128, 0)
        self.PURPLE = (128, 0, 128)
        self.TEAL = (0, 128, 128)
        self.NAVY = (0, 0, 128)
        self.ORANGE = (255, 165, 0)
        self.BROWN = (165, 42, 42)
        self.LIME = (0, 255, 0)
        self.PINK = (255, 192, 203)
        
    def random_color(self):
        return (randint(0, 255), randint(0, 255), randint(0, 255))