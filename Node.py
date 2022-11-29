class Node:
    # childrens = None
    # type = None
    def __init__(self):
        self.childrens = []
        self.type = ''
        self.val = ''

    def print(self, lvl=0):
        try:
            r = ('-' * lvl) + self.type + " : " + str(self.val)
            print(r)
            #print(self.childrens)
            #print(self.type)
            for c in self.childrens:
                c.print(lvl+1)
        except:
            print("Semantic invalid")

    def semanticPrint(self, lvl=0):
        r = (' ' * lvl) + self.type + ":" + str(self.val)
        #print(r)
        #print(self.childrens)
        stack = []
        #print(" ANOTHER INT ")
        #print(self.type, "Que es parent")
        if self.type == "INT_DCL":
            for leaf in self.childrens:
                print((' ' * lvl) + "parent: ", self.val, "hoja tipo:", leaf.type, "hoja valor: ", leaf.val, "Primer hijo: " ,leaf.childrens)
                if len(leaf.childrens) > 1:
                    print(leaf.childrens[1].childrens, "CUANTOS")
            #     for hijos in leaf.childrens:
            #         lvlInner = lvl
            #         print(hijos.val)
            #         hijos.semanticPrint(lvlInner+1)

            #     leaf.semanticPrint(lvl+1)
        for parent in self.childrens:
            parent.semanticPrint(lvl+1)
                #stack.append(parent)
            #print("parent", parent.type)
                #print(parent.val)    
    def __repr__(self) -> str:
        return str(self.type) + " [Value]: " + str(self.val)

    def __str__(self) -> str:
        return str(self.type) + " [Value]: " + str(self.val)
