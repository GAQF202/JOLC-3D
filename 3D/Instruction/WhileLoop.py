from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class WhileLoop(Instruction):

    def __init__(self, condition:Expression, block) -> None:
        super().__init__()
        self.condition = condition
        self.block = block

    def compile(self, environment:Environment) -> Value:
        #EVALUA LA EXPRESION
        initLabel = self.generator.newLabel()
        self.condition.generator = self.generator
        self.generator.addLabel(initLabel)
        condition = self.condition.compile(environment)

        labelTrue = self.generator.newLabel()
        labelFalse = self.generator.newLabel()

        self.generator.addIf(condition.value,'1','==',labelTrue)
        self.generator.addGoto(labelFalse)
        self.generator.addLabel(labelTrue)
        self.block.generator = self.generator
        self.block.compile(environment)
        self.generator.addGoto(initLabel)
        self.generator.addLabel(labelFalse)


        '''
        L3:
        if(t0 == 1){goto L0}
        goto L1
        L0:
        instrucciones
        goto L3
        L1:
        '''

