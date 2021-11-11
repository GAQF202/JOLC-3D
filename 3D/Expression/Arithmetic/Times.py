from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class Times(Expression):

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
                self.generator.addExpression(newTemp,leftValue.getValue(),rightValue.getValue(),"*")
                return Value(newTemp,True,rightValue.type)
            else:
                print("Error en multiplicacion")
                return Value("0",False,typeExpression.INTEGER)

        elif(leftValue.type == typeExpression.FLOAT):
            if(rightValue.type == typeExpression.INTEGER or rightValue.type == typeExpression.FLOAT):
                self.generator.addExpression(newTemp,leftValue.getValue(),rightValue.getValue(),"*")
                return Value(newTemp,True,typeExpression.FLOAT)
            else:
                print("Error en multiplicacion")
                return Value("0",False,typeExpression.INTEGER)

        elif(leftValue.type == typeExpression.CADENA):
            if(rightValue.type == typeExpression.CADENA):
                self.generator.addExpression(newTemp,'H','0','+')
                tempLeft = self.generator.newTemp()
                tempRight = self.generator.newTemp()
                self.generator.addGetHeap(tempLeft,leftValue.value)
                self.generator.addGetHeap(tempRight,rightValue.value)
                sizeTemp = self.generator.newTemp()
                self.generator.addExpression(sizeTemp,tempLeft,tempRight,'+')
                self.generator.addExpression(sizeTemp,sizeTemp,'1','-')
                self.generator.addSetHeap('H',sizeTemp)
                self.generator.addNextHeap()

                #self.getString(leftValue.value)
                #self.getString(rightValue.value)
                leftValue.getString(self.generator)
                rightValue.getString(self.generator)

                #print(leftValue.value,rightValue.value)
                return Value(newTemp,True,typeExpression.CADENA)
        else:
            print("Error los tipos no se pueden multiplicar")

    #METODO PARA OBTENER LOS VALORES DEL STRING
    def getString(self,tempValue):
        newTemp = self.generator.newTemp()
        self.generator.addGetHeap(newTemp, tempValue)
        top = self.generator.newTemp()
        self.generator.addExpression(top,tempValue,'1','+')
        cont = self.generator.newTemp()
        self.generator.addExpression(cont,newTemp,tempValue,'+')

        newLabel = self.generator.newLabel()
        self.generator.addLabel(newLabel)

        labelTrue = self.generator.newLabel()
        labelFalse = self.generator.newLabel()
        self.generator.addIf(top,cont,'<',labelTrue)
        self.generator.addGoto(labelFalse)
        self.generator.addLabel(labelTrue)
        tempHeap = self.generator.newTemp()
        self.generator.addGetHeap(tempHeap,top)
        self.generator.addSetHeap('H',tempHeap)
        self.generator.addNextHeap()
        self.generator.addExpression(top,top,'1','+')
        self.generator.addGoto(newLabel)
        self.generator.addLabel(labelFalse)
