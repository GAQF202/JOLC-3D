from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class ElseIfCondition(Instruction):

    def __init__(self, condition:Expression, block) -> None:
        super().__init__()
        self.condition = condition
        self.block = block

    def compile(self, environment:Environment, jumpLabel) -> Value:
        #EVALUA LA EXPRESION
        self.condition.generator = self.generator
        condition = self.condition.compile(environment)

        labelTrue = self.generator.newLabel()
        labelFalse = self.generator.newLabel()
        self.generator.addIf(condition.value,'1','==',labelTrue)
        self.generator.addGoto(labelFalse)
        self.generator.addLabel(labelTrue)
        #EJECUTA LAS INSTRUCCIONES 
        self.block.generator = self.generator #SE PASA EL GENERADOR ACTUAL AL GENERADOR DE BLOQUE
        self.block.compile(environment)
        self.generator.addGoto(jumpLabel)
        self.generator.addLabel(labelFalse)
