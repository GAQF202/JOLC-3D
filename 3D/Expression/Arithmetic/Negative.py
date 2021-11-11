from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class Negative(Expression):

    def __init__(self, left: Expression):
        super().__init__()
        self.leftExpression = left

    def compile(self, environment: Environment) -> Value:
        self.leftExpression.generator = self.generator

        leftValue : Value = self.leftExpression.compile(environment)
        newTemp = self.generator.newTemp()
        
        #SI ES UN ARRAY ME MUEVO AL VALOR REAL Y LE PASO EL TIPO DEL ARRAY AL VALOR
        if(leftValue.type == typeExpression.ARRAY):
            tempAccess = self.generator.newTemp()
            self.generator.addExpression(tempAccess,leftValue.value,'1','+' )
            self.generator.addGetHeap(leftValue.value,tempAccess)
            leftValue = Value(leftValue.value,True,leftValue.typeArray)
        #-----------------------------------------------------------------------------

        if(leftValue.type == typeExpression.INTEGER):
            self.generator.addExpression(newTemp,'0',leftValue.getValue(),"-")
            return Value(newTemp,True,typeExpression.INTEGER)

        elif(leftValue.type == typeExpression.FLOAT):
            self.generator.addExpression(newTemp,'0',leftValue.getValue(),"-")
            return Value(newTemp,True,typeExpression.FLOAT)
        else:
            print("Error los tipos no puede ser negativo")


