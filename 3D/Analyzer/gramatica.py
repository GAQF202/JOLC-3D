reservadas = {
    'function'  : 'FUNCTION',
    'print'     : 'PRINT',
    'println'   : 'PRINTLN',
    'Int64'     : 'INT64',
    'Float64'   : 'FLOAT64',
    'Char'      : 'CHAR',
    'String'    : 'STRING',
    'Bool'      : 'BOOL',
    'nothing'   : 'NULO',
    'true'      : 'TRUE',
    'false'     : 'FALSE',
    'uppercase' : 'UPPERCASE',
    'lowercase' : 'LOWERCASE',
    'log10'     : 'LOGARITMOB10',
    'log'       : 'LOGARITMONOB10',
    'sin'       : 'SIN',
    'cos'       : 'COS',
    'tan'       : 'TAN',
    'sqrt'      : 'SQRT',
    'end'       : 'END',
    'return'    : 'RETURN',
    'while'     : 'MIENTRAS',
    'for'       : 'FOR',
    'in'        : 'IN',
    'if'        : 'IF',
    'elseif'    : 'ELSEIF',
    'else'      : 'ELSE',
    'parse'     : 'PARSE',
    'trunc'     : 'TRUNC',
    'float'     : 'FLOAT',
    'string'    : 'STRINGNATIVE',
    'typeof'    : 'TYPEOF',
    'push'      : 'PUSH',
    'pop'       : 'POP',
    'length'    : 'LENGTH',
    'break'     : 'BREAK',
    'continue'  : 'CONTINUE',
    'mutable'   : 'MUTABLE',
    'struct'    : 'STRUCT',
    'global'    : 'GLOBAL',
    'local'     : 'LOCAL'
}

tokens = [
    'MAS',
    'MENOS',
    'PARENTESISA',
    'PARENTESISC',
    'POR',
    'DIVIDIDO',
    'POTENCIA',
    'COMA',
    'PCOMA',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CARACTER',
    'PORCENTAJE',
    'MAYOR',
    'MENOR',
    'MAYORIGUAL',
    'MENORIGUAL',
    'DOBLEIGUAL',
    'NOIGUAL',
    'OR',
    'AND',
    'NOT',
    'DOSP',
    'IGUAL',
    'ID',
    'CORCHETEA',
    'CORCHETEC',
    'COMILLASDOBLES',
    'PUNTO'
] + list(reservadas.values())

#Tokens
t_IGUAL = r'='
t_CORCHETEA = r'\['
t_CORCHETEC = r'\]'
t_MAS = r'\+'
t_MENOS = r'-'
t_OR = r'\|\|'
t_AND = r'\&\&'
t_NOT = r'!'
t_MAYOR = r'>'
t_MENOR= r'<'
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_DOBLEIGUAL = r'=='
t_NOIGUAL = r'!='
t_PARENTESISA = r'\('
t_PARENTESISC = r'\)'
t_COMA = r','
t_PCOMA = r'\;'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_POTENCIA = r'\^'
t_PORCENTAJE = r'%'
t_DOSP = r':'
t_COMILLASDOBLES = r'\"'
t_PUNTO = r'\.'

#IDENTIFICADOR
def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value,'ID')    # Check for reserved words
     return t

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 


def t_CARACTER(t):
    r'\'.?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Floaat value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Int value too large %d", t.value)
        t.value = 0
    return t

# COMENTARIO MULTILINEA
def t_COMENTARIO_MULTILINEA(t):
    r'\#\=(.|\n)*?\=\#'
    t.lexer.lineno += t.value.count('\n')

# COMENTARIO SIMPLE
def t_COMENTARIO_SIMPLE(t):
    r'\#.*' #PUEDE SER -> r'//.*\n?'
    t.lexer.lineno += 1

t_ignore = " \t"

def t_nuevalinea(t):
    r'\n'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


