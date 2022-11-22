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
