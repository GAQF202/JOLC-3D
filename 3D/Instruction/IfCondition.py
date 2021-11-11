from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class IfCondition(Instruction):

    def __init__(self, condition:Expression, block, elseIfBlock, elseBlock, line, column) -> None:
        super().__init__()
        self.condition = condition
        self.block = block
        self.elseIfBlock = elseIfBlock
        self.elseBlock = elseBlock
        self.line = line
        self.column = column

    def compile(self, environment:Environment) -> Value:
        #EVALUA LA EXPRESION
        self.condition.generator = self.generator
        condition = self.condition.compile(environment)

        labelTrue = self.generator.newLabel()
        labelFalse = self.generator.newLabel()
        jumpLabel = self.generator.newLabel()
        self.generator.addIf(condition.value,'1','==',labelTrue)
        self.generator.addGoto(labelFalse)
        self.generator.addLabel(labelTrue)
        #EJECUTA LAS INSTRUCCIONES 
        self.block.generator = self.generator #SE PASA EL GENERADOR ACTUAL AL GENERADOR DE BLOQUE
        self.block.compile(environment)
        self.generator.addGoto(jumpLabel)
        #print(jumpLabel)
        self.generator.addLabel(labelFalse)

        #RECORRE LA LISTA DE ELSEIF QUE SE LE ENVIA
        if(self.elseIfBlock != None): 
            for elseif in self.elseIfBlock:
                elseif.generator = self.generator
                elseif.compile(environment,jumpLabel)
                #self.generator.addGoto(jumpLabel)
        if(self.elseBlock != None):
            self.elseBlock.generator = self.generator
            self.elseBlock.compile(environment)
            self.generator.addGoto(jumpLabel)
        
        self.generator.addLabel(jumpLabel)


        '''if(t0 == 1){goto L0}
        goto L1
        L0:
        instrucciones
        goto L2
        L1:

        if(t0 == 1){goto L0}
        goto L1
        L0:
        instrucciones
        goto L2
        L1:
        if(t1 == 1){'''

