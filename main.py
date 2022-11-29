import sys
sys.path.insert(0, "..")
reserved = {
    "int": "INTDCL",
    "float": "FLOATDCL",
    "print": "PRINT",
    "boolean": "BOOLDCL",
    "true": "BOOLVAL",
    "false": "BOOLVAL",
    "if": "IF",
    "else": "ELSE",
    "elif": "ELIF",
    "and": "AND",
    "or": "OR",
    "while":"WHILE",
    "for": "FOR"
}
# Terminales que identifica yacc.py (4.2 the tokens list)
tokens = [
    'NAME', 'INUMBER', 'FNUMBER', 'EQ', 'NE', 'GT', 'LT', 'GE', 'LE',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN'
] + list(reserved.values())
#tokens.extend(reserved.values())
literals = ['^', '=', ';', '{', '}']
######### Start of specification of tokens (4.3) #########
# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
# Comparisons
# Character literals are limited to a single character. +
# Thus, it is not legal to specify literals such as '<=' or '=='.
# For this, use the normal lexing rules
# (e.g., #define a rule such as t_EQ = r'==').
t_EQ = r'=='  # Equals
t_NE = r'!='  # Not Equals
t_LT = r'<' # LESS
t_GT = r'>' # Greater
t_LE = r'<=' #  Less equals
t_GE = r'>=' # Great equals
# Estados iniciales t_INITIAL or default t_PREFIX
def t_NAME(t):
    r'[a-zA-Z_]+[a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')    # Check for reserved words
    return t
    
def t_FNUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    #t.lexer.lineno += t.value.count("\n")
    t.lexer.lineno += len(t.value)
 # A string containing ignored characters (spaces and tabs)
t_ignore = " \t"
# Error handling rule:  the t.value attribute contains 
# the rest of the input string that has not been tokenized
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
# Note(s):
# t.value (txt matched), t.lineno, t.lexpos
# By default, t.type is set to the name
# following the t_ prefix.
# tok.type, tok.value, tok.lineno, and tok.lexpos
# You should avoid writing individual rules for reserved words. For example, if you write rules like this,
######### End of specification of tokens #########
#########
## Lexer tips:
## The token() method must return an object tok that has type and value attributes. If line number tracking is being used, then the token should also define a lineno attribute.
#########
# Build the lexer
import ply.lex as lex
#lexer = lex.lex(optimize=1, lextab="prueba")
lexer = lex.lex(debug=1)
# Parsing rules


from Node import Node
# dictionary of names
symbolsTable = {
    "table" : {},
    "parent" : None,
}
abstractTree = None

def p_prog(p):
    'prog : stmts'
    global abstractTree
    abstractTree = Node()
    abstractTree.type = 'root'
    abstractTree.childrens.extend(p[1])
    
def p_statements_recursion(p):
    '''stmts : statement stmts
             | statement '''
    stmt = p[1]
    if len(p) == 3:
        stmts = [ stmt ]
        stmts.extend(p[2])
        p[0] = stmts
    else: 
        p[0] = [ stmt ]

def p_statement_dcl_and_assign(p):
    '''statement : FLOATDCL NAME "=" expression ";"
                 | INTDCL NAME "=" expression ";"
                 | BOOLDCL NAME "=" boolexp ";" '''
    dcl_type = ''
    if p[1] == 'int':
        dcl_type = 'INT_DCL'
        symbolsTable["table"][p[2]] = {"type": "INT", "value": p[4].val}
    elif p[1] == 'float':
        dcl_type = 'FLOAT_DCL'
        symbolsTable["table"][p[2]] = {"type": "FLOAT", "value": p[4].val}
    elif p[1] == 'boolean':
        dcl_type = 'BOOL_DCL'
        symbolsTable["table"][p[2]] = {"type": "BOOLEAN", "value": p[4].val}
    n = Node()
    n.val = "="
    n.type = "ASSIGN"
    n1 = Node()
    n1.type = dcl_type
    n1.val = p[2]
    n.childrens.append(n1)
    n.childrens.append(p[4])

    # idName = Node()
    # idName.val = p[2]
    # idName.type = "ID"
    # assign.childrens.append(idName)
    #n.childrens.append(p[4])
    p[0] = n


