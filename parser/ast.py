from enum import Enum, auto

class AST_TYPE(Enum):
    ASSIGN = auto()
    COMPUTE_VAL = auto()
    COMPUTE_SOL = auto()

class ASTWrapper:
    def __init__(self, root, type):
        self.root = root
        self.type = type
  