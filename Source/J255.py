import os
import sys
import time

from ast import literal_eval
from J255_Graphic import ExecuteG
from J255_Network import ExecuteNet
from J255_Variable import (Variable,
                           DeclareVariable,
                           GetVariable,
                           GetVariableValue,
                           SetVariableValue,
                           DeclaredVariable)

# Check arguments and main file
if len(sys.argv) == 1 or __name__ != "__main__":
    print("Usage : J255 [J255 File Path]")

    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

class Function:
    def __init__(self):
        self.code = []

    def Call(self):
        for i in range(0, len(self.code)):
            Execute(code[self.code[i]])

# Variables
targetFilePath = sys.argv[1]

functions: dict[str, Function] = {}
executable = True
thisFunctionName = ""
useList: dict[str, str] = {}

# Flags
# -1 : None
# 0 : if False
# 1 : for loop
# 2 : else
# 3 : declare function
# 4 : while loop
flag = -1

# 0 : Loop count / Condition
# 1 : Start code line
# 2 : End code line
forData = []
whileData = []

code = []

# Functions
def Execute(line: str):
    global executable
    global thisFunctionName
    global flag
    global forData
    global whileData
    global code
    
    args: list[str] = line.strip().split(" ", 1)
    
    code.append(line)

    # Declare a function
    if flag == 3:
        # End of declare function
        if "return" in line:
            flag = -1
            thisFunctionName = ""

            return
        
        lineIndex = len(code) - 1

        functions[thisFunctionName].code.append(lineIndex)

        return

    # Keywords
    if args[0] == "if":
        if args[1] == "True" or IsTrue(args[1]) or (DeclaredVariable(args[1]) and GetVariableValue(args[1])):
            return
        else:
            flag = 0
    elif args[0] == "else":
        if flag == 0:
            flag = 2
        else:
            flag = 0
    elif args[0] == "endif":
        flag = -1
    elif args[0] == "loop":
        flag = 1

        forData.clear()
        forData.append(GetVariableValue(args[1]) if DeclaredVariable(args[1]) else int(args[1]))
        forData.append(len(code))
    elif args[0] == "endloop":
        flag = -1
        
        lineIndex = len(code) - 1
        
        forData.append(lineIndex)

        for i in range(0, forData[0]):
            for j in range(forData[1], forData[2]):
                Execute(code[j])
    elif args[0] == "while":
        flag = 4

        whileData.clear()
        whileData.append(args[1])
        whileData.append(GetVariableValue(args[1]) if DeclaredVariable(args[1]) else bool(args[1]))
        whileData.append(len(code))   
    elif args[0] == "endwhile":
        flag = -1

        lineIndex = len(code) - 1

        whileData.append(lineIndex)

        while whileData[1]:
            for j in range(whileData[2], whileData[3]):
                Execute(code[j])

            whileData[1] = GetVariableValue(whileData[0]) if DeclaredVariable(whileData[0]) else bool(whileData[0])
    elif args[0] == "function":
        flag = 3
        functions[args[1]] = Function()
        thisFunctionName = args[1]
    elif args[0] == "call":
        if args[1] in functions:
            functions[args[1]].Call()
    elif args[0] == "use":
        datas = args[1].split(" as ", 1)

        if len(datas) == 1:
            useList[args[1]] = args[1]
        else:
            useList[datas[0]] = datas[1]
    elif args[0] == "include":
        Run(os.path.join(os.getcwd(), "TestCode", args[1]))

    # Use list
    elif "G" in useList and args[0] == useList["G"]:
        ExecuteG(args)
    elif "Net" in useList and args[0] == useList["Net"]:
        ExecuteNet(args)

    # Flags
    if flag == 0 or flag == 1 or flag == 4:
        return
    
    # Types
    elif args[0] == "int":
        DeclareVariable(args[1], Variable(0))
    elif args[0] == "float":
        DeclareVariable(args[1], Variable(0.0))
    elif args[0] == "string":
        DeclareVariable(args[1], Variable(""))
    elif args[0] == "bool":
        DeclareVariable(args[1], Variable(False))

    # Operators
    elif DeclaredVariable(args[0]):
        if args[1].startswith("= "):
            datas = args[1].split("=", 1)
            value = datas[1].replace(" ", "", 1)

            GetVariable(args[0]).Set(GetVariableValue(value) if DeclaredVariable(value) else literal_eval(value))
        elif args[1].startswith("+= "):
            datas = args[1].split("+=", 1)
            value = datas[1].replace(" ", "", 1)

            GetVariable(args[0]).Add(GetVariableValue(value) if DeclaredVariable(value) else literal_eval(value))
        elif args[1].startswith("-= "):
            datas = args[1].split("-=", 1)
            value = datas[1].replace(" ", "", 1)

            GetVariable(args[0]).Sub(GetVariableValue(value) if DeclaredVariable(value) else literal_eval(value))
        elif args[1].startswith("*= "):
            datas = args[1].split("*=", 1)
            value = datas[1].replace(" ", "", 1)

            GetVariable(args[0]).Mul(GetVariableValue(value) if DeclaredVariable(value) else literal_eval(value))
        elif args[1].startswith("/= "):
            datas = args[1].split("/=", 1)
            value = datas[1].replace(" ", "", 1)

            GetVariable(args[0]).Div(GetVariableValue(value) if DeclaredVariable(value) else literal_eval(value))

    # Functions
    elif args[0] == "print":
        sys.stdout.flush()
        
        if DeclaredVariable(args[1]):
            print(GetVariableValue(args[1]), end = "")
        else:
            print(args[1], end = "")
    elif args[0] == "println":
        if DeclaredVariable(args[1]):
            print(GetVariableValue(args[1]))
        else:
            args[1] = args[1].replace("\\n", "\n")
            
            print(args[1])
    elif args[0] == "input":
        if DeclaredVariable(args[1]):
            if type(GetVariableValue(args[1])) == int:
                SetVariableValue(args[1], int(input()))
            elif type(GetVariableValue(args[1])) == float:
                SetVariableValue(args[1], float(input()))
            elif type(GetVariableValue(args[1])) == str:
                SetVariableValue(args[1], str(input()))
            elif type(GetVariableValue(args[1])) == bool:
                SetVariableValue(args[1], bool(input()))
    elif args[0] == "sleep":
        if DeclaredVariable(args[1]):
            if type(GetVariableValue(args[1])) == int or type(GetVariableValue(args[1])) == float:
                time.sleep(GetVariableValue(args[1]))
        else:
            time.sleep(int(args[1]))
    elif args[0] == "readfile":
        datas = args[1].split(" ", 1)
        path: str = ""

        if DeclaredVariable(datas[0]) and type(GetVariableValue(datas[0]) == str):
            path = GetVariableValue(datas[0])
        else:
            path = datas[0]

        with open(path, "r", encoding = "utf-8") as file:
            if DeclaredVariable(datas[1]):
                SetVariableValue(datas[1], file.read())
    elif args[0] == "writefile":
        datas = args[1].split(" ", 1)
        path: str = ""

        if DeclaredVariable(datas[0]) and type(GetVariableValue(datas[0]) == str):
            path = GetVariableValue(datas[0])
        else:
            path = datas[0]

        with open(path, "w", encoding = "utf-8") as file:
            data: str = ""

            if DeclaredVariable(datas[1]):
                data = GetVariableValue(datas[1])
            else:
                data = datas[1]

            file.write(data)
    elif args[0] == "system":
        os.system(args[1])

def IsTrue(args: str):
    datas = args.split(" ", 5)
    
    # Default value!
    if datas[0] != "currentScore":
        return False
    
    value = GetVariableValue(datas[0])

    return value != None and value % int(datas[2]) == int(datas[4])

# Run
def Run(path):
    with open(path, "r", encoding = "utf-8") as file:
        while True:
            line = file.readline().strip()

            if line == '':
                continue
            elif line == "end":
                break

            # Multi line comments
            if ")--" in line:
                if len(line) == 1:
                    continue
                
                split = line.split(")--", 1)
                line = split[1]
            elif "--(" in line:
                continue

            # Returns immediately if no code or comments
            if line.startswith("--"):
                continue

            commands: list[str] = []

            for i in range(0, len(line) - 1):
                if line[i + 1] == ".":
                    if not line[i] == "^":
                        commands.append(line[0:i + 1].replace("^.", "."))

            if len(commands) == 0:
                break

            for command in commands:
                Execute(command)

Run(targetFilePath)