'''from Enum_types.Operations import Operations
from Expression.Primitive import Primitive
from Instructions.Print import Print
from Instructions.Declaration import Declaration
from Instructions.Empty import Empty
from Instructions.Break import Break
from Instructions.Struct import Struct
from Instructions.Continue import Continue
from Instructions.AlterStruct import AlterStruct
from Expression.Arithmetic import Arithmetic
from Expression.Relationals import Relationals
from Expression.Logics import Logics
from Expression.VariableCall import VariableCall
from Expression.AttributeStruct import AttributeStruct
from Expression.NativeDoublePar import NativeDoublePar
from Expression.AccessStruct import AccessStruct
from Reports.Node import Node'''
from Environment.Environment import Environment
from Enum_types.typeExpression import typeExpression
from Expression.Primitive.NumberVal import NumberVal
from Expression.Primitive.VariableCall import VariableCall
from Expression.Primitive.StringVal import StringVal
from Expression.Primitive.Range import Range
from Expression.Primitive.TrueVal import TrueVal
from Expression.Primitive.FalseVal import FalseVal
from Expression.Arithmetic.Plus import Plus
from Expression.Arithmetic.Minus import Minus
from Expression.Arithmetic.Times import Times
from Expression.Arithmetic.Divided import Divided
from Expression.Arithmetic.Module import Module
from Expression.Arithmetic.Pow import Pow
from Expression.Arithmetic.Negative import Negative
from Expression.Relational.Equal import Equal
from Expression.Relational.NotEqual import NotEqual
from Expression.Relational.Greater import Greater
from Expression.Relational.GreaterOrEqual import GreaterOrEqual
from Expression.Relational.Less import Less
from Expression.Relational.LessOrEqual import LessOrEqual
from Expression.Logic.Or import Or
from Expression.Logic.And import And
from Expression.Logic.Not import Not
from Expression.Natives.UpperCase import UpperCase
from Expression.Natives.LowerCase import LowerCase
from Expression.Array.Array import Array
from Expression.Array.ArrayCall import ArrayCall
from Expression.Natives.Length import Length
from Instruction.Declaration import Declaration
from Instruction.Function import Function
from Instruction.Parameter import Parameter
from Instruction.FunctionCall import FunctionCall
from Instruction.IfCondition import IfCondition
from Instruction.ElseIfCondition import ElseIfCondition
from Instruction.BlockLoop import BlockLoop
from Instruction.WhileLoop import WhileLoop
from Instruction.ForLoop import ForLoop
from Instruction.Return import Return
from Instruction.AssignmentArray import AssignmentArray
from Generator.Generator import Generator
from Instruction.Print import Print
import ply.lex as lex
lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    #('left','IGUAL'),
    #('left','MAYOR','MENOR'),
    ('left','UNOT'),
    ('left','AND','OR'),
    ('left','MENOR','MENORIGUAL','MAYOR','MAYORIGUAL','DOBLEIGUAL','NOIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO','PORCENTAJE'),
    ('left','POTENCIA'),
    ('left','UMENOS')
    )

def p_instruccion(t):
    'start : body'

    generator : Generator = Generator()
    globalEnv = Environment(None)
    for ins in t[1]:
        ins.generator = generator
        ins.compile(globalEnv)

    t[0] = generator.getCode()

def p_body(t):
    '''
    body : body Print
         | body Println
         | body Asignacion
         | body create_function
         | body functionCall
         | body whileLoop
         | body forLoop
         | body IfCondition
         | body parseNative
         | body truncNative
         | body floatNative
         | body stringNative
         | body typeOfNative
         | body pushArray
         | body popArray
         | body lengthArray
         | body assignmentArray
         | body Struct
         | body structAccess
         | Print
         | Println
         | create_function
         | Asignacion
         | functionCall
         | whileLoop
         | forLoop
         | IfCondition
         | parseNative
         | truncNative
         | floatNative
         | stringNative
         | typeOfNative
         | pushArray
         | popArray
         | lengthArray
         | assignmentArray
         | Struct
         | structAccess
         | empty
    '''
    if(len(t) == 3):
        t[1].append(t[2])
        t[0] = t[1]
    elif(len(t)== 2):
        t[0] = [t[1]]

def p_Struct(t):
    '''
    Struct : MUTABLE STRUCT ID bodyStruct END PCOMA
           | STRUCT ID bodyStruct END PCOMA
    '''
    #if len(t) == 7:
    #    t[0] = Struct(t[3],t[4],True, t.lineno(1), find_column(t.slice[1]))
    #elif len(t) == 6:
     #   t[0] = Struct(t[2],t[3],False, t.lineno(1), find_column(t.slice[1]))

