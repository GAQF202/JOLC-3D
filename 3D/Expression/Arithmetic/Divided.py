from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class Divided(Expression):

    def __init__(self, left: Expression, right: Expression):
        super().__init__()
        self.leftExpression = left
        self.rightExpression = right

    def compile(self, environment: Environment) -> Value:
        self.leftExpression.generator = self.generator
        self.rightExpression.generator = self.generator

        leftValue : Value = self.leftExpression.compile(environment)
        rightValue : Value = self.rightExpression.compile(environment)
        newTemp = self.generator.newTemp()
        
        #SI ES UN ARRAY ME MUEVO AL VALOR REAL Y LE PASO EL TIPO DEL ARRAY AL VALOR
        if(leftValue.type == typeExpression.ARRAY):
            tempAccess = self.generator.newTemp()
            self.generator.addExpression(tempAccess,leftValue.value,'1','+' )
            self.generator.addGetHeap(leftValue.value,tempAccess)
            leftValue = Value(leftValue.value,True,leftValue.typeArray)
        if(rightValue.type == typeExpression.ARRAY):
            tempAccess = self.generator.newTemp()
            self.generator.addExpression(tempAccess,rightValue.value,'1','+' )
            self.generator.addGetHeap(rightValue.value,tempAccess)
            rightValue = Value(rightValue.value,True,rightValue.typeArray)
        #-----------------------------------------------------------------------------

        if(leftValue.type == typeExpression.INTEGER):
            if(rightValue.type == typeExpression.INTEGER or rightValue.type == typeExpression.FLOAT):
                self.generator.addExpression(newTemp,leftValue.getValue(),rightValue.getValue(),"/")
                return Value(newTemp,True,rightValue.type)
            else:
                print("Error en division")
                return Value("0",False,typeExpression.INTEGER)

        elif(leftValue.type == typeExpression.FLOAT):
            if(rightValue.type == typeExpression.INTEGER or rightValue.type == typeExpression.FLOAT):
                self.generator.addExpression(newTemp,leftValue.getValue(),rightValue.getValue(),"/")
                return Value(newTemp,True,rightValue.FLOAT)
            else:
                print("Error en division")
                return Value("0",False,typeExpression.INTEGER)
        else:
            return Value("0",False,typeExpression.INTEGER)
            print("Error los tipos no se pueden restar")
