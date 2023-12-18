

class Memory:
    def __init__(self, name): # memory name
        self.scope_name = name
        self.memory = {}
        return

    def has_key(self, name):  # variable name
        return name in self.memory
    
    def get(self, name):         # gets from memory current value of variable <name>
        return self.memory[name]
    
    def put(self, name, value):  # puts into memory current value of variable <name>
        self.memory[name] = value

class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        if memory is None:
            self.memory = Memory("global")
        else:
            self.memory = Memory(memory)
        self.stack = [self.memory]

    def get(self, name):             # gets from memory stack current value of variable <name>
        # print("get",name)
        # for mem in self.stack:
        #     print(mem.scope_name, mem.memory)

        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i].has_key(name):
                return self.stack[i].get(name)
        return None
    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        # print("set",name)
        self.stack[-1].put(name, value) #???? 50/50 nie zdziala jak chce omodifikowac inny scope
        # for mem in self.stack:
        #     print(mem.scope_name, mem.memory)

    def push(self, memory: Memory): # pushes memory <memory> onto the stack
        self.stack.append(memory)


    def pop(self):          # pops the top memory from the stack
        for key in list(self.stack[-1].memory.keys()):
            for i in range(len(self.stack) - 2, -1, -1):
                if self.stack[i].has_key(key):
                    self.stack[i].put(key, self.stack[-1].get(key))
                    break
        self.stack.pop()

    def get_scope(self):
        return self.stack[-1].scope_name