def p_bodyStruct(t):
    '''
    bodyStruct : bodyStruct ID DOSP DOSP type PCOMA 
               | bodyStruct ID PCOMA  
               | ID DOSP DOSP type PCOMA
               | ID PCOMA
    '''
   # if len(t) == 7:
     #   t[1].append(AttributeStruct(t[2],t[5], t.lineno(1), find_column(t.slice[2])))
    #    t[0] = t[1]
   # elif len(t) == 4:
    #    t[1].append(AttributeStruct(t[2],typeExpression.NULO, t.lineno(1), find_column(t.slice[2])))
    #    t[0] = t[1]
    #elif len(t) == 6:
    #    t[0] = [AttributeStruct(t[1],t[4], t.lineno(1), find_column(t.slice[1]))]
    #elif len(t) == 3:
    #    t[0] = [AttributeStruct(t[1],typeExpression.NULO, t.lineno(1), find_column(t.slice[1]))]

def p_body_typeStruct(t):
    '''
    bodyStruct : bodyStruct ID DOSP DOSP ID PCOMA
               | ID DOSP DOSP ID PCOMA
    '''
    #if len(t) == 7:
    #    t[1].append(AttributeStruct(t[2],t[5], t.lineno(1), find_column(t.slice[2])))
    #    t[0] = t[1]
    #elif len(t) == 6:
     #   t[0] = [AttributeStruct(t[1],t[4], t.lineno(1), find_column(t.slice[1]))]


def p_structAccess(t):
    'structAccess : ID attributes IGUAL exp PCOMA'
    #t[0] = AlterStruct(t[1],t[2],t[4], t.lineno(1), find_column(t.slice[1]))

def p_pushArray(t):
    '''
    pushArray : PUSH NOT PARENTESISA exp COMA parametersCall PARENTESISC PCOMA  
    '''
    #t[0] = ArraysFunctions(t[4], t[6], Operations.PUSH, False, t.lineno(1), find_column(t.slice[1]))


def p_pushArray_id(t):
    '''
    pushArray : PUSH NOT PARENTESISA ID COMA parametersCall PARENTESISC PCOMA  
    '''
    #t[0] = ArraysFunctions(t[4], t[6], Operations.PUSH, True, t.lineno(1), find_column(t.slice[1]))

def p_popArray(t):
    '''
    popArray : POP NOT PARENTESISA exp PARENTESISC PCOMA  
    '''
    #t[0] = ArraysFunctions(t[4], None, Operations.POP, False, t.lineno(1), find_column(t.slice[1]))


def p_popArray_id(t):
    '''
    popArray : POP NOT PARENTESISA ID PARENTESISC PCOMA  
    '''
    #t[0] = ArraysFunctions(t[4], None, Operations.POP, True, t.lineno(1), find_column(t.slice[1]))

def p_lengthArray(t):
    '''
    lengthArray : LENGTH PARENTESISA exp PARENTESISC PCOMA  
    '''
    #t[0] = ArraysFunctions(t[3], None, Operations.LENGTH, False, t.lineno(1), find_column(t.slice[1]))


def p_lengthArray_id(t):
    '''
    lengthArray : LENGTH PARENTESISA ID PARENTESISC PCOMA  
    '''
   # t[0] = ArraysFunctions(t[3], None, Operations.LENGTH, True, t.lineno(1), find_column(t.slice[1]))

def p_parseNative(t):
    '''
    parseNative : PARSE PARENTESISA type COMA exp PARENTESISC PCOMA
    '''
    #t[0] = NativeDoublePar(Operations.PARSE, t[3], t[5], t.lineno(1), find_column(t.slice[1]))

def p_truncNative(t):
    '''
    truncNative : TRUNC PARENTESISA type COMA exp PARENTESISC PCOMA
                | TRUNC PARENTESISA exp PARENTESISC PCOMA
    '''
    #if (len(t) == 8):
    #    t[0] = NativeDoublePar(Operations.TRUNC, t[3], t[5], t.lineno(1), find_column(t.slice[1]))
    #elif (len(t) == 6):
    #    t[0] = NativeOnePar(Operations.TRUNC, t[3], t.lineno(1), find_column(t.slice[1]))

