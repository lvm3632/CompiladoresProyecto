class Node:
    # childrens = None
    # type = None
    def __init__(self):
        self.childrens = []
        self.type = ''
        self.val = ''

    def print(self, lvl=0):
        r = (' ' * lvl) + self.type + ":" + str(self.val)
        print(r)
        #print(self.childrens)
        for c in self.childrens:
            c.print(lvl+1)
    
    def __repr__(self) -> str:
        return str(self.type) + " [Value]: " + str(self.val)

    def __str__(self) -> str:
        return str(self.type) + " [Value]: " + str(self.val)