def p_statement_declare_int(p):
    'statement : INTDCL NAME ";"'
    symbolsTable["table"][p[2]] = {"type": "INT", "value": 0}
    n = Node()
    n.type = "INT_DCL"
    n.val = p[2]
    p[0] = n

def p_statement_declare_float(p):
    'statement : FLOATDCL NAME ";"'
    symbolsTable["table"][p[2]] = {"type": "FLOAT", "value": 0}
    n = Node()
    n.type = "FLOAT_DCL"
    n.val = p[2]
    p[0] = n

def p_statement_declare_bool(p):
    'statement : BOOLDCL NAME ";"'
    symbolsTable["table"][p[2]] = {"type": "BOOLEAN", "value": False}
    n = Node()
    n.type = "BOOL_DCL"
    n.val = p[2]
    p[0] = n


def p_boolean_value(p):
  '''boolean_value : boolexp
                   | NAME '''
  n = Node()
  if isinstance(type(p[1]), str) and p[1].type == "BOOLVAL":
    n.type = 'BOOLEAN'
    n.val = p[1]
  else:
    n.type = 'BOOLVAL'
    n.val = str(p[1].val).lower()
  p[0] = n

def p_bool_expression(p):
    "boolexp : BOOLVAL"
    n = Node()
    n.type = 'BOOLVAL'
    n.val = (p[1] == 'true')
    p[0] = n
    
def p_boolean_expression(p):
  '''boolean_expression : LPAREN boolean_expression RPAREN
                        | boolean_expression AND boolean_expression
                        | boolean_expression OR boolean_expression
                        | boolean_value
                        | comparison'''
  if len(p) > 2:
    if p[2] in ['and', 'or']:
      n = Node()
      n.val = p[2]
      n.type = p[2].upper() 
      n.childrens.append(p[1])
      n.childrens.append(p[3])
      p[0] = n
    else:
      p[0] = p[2]
  else:
    p[0] = p[1]

def p_comparison(p):
  '''comparison : expression EQ expression
                | expression NE expression
                | expression GT expression
                | expression LT expression
                | expression GE expression
                | expression LE expression'''
  n = Node()
  n.val = p[2]
  n.type = p[2]
  n.childrens.append(p[1])
  n.childrens.append(p[3])
  p[0] = n

def p_statement_if(p):
    '''statement : IF LPAREN boolean_expression RPAREN "{" stmts "}" elif else '''
    n = Node()
    n.val = "if"
    n.type = "IF"
    n.childrens.append(p[3])
    n.childrens.extend(p[6])
    if p[8] != None:
        n.childrens.append(p[8])
    if p[9] != None:
        n.childrens.append(p[9])
    p[0] = n

def p_block_else(p):
    '''else : ELSE "{" stmts "}"
                | empty
        '''
    if len(p) > 2:
        n = Node()
        n.childrens.extend(p[3])
        n.type = "ELSE"
        p[0] = n 

def p_elif(p):
    '''elif : ELIF LPAREN boolean_expression RPAREN "{" stmts "}"
            | empty'''
    if len(p) > 2:
        n = Node()
        n.val = "elif"
        n.type ="ELIF"
        n.childrens.append(p[3])
        n.childrens.extend(p[6])
        p[0] = n

def p_statement_while(p):
    '''statement : WHILE LPAREN boolean_expression RPAREN "{" stmts "}"'''
    n = Node()
    n.type = 'WHILE'
    n2 = Node()
    n2.childrens = p[6]
    n.childrens.append(p[3])
    n.childrens.append(n2)
    p[0] = n

def p_statement_assign(p):
    '''statement : NAME "=" expression ";"'''
    if p[1] not in symbolsTable["table"]:
        print ( "You must declare a variable before using it")
    n = Node()
    n.type = 'ASSIGN'
    n.val = "="
    ##n.childrens.append(p[1])
    n1 = Node()
    n1.type = 'ID'
    n1.val = p[1]
    n.childrens.append(n1)
    n.childrens.append(p[3])
    p[0] = n

def p_statement_print(p):
    'statement : PRINT expression ";"'
    n = Node()
    n.type = 'PRINT'
    n.childrens.append(p[2])
    p[0] = n

