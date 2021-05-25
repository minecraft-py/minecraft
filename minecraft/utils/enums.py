from enum import Enum, auto

class ToolLevel(Enum):
    WOOD = auto()
    STONE = auto()
    IRON = auto()
    DIAMOND = auto()

class ToolType(Enum):
    SWORD = auto()
    AXE = auto()
    PICKAXE = auto()
    SHOVEL = auto()
    HOE = auto()
