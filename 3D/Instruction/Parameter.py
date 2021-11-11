from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class Parameter(Instruction):

    def __init__(self, id:str, type: typeExpression, line, column) -> None:
        super().__init__()
        self.id = id
        self.type = type
        self.line = line
        self.column = column

    def compile(self, environment:Environment) -> Value:
        self.generator = self.generator
        tempVar: Symbol = environment.saveVariable(self.id,self.type,[],'','','')

        #if(self.type != typeExpression.BOOL):
         #   self.generator.addSetStack(str(tempVar.position),'\'\'')
        #else:
         #   self.generator.addSetStack(str(tempVar.position),'\'\'')