def p_floatNative(t):
    '''
    floatNative : FLOAT PARENTESISA exp PARENTESISC PCOMA
    '''
    #t[0] = NativeOnePar(Operations.CONVERTTOFLOAT, t[3], t.lineno(1), find_column(t.slice[1]))

def p_stringNative(t):
    '''
    stringNative : STRINGNATIVE PARENTESISA exp PARENTESISC PCOMA
    '''
    #t[0] = NativeOnePar(Operations.STRINGNATIVE, t[3], t.lineno(1), find_column(t.slice[1]))

def p_typeOfNative(t):
    '''
    typeOfNative : TYPEOF PARENTESISA exp PARENTESISC PCOMA
    '''
    #t[0] = NativeOnePar(Operations.TYPEOF, t[3], t.lineno(1), find_column(t.slice[1]))

def p_IfCondition(t):
    '''
    IfCondition : IF exp block_loops elseIfSt elseSt END PCOMA
    '''
    t[0] = IfCondition(t[2],BlockLoop(t[3]),t[4],t[5], t.lineno(1), find_column(t.slice[1]))

def p_elseIfSt(t):
    '''
    elseIfSt : elseIfSt ELSEIF exp block_loops
             | ELSEIF exp block_loops
             | empty
    '''
    if len(t) == 5 : 
        t[1].append(ElseIfCondition(t[3],BlockLoop(t[4])))
        t[0] = t[1]
    elif len(t) == 4:
        t[0] = [ ElseIfCondition(t[2],BlockLoop(t[3])) ]
    elif len(t) == 2:
        t[0] = None

def p_elseSt(t):
    '''
    elseSt : ELSE block_loops
           | empty
    '''
    if len(t) == 3: t[0] = BlockLoop(t[2])
    elif len(t) == 2: t[0] = t[1]

def p_empty(t):
    'empty :'
    #t[0] = Empty()

def p_while(t):
    '''
    whileLoop : MIENTRAS exp block_loops END PCOMA
    '''
    t[0] = WhileLoop(t[2], BlockLoop(t[3]))

def p_for(t):
    '''
    forLoop : FOR ID IN exp block_loops END PCOMA
    '''
    t[0] = ForLoop(t[2], t[4], BlockLoop(t[5]), t.lineno(1), find_column(t.slice[1]))

def p_functionCall(t):
    '''
    functionCall : ID PARENTESISA parametersCall PARENTESISC PCOMA
                 | ID PARENTESISA PARENTESISC PCOMA
    '''
    if len(t) == 6 : t[0] = FunctionCall(t[1], t[3], False)
    elif len(t) == 5 : t[0] = FunctionCall(t[1], [], False)

def p_parametersCall(t):
    '''
    parametersCall : parametersCall COMA exp
                   | exp
    '''
    if len(t) == 4 :
        t[1].append(t[3])
        t[0] = t[1]
    elif len(t) == 2:
        t[0] = [t[1]]

def p_create_function(t):
    '''
    create_function : FUNCTION ID PARENTESISA parameters PARENTESISC block_function END PCOMA
                    | FUNCTION ID PARENTESISA PARENTESISC block_function END PCOMA
    '''
    if len(t) == 9 : t[0] = Function(t[2], t[4], typeExpression.NULO, t[6])
    elif len(t) == 8 : t[0] = Function(t[2], [], typeExpression.NULO, t[5])

def p_parameters(t):
    '''
    parameters : parameters COMA ID 
               | parameters COMA ID DOSP DOSP  type  
               | parameters COMA ID DOSP DOSP  ID
               | ID 
               | ID DOSP DOSP type
               | ID DOSP DOSP ID
    '''
    
    if len(t) == 7 : 
        t[1].append( Parameter((t[3]), t[6], t.lineno(1), find_column(t.slice[3])))
        t[0] = t[1]
    #elif len(t) == 4 : 
    #    t[1].append( Parameter((t[3]), typeExpression.NULO, t.lineno(1), find_column(t.slice[3])) )
    #    t[0] = t[1]
    elif len(t) == 5:
        t[0] = [Parameter((t[1]), t[4], t.lineno(1), find_column(t.slice[1]))]
    #elif len(t) == 2:
    #    t[0] = [Parameter((t[1]), typeExpression.NULO, t.lineno(1), find_column(t.slice[1]))]