def p_expression_name(p):
    "expression : NAME"
    if p[1] in symbolsTable["table"]:
        n = Node()
        n.type = 'ID'
        n.val = p[1]
        p[0] = n

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression '^' expression
                  | LPAREN expression RPAREN
                   '''
    if p[2] in ['+', '-', '*', '/', '^']:
        n = Node()
        n.type = p[2]
        n.childrens.append(p[1])
        n.childrens.append(p[3])
        p[0] = n
    else:
        p[0] = p[2]

def p_expression_inumber(p):
    "expression : INUMBER"
    n = Node()
    n.type = 'INUMBER'
    n.val = int(p[1])
    p[0] = n
    
def p_expression_fnumber(p):
    "expression : FNUMBER"
    n = Node()
    n.type = 'FNUMBER'
    n.val = float(p[1])
    p[0] = n

def p_expression_boolval(p):
     "expression : boolexp"
     p[0] = p[1]

def p_for_statement(p):
    '''statement : FOR LPAREN statement boolean_expression ";" step RPAREN "{" stmts "}" '''
    n = Node()
    n.type = "FOR"
    n.childrens.append(p[3])
    n.childrens.append(p[4])
    n.childrens.append(p[6])
    n.childrens.extend(p[9])
    p[0] = n
    
def p_step(p):
    '''step : NAME PLUS "=" INUMBER
            | NAME MINUS "=" INUMBER
            | NAME TIMES "=" INUMBER
            | NAME DIVIDE "=" INUMBER
            | NAME PLUS PLUS
            | NAME MINUS MINUS '''
    if len(p) == 4: 
        n = Node()  
        if p[2] in ['+', '-']:
            n.type = "ASSIGN"
            if p[1] in symbolsTable["table"]:
                n1 = Node()
                n1.type = 'ID'
                n1.val = p[1]
                n.childrens.append(n1)
                n.val = "="
            else:
                print("Error undeclared variable")
                n.val = "UNDECLARED-VARIABLE"
            postfix = Node()
            postfix.type = p[2]
            n2 = Node()
            n2.val = p[1]
            n2.type = "ID"
            n3 = Node()
            n3.val = 1
            n3.type = "INUMBER"
            postfix.childrens.append(n2)
            postfix.childrens.append(n3)
            #postfix.val = 1
            n.childrens.append(postfix)
            p[0] = n
    elif len(p) == 5:
        n = Node()
        if p[2] in ['+', '-', '*', '/']:
            n.type = "ASSIGN"
            if p[1] in symbolsTable["table"]:
                n1 = Node()
                n1.type = 'ID'
                n1.val = p[1]
                n.childrens.append(n1)
                op = Node()
                op.type = p[2]
                nbr = Node()
                nbr.type = "INUMBER"
                nbr.val = p[4]
                op.childrens.append(n1)
                op.childrens.append(nbr)

                n.childrens.append(op)
                p[0] = n
            else:
                print("Error undeclared variable")
                n.val = "UNDECLARED-VARIABLE"

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print(p)
    if p:
        print("Syntax error at '%s'" % p.value)
        # Just discard the token and tell the parser it's okay.
        parser.errok()
        # or parser.token() # or parser.restart()
    else:
        print("Syntax error at EOF")
## Precedence:
## TIMES/DIVIDE have higher precedence than PLUS/MINUS 
# (since they appear later in the precedence specification).
import ply.yacc as yacc
parser = yacc.yacc(start="prog")
precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'EQ', 'NE'),
    ('nonassoc', 'LT', 'GT', 'GE', 'LE'),  # Evitar a > b > c > pero sí a a > b
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', '^'),
    ('right', 'UMINUS'), # Unary minus operator eg: + -5
)

def getTacFile():
    file = open("output-tac.txt", "w")
    sys.stdout = file
    genTAC(abstractTree)
    f.close()

def getSyntFile():
    file = open("output-syntax.txt", "w")
    sys.stdout = file
    abstractTree.print()
    f.close()

f = open("code.txt")
content = f.read()
print("YACC PARSE: ", yacc.parse(content))

print("======= Start of Syntax Analysis (Tree) =======")
abstractTree.print()
print("======= End of Syntax Analysis (Tree)  =======")
# print("\n======= Start of Semantic Analysis (Tree) =======")
# #abstractTree.semanticPrint()
# print("======= End of Semantic Analysis (Tree)  =======\n")
declTags = ['INUMBER', 'FNUMBER', 'BOOLVAL', 'ID']
opSymbols = ['+', '-', '*', '/', '^']
compSymbols = ['!=', '==', 'AND', 'OR', '>', '<', '>=', '<=']
varCounter = 0
labelCounter = 0

def genTAC(node):
    try:
        global varCounter
        global labelCounter
        ##print(node.type, "NODE")
        if (node.type == "ASSIGN"):
            print(node.childrens[0].val, ":=", genTAC(node.childrens[1]))
        elif (node.type in declTags):
            return str(node.val)
        elif (node.type in compSymbols):
            tempVar = "t" + str(varCounter)
            varCounter = varCounter + 1
            print(tempVar, ":=",
                genTAC(node.childrens[0]), node.type, genTAC(node.childrens[1]))
            return tempVar
        elif (node.type in opSymbols):
            tempVar = "t" + str(varCounter)
            varCounter = varCounter + 1
            print(tempVar, " := ",
                genTAC(node.childrens[0]), node.type, genTAC(node.childrens[1]))
            return tempVar
        elif (node.type == "PRINT"):
            print("PRINT ", genTAC(node.childrens[0]))
        elif (node.type == "IF"):
            tempVar = "t" + str(varCounter)
            varCounter = varCounter + 1
            print(tempVar, ":=!", genTAC(node.childrens[0]))
            tempLabel = "l" + str(labelCounter)
            labelCounter = labelCounter + 1
            print("gotoLabelIf", tempVar, tempLabel)
            genTAC(node.childrens[1])
            print(tempLabel)
            for child in node.childrens[2:len(node.childrens)]:
                genTAC(child)
        elif (node.type == "ELIF"):
            tempVar = "t" + str(varCounter)
            varCounter = varCounter + 1
            print(tempVar, " :=!", genTAC(node.childrens[0]))
            tempLabel = "l" + str(labelCounter)
            labelCounter = labelCounter + 1
            print("gotoLabelIf ", tempVar, tempLabel)
            genTAC(node.childrens[1])
            print(tempLabel)
            for child in node.childrens[2:len(node.childrens)]:
                genTAC(child)
        elif (node.type == "ELSE"):
            genTAC(node.childrens[0])
        elif (node.type == "WHILE"):
            tmplbl1 = "l" + str(labelCounter)
            labelCounter = labelCounter + 1
            print(tmplbl1)
            tempVar = "t" + str(varCounter)
            varCounter = varCounter + 1
            print(tempVar + " :=!", genTAC(node.childrens[0]))
            tmplbl2 = "l" + str(labelCounter)
            labelCounter = labelCounter + 1
            print("gotoLabelIf", tempVar, tmplbl2)
            genTAC(node.childrens[1])
            print("gotoLabelIf", tempVar, tmplbl1)
            print(tmplbl2)
        elif (node.type == "FOR"):
            genTAC(node.childrens[0])
            tmplbl1 = "l" + str(labelCounter)
            labelCounter = labelCounter + 1
            print(tmplbl1)
            tempVar = "t" + str(varCounter)
            varCounter = varCounter + 1
            print(tempVar, " := !", genTAC(node.childrens[1]))
            tmplbl2 = "l" + str(labelCounter)
            labelCounter = labelCounter + 1
            print("gotoLabelIf ", tempVar, tmplbl2)
            genTAC(node.childrens[3])
            genTAC(node.childrens[2])
            print("gotoLabelIf ", tempVar, tmplbl1)
            print(tmplbl2)
        else:
            for child in node.childrens:
                genTAC(child)
    except:
        print("Input inválido")


print("\n======= Start of TAC =======")
genTAC(abstractTree)
print("======= End of TAC =======")

# Output TAC to file
getSyntFile()
getTacFile()
#Some examples
# for ( i = 0; i < 3; i++){
#     stamentes
# }
# i := 0
# t1 = i < 3
# t0 = !t1
# gotoLabelif t0 Label1
# staments
# i = i + 1
# Label1
# while ( condicion ) {
#     staments
# }
# WHILE
# t1 = condicion
# t0 = !t1
# gotoLabelif t0 Label1
# staments
# Label1
