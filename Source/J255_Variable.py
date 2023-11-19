class Variable:
    def __init__(self, value):
        self.value = value

    def Set(self, value):
        if self.value.__class__ != value.__class__:
            return
        
        self.value = value
    
    def Add(self, value):
        if self.value.__class__ != value.__class__:
            return
        
        self.value += value
    
    def Sub(self, value):
        if self.value.__class__ != value.__class__:
            return
        
        self.value -= value
    
    def Mul(self, value):
        if self.value.__class__ != value.__class__:
            return
        
        self.value *= value
    
    def Div(self, value):
        if self.value.__class__ != value.__class__:
            return
        
        self.value /= value

variables: dict[str, Variable] = {}

def DeclareVariable(name: str, variable: Variable):
    variables[name] = variable

def GetVariable(name: str) -> Variable:
    return variables[name] if name in variables else None

def GetVariableValue(name: str):
    return variables[name].value if name in variables else None

def SetVariableValue(name: str, value):
    if name in variables:
        variables[name].Set(value)

def DeclaredVariable(name: str) -> bool:
    return name in variables