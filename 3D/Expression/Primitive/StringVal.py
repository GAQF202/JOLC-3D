from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class StringVal(Expression):

    def __init__(self, value, type: typeExpression) -> None:
        super().__init__()
        self.type = type
        self.value = value

    def compile(self, environment: Environment) -> Value:
        
        if(self.type == typeExpression.CADENA ):
            newTemp = self.generator.newTemp()  
            self.generator.addExpression(newTemp,'H','0',"+")
            self.generator.addSetHeap("H",str(len(self.value)+1))
            self.generator.addNextHeap()

            for character in self.value:
                self.generator.addSetHeap("H",str(ord(character)))
                self.generator.addNextHeap()

            return Value(newTemp,True,typeExpression.CADENA)

        print("No se reconoce el tipo")
        return Value("0",False,typeExpression.INTEGER)