def p_block_function(t):
    '''
    block_function : block_function Print
                   | block_function Println
                   | block_function Asignacion
                   | block_function retorno
                   | block_function functionCall
                   | block_function whileLoop
                   | block_function forLoop
                   | block_function IfCondition
                   | block_function parseNative
                   | block_function truncNative
                   | block_function floatNative
                   | block_function stringNative
                   | block_function typeOfNative
                   | block_function pushArray
                   | block_function popArray
                   | block_function lengthArray
                   | block_function assignmentArray
                   | block_function Struct
                   | block_function structAccess
                   | Print
                   | Println
                   | Asignacion
                   | retorno
                   | functionCall
                   | whileLoop
                   | forLoop
                   | IfCondition
                   | parseNative
                   | truncNative
                   | floatNative
                   | stringNative
                   | typeOfNative
                   | pushArray
                   | popArray
                   | lengthArray
                   | assignmentArray
                   | Struct
                   | structAccess
                   | empty
    '''
    if(len(t) == 3):
        t[1].append(t[2])
        t[0] = t[1]
    elif(len(t)== 2):
        t[0] = [t[1]]

def p_Break(t):
    'Break : BREAK PCOMA'
    #t[0] = Break()

def p_Continue(t):
    'Continue : CONTINUE PCOMA'
    #t[0] = Continue()

def p_block_loops(t):
    '''
    block_loops : block_loops Print
                | block_loops Println
                | block_loops Asignacion
                | block_loops retorno
                | block_loops functionCall
                | block_loops forLoop
                | block_loops whileLoop
                | block_loops IfCondition
                | block_loops parseNative
                | block_loops truncNative
                | block_loops floatNative
                | block_loops stringNative
                | block_loops typeOfNative
                | block_loops pushArray
                | block_loops popArray
                | block_loops lengthArray
                | block_loops assignmentArray
                | block_loops Break
                | block_loops Continue
                | block_loops Struct
                | block_loops structAccess
                | Print
                | Println
                | Asignacion
                | retorno
                | functionCall
                | whileLoop
                | forLoop
                | IfCondition
                | parseNative
                | truncNative
                | floatNative
                | stringNative
                | typeOfNative
                | pushArray
                | popArray
                | lengthArray
                | assignmentArray
                | Break
                | Continue
                | Struct
                | structAccess
                | empty
    '''
    if(len(t) == 3):
        t[1].append(t[2])
        t[0] = t[1]
    elif(len(t)== 2):
        t[0] = [t[1]]

def p_retorno(t):
    '''
    retorno : RETURN exp PCOMA
    '''
    t[0] = Return(t[2])

def p_Print(t):
    '''Print : PRINT PARENTESISA exp PARENTESISC PCOMA'''
    t[0] = Print(t[3],False,False, t.lineno(1), find_column(t.slice[1]))

def p_otherFormPrint(t):
    '''Print : PRINT PARENTESISA parametersCall PARENTESISC PCOMA'''
    #t[0] = Print(t[3],False,True, t.lineno(1), find_column(t.slice[1]))
 
def p_Println(t):
    '''Println : PRINTLN PARENTESISA exp PARENTESISC PCOMA
               | PRINTLN PARENTESISA PARENTESISC PCOMA      
    '''
    if len(t) == 6:
        t[0] = Print(t[3],True,False, t.lineno(1), find_column(t.slice[1]))
    elif len(t) == 5:
        t[0] = Print(Primitive("",typeExpression.CADENA),True,False, t.lineno(1), find_column(t.slice[1]))

def p_otherFormPrintln(t):
    'Println : PRINTLN PARENTESISA parametersCall PARENTESISC PCOMA'
    #t[0] = Print(t[3],True,True, t.lineno(1), find_column(t.slice[1]))

