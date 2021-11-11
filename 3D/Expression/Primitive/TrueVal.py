from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class TrueVal(Expression):

    def __init__(self, value, type: typeExpression) -> None:
        super().__init__()
        self.type = type
        self.value = value

    def compile(self, environment: Environment) -> Value:
        
        if(self.type == typeExpression.BOOL):
            newTemp = self.generator.newTemp()
            self.generator.addExpression(newTemp,'1','','')
            return Value(newTemp,True,typeExpression.BOOL)

        print("No se reconoce el tipo")
        return Value("0",False,typeExpression.INTEGER)