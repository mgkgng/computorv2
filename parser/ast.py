from enum import Enum, auto

class AST_TYPE(Enum):
    ASSIGN = auto()
    COMPUTE_VAL = auto()
    COMPUTE_SOL = auto()

class ASTWrapper:
    def __init__(self, root, type):
        self.root = root
        self.type = type

    def __str__(self):
        ret = 'AST Type: ' + 'Assignement' if self.type == AST_TYPE.ASSIGN \
            else 'Computation of value' if self.type == AST_TYPE.COMPUTE_VAL \
            else 'Computation of solution'
        ret += self.root.__str__()
        return ret