def p_Asignacion(t):
    ''' 
       Asignacion : ID IGUAL exp PCOMA
                  | ID IGUAL exp  DOSP DOSP  type  PCOMA
                  | ID IGUAL exp  DOSP DOSP  ID  PCOMA
    '''

    if(len(t)==5) : t[0] = Declaration(t[1],t[3],None)#,False, t.lineno(1), find_column(t.slice[1]))
    elif(len(t)==8) : t[0] = Declaration(t[1],t[3],t[6])#,False, t.lineno(1), find_column(t.slice[1]))

def p_Asignacion_entornos(t):
    '''
    Asignacion : GLOBAL ID IGUAL exp PCOMA
               | GLOBAL ID PCOMA
    '''
    #if len(t) == 6:
    #    t[0] = Declaration(t[2],t[4],None,True, t.lineno(1), find_column(t.slice[1]))
    #elif len(t) == 4:
     #   t[0] = Empty()

def p_exp(t):
    '''
    exp : exp MAS exp
        | exp MENOS exp
        | exp POR exp
        | exp DIVIDIDO exp
        | exp POTENCIA exp
        | exp PORCENTAJE exp
        | exp MAYOR exp
        | exp MENOR exp
        | exp MAYORIGUAL exp
        | exp MENORIGUAL exp
        | exp DOBLEIGUAL exp
        | exp NOIGUAL exp
        | exp OR exp
        | exp AND exp
    '''
    if t[2] == '+'  : t[0] = Plus(t[1],t[3])
    elif t[2] == '-': t[0] = Minus(t[1],t[3])
    elif t[2] == '*': t[0] = Times(t[1],t[3])
    elif t[2] == '/': t[0] = Divided(t[1],t[3])
    elif t[2] == '^': t[0] = Pow(t[1],t[3])
    elif t[2] == '%': t[0]  = Module(t[1],t[3])
    elif t[2] == '>': t[0]  = Greater(t[1],t[3])
    elif t[2] == '<': t[0]  = Less(t[1],t[3])
    elif t[2] == '>=': t[0] = GreaterOrEqual(t[1],t[3])
    elif t[2] == '<=': t[0] = LessOrEqual(t[1],t[3])
    elif t[2] == '==': t[0] = Equal(t[1],t[3])
    elif t[2] == '!=': t[0] = NotEqual(t[1],t[3])
    elif t[2] == '||': t[0] = Or(t[1],t[3])
    elif t[2] == '&&': t[0] = And(t[1],t[3])


def p_attributeStruct_exp(t):
    'exp : ID attributes'
    #t[0] = AccessStruct(t[1],t[2])

def p_attributes_exp(t):
    '''
    attributes : attributes PUNTO ID
               | PUNTO ID
    '''
    #if len(t) == 4:
    #    t[1].append(t[3])
    #    t[0] = t[1]
    #elif len(t) == 3:
    #    t[0] = [t[2]]

def p_pushArray_exp(t):
    '''
    exp : PUSH NOT PARENTESISA exp COMA parametersCall PARENTESISC  
    '''

    #t[0] = ArraysFunctions(t[4], t[6], Operations.PUSH, False, t.lineno(1), find_column(t.slice[1]))

def p_pushArray_id_exp(t):
    '''
    exp : PUSH NOT PARENTESISA ID COMA parametersCall PARENTESISC  
    '''
    #t[0] = ArraysFunctions(t[4], t[6], Operations.PUSH, True, t.lineno(1), find_column(t.slice[1]))

def p_popArray_exp(t):
    '''
    exp : POP NOT PARENTESISA exp PARENTESISC  
    '''
    #t[0] = ArraysFunctions(t[4], None, Operations.POP, False, t.lineno(1), find_column(t.slice[1]))


def p_popArray_id_exp(t):
    '''
    exp : POP NOT PARENTESISA ID PARENTESISC  
    '''
    #t[0] = ArraysFunctions(t[4], None, Operations.POP, True, t.lineno(1), find_column(t.slice[1]))

def p_lengthArray_exp(t):
    '''
    exp : LENGTH PARENTESISA exp PARENTESISC  
    '''
    t[0] = Length(t[3], False, t.lineno(1), find_column(t.slice[1]))


