from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class Greater(Expression):

    def __init__(self, left:Expression, right:Expression) -> None:
        super().__init__()
        self.leftExpression = left
        self.rightExpression = right
    
    def compile(self, environment:Environment) -> Value:
        self.leftExpression.generator = self.generator
        self.rightExpression.generator = self.generator

        leftValue: Value = self.leftExpression.compile(environment)
        rightValue: Value = self.rightExpression.compile(environment)

        #TEMPORAL PARA GUARDAR EL RESULTADO
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

        if(rightValue.type == typeExpression.INTEGER or rightValue.type == typeExpression.FLOAT):
            if(leftValue.type == typeExpression.INTEGER or leftValue.typeExpression.FLOAT):
                
                newValue = Value(newTemp,False,typeExpression.BOOL)

                if(self.trueLabel == ""):
                    self.trueLabel = self.generator.newLabel()
                
                if(self.falseLabel == ""):
                    self.falseLabel = self.generator.newLabel()

                self.generator.addIf(leftValue.value, rightValue.value, ">", self.trueLabel)

                self.generator.addGoto(self.falseLabel)

                self.generator.addLabel(self.trueLabel)
                self.generator.addExpression(newTemp,'1','','')
                jumpLabel = self.generator.newLabel()
                self.generator.addGoto(jumpLabel)
                self.generator.addLabel(self.falseLabel)
                self.generator.addExpression(newTemp,'0','','')
                self.generator.addLabel(jumpLabel)

                #newValue.trueLabel = self.trueLabel
                #newValue.falseLabel = self.falseLabel
                return newValue

        if(rightValue.type == typeExpression.CADENA):
            if(leftValue.type == typeExpression.CADENA):
                newValue = Value(newTemp,False,typeExpression.BOOL)
                self.generator.addExpression(leftValue.value,leftValue.value,'1','+')
                self.generator.addExpression(rightValue.value,rightValue.value,'1','+')
                leftString = self.generator.newTemp()
                rightString = self.generator.newTemp()
                self.generator.addGetHeap(leftString,leftValue.value)
                self.generator.addGetHeap(rightString,rightValue.value)
                labelTrue = self.generator.newLabel()
                falseLabel = self.generator.newLabel()
                jumpLabel = self.generator.newLabel()
                self.generator.addIf(leftString,rightString,'>',labelTrue)
                self.generator.addGoto(falseLabel)
                self.generator.addLabel(labelTrue)
                self.generator.addExpression(newTemp,'1','','')
                self.generator.addGoto(jumpLabel)
                self.generator.addLabel(falseLabel)
                self.generator.addExpression(newTemp,'0','','')
                self.generator.addLabel(jumpLabel)
                return newValue
            else:
                print("Error en el mayor que")



