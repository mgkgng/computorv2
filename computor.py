from utils import OP

class Computor:
    def __init__(self):
        self.vars = {}
        self.funcs = {}

    def read_input(self):
        s = input(">>> ")
        input_type = self.parse_input(s)
        if input_type == OP.ASSIGN:
            pass
        elif input_type == OP.COMPUTE:
            pass
        else:
            print("Error: invalid input")

    def get_op_type(self, rexps):
        if rexps[-1] == '?':
            if len(rexps[:-1]) == 0:
                res = OP.COMPUTE_VAL
            else:
                # TODO error check here
                res = OP.COMPUTE_SOL
        else:
            res = OP.ASSIGN
        return res

    def parse_input(self, s):
        exps = s.replace(' ', '').split('=')
        if len(exps) != 2:
            return OP.ERROR
        op_type = self.get_op_type(exps[1])
        if op_type == OP.COMPUTE_VAL or op_type == OP.COMPUTE_SOL:
            exps[1] = exps[1][:-1]
        
        if op_type == OP.ASSIGN:
            if not exps[0].isalpha():
                return OP.ERROR
            var_name = exps[0].lower()

    def assign(self, left, right):
        pass
    
    def compute(self, left, right):
        pass

            
        
        