def p_lengthArray_id_exp(t):
    '''
    exp : LENGTH PARENTESISA ID PARENTESISC  
    '''
    t[0] = Length(t[3], True, t.lineno(1), find_column(t.slice[1]))

def p_exp_parseNative(t):
    '''
    exp : PARSE PARENTESISA type COMA exp PARENTESISC
    '''
   # t[0] = NativeDoublePar(Operations.PARSE, t[3], t[5], t.lineno(1), find_column(t.slice[1]))



def p_exp_truncNative(t):
    '''
    exp : TRUNC PARENTESISA type COMA exp PARENTESISC
        | TRUNC PARENTESISA exp PARENTESISC
    '''
    #if (len(t) == 7):
    #    t[0] = NativeDoublePar(Operations.TRUNC, t[3], t[5])
    #elif (len(t) == 5):
    #    t[0] = NativeOnePar(Operations.TRUNC, t[3], t.lineno(1), find_column(t.slice[1]))

def p_exp_floatNative(t):
    '''
    exp : FLOAT PARENTESISA exp PARENTESISC
    '''
    #t[0] = NativeOnePar(Operations.CONVERTTOFLOAT, t[3], t.lineno(1), find_column(t.slice[1]))

def p_exp_stringNative(t):
    '''
    exp : STRINGNATIVE PARENTESISA exp PARENTESISC
    '''
    #t[0] = NativeOnePar(Operations.STRINGNATIVE, t[3], t.lineno(1), find_column(t.slice[1]))

def p_exp_typeOfNative(t):
    '''
    exp : TYPEOF PARENTESISA exp PARENTESISC
    '''
    #t[0] = TypeOf(t[3], t.lineno(1), find_column(t.slice[1]))


def p_exp_array(t):
    '''
    exp : array
    '''
    t[0] = t[1]

def p_array(t):
    '''
    array : CORCHETEA parametersCall CORCHETEC
    '''
    t[0] = Array(t[2])

def p_exp_range(t):
    '''
    exp : exp DOSP exp
    '''
    t[0] = Range(t[1],t[3])

def p_exp_function(t):
    '''
    exp : ID PARENTESISA parametersCall PARENTESISC
                 | ID PARENTESISA PARENTESISC
    '''
    if len(t) == 5 : t[0] = FunctionCall(t[1], t[3], True)
    elif len(t) == 4 : t[0] = FunctionCall(t[1], [], True)

def p_exp_unaria(t):
    '''exp : MENOS exp %prec UMENOS
    '''
    if t[1] == '-' : t[0] = Negative(t[2])

def p_exp_unaria_not(t):
    '''exp : NOT exp %prec UNOT
    '''
    if t[1] == '!' : t[0] = Not(t[2])

def p_exp_agrupacion(t):
    'exp : PARENTESISA exp PARENTESISC'
    t[0] = t[2]

def p_exp_valor_entero(t):
    '''exp  : ENTERO
    '''
    t[0] = NumberVal(t[1],typeExpression.INTEGER)

def p_exp_valor_decimal(t):
    '''exp  : DECIMAL
    '''
    t[0] = NumberVal(t[1],typeExpression.FLOAT)


def p_exp_valor_cadena(t):
    '''
    exp : CADENA 
    '''
    t[0] = StringVal(t[1],typeExpression.CADENA)

def p_exp_valor_caracter(t):
    '''exp  : CARACTER
    '''
    #t[0] = Primitive(t[1],typeExpression.CHARACTER)

def p_exp_valor_booleano(t):
    '''exp  : FALSE
    '''
    t[0] = FalseVal(t[1],typeExpression.BOOL)

def p_exp_valor_true(t):
    '''exp : TRUE '''
    t[0] = TrueVal(t[1],typeExpression.BOOL)

def p_exp_valor_nothing(t):
    '''
    exp : NULO 
    '''
    #t[0] = Primitive(t[1],typeExpression.NULO)

def p_exp_valor_id(t):
    '''exp  : ID
            | ID listArray
    '''
    if len(t) == 2 : t[0] = VariableCall(t[1])
    elif len(t) == 3 : t[0] = ArrayCall(t[1],t[2], t.lineno(1), find_column(t.slice[1]))

