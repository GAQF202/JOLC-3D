from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class BlockLoop(Instruction):

    def __init__(self, block) -> None:
        super().__init__()
        self.block = block

    def compile(self, environment:Environment) -> Value:

        #EJECUTA EL BLOQUE DE CODIGO QUE SE ENVIA
        for instruction in self.block:
            if(instruction != None):
                instruction.generator = self.generator
                instruction.compile(environment)        

