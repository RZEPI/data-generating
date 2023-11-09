from enum import Enum
from random import choice, randint

class Types(Enum):
    CONTENT = 0
    BUGFIX = 1
    PERFORMANCE = 2
    QUALITY_OF_LIFE = 3