def p_assignmentArray(t):
    '''
    assignmentArray : ID listArrayRef IGUAL exp PCOMA
    '''
    t[0] = AssignmentArray(t[1],t[2],t[4], t.lineno(1), find_column(t.slice[1]))


def p_list_array_reference(t):
    '''
    listArrayRef : listArrayRef CORCHETEA exp CORCHETEC
                 | CORCHETEA exp CORCHETEC
    '''
    if(len(t) == 5):
        t[1].append(t[3])
        t[0] = t[1]
    elif(len(t) == 4):
        t[0] = [t[2]]


def p_list_array(t):
    '''
    listArray : listArray CORCHETEA exp CORCHETEC
              | CORCHETEA exp CORCHETEC
    '''
    if(len(t) == 5):
        t[1].append(t[3])
        t[0] = t[1]
    elif(len(t) == 4):
        t[0] = [t[2]]
    #if(len(t) == 5):
    #    t[0] = ArrayCall(t[1], t[3], t.lineno(2), find_column(t.slice[2]))
    #elif(len(t) == 4):
    #    tempVar = VariableCall(t[-1])
    #    t[0] = ArrayCall(tempVar, t[2], t.lineno(1), find_column(t.slice[1]))


def p_exp_uppercase(t):
    '''exp  : UPPERCASE PARENTESISA exp PARENTESISC
    '''
    t[0] = UpperCase(t[3])

def p_exp_lowercase(t):
    '''exp  : LOWERCASE PARENTESISA exp PARENTESISC
    '''
    t[0] = LowerCase(t[3])

def p_exp_logaritmo_b10(t):
    '''exp  : LOGARITMOB10 PARENTESISA exp PARENTESISC
    '''
    #t[0] = Natives(t[3],Operations.LOGARITMO_BASE10)

def p_exp_logaritmo_no_b10(t):
    '''exp  : LOGARITMONOB10 PARENTESISA exp COMA exp PARENTESISC
    '''
    #t[0] = Arithmetic(t[3], t[5], Operations.LOGARITMO_DISTINTA_BASE)

def p_exp_seno(t):
    '''exp  : SIN PARENTESISA exp PARENTESISC
    '''
    #t[0] = Natives(t[3],Operations.SENO)

def p_exp_coseno(t):
    '''exp  : COS PARENTESISA exp PARENTESISC
    '''
    #t[0] = Natives(t[3],Operations.COSENO)

def p_exp_tangente(t):
    '''exp  : TAN PARENTESISA exp PARENTESISC
    '''
    #t[0] = Natives(t[3],Operations.TANGENTE)

def p_exp_raiz_cuadrada(t):
    '''exp  : SQRT PARENTESISA exp PARENTESISC
    '''
    #t[0] = Natives(t[3],Operations.RAIZ_CUADRADA)


def p_type_int64(t):
    'type : INT64'
    t[0] = typeExpression.INTEGER


def p_type_float64(t):
    'type : FLOAT64'
    t[0] = typeExpression.FLOAT

def p_type_string(t):
    'type : STRING'
    t[0] = typeExpression.CADENA

def p_type_char(t):
    'type : CHAR'
    t[0] = typeExpression.CARACTER

def p_type_bool(t):
    'type : BOOL'
    t[0] = typeExpression.BOOL

def p_type_nulo(t):
    'type : NULO'
    t[0] = typeExpression.NULO

def p_error(t):
    print("Error sintáctico en '%s'" % t.value," En linea: ", t.lineno+1)

import ply.yacc as yacc
parser = yacc.yacc()
#OBTENER LA ENTRADA 
input = ""

#FUNCION PARA SETEAR LA ENTRADA EN LA VARIABLE INPUT
def set_input(inputFunc):
    global input
    input = ""
    input = inputFunc

#FUNCION PARA ENCONTRAR EL NUMERO DE COLUMNA
def find_column(token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    #print(token.lexpos , " ", line_start)
    return (token.lexpos - line_start) + 1

'''f = open("./entrada.txt", "r")
input = f.read()
print(input)
parser.parse(input)'''