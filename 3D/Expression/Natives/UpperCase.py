from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class UpperCase(Expression):

    def __init__(self, expression:Expression) -> None:
        super().__init__()
        self.expression = expression

    def compile(self, environment: Environment) -> Value:

        self.expression.generator = self.generator
        expression = self.expression.compile(environment)
        
        #SI ES UN ARRAY ME MUEVO AL VALOR REAL Y LE PASO EL TIPO DEL ARRAY AL VALOR
        if(expression.type == typeExpression.ARRAY):
            tempAccess = self.generator.newTemp()
            self.generator.addExpression(tempAccess,expression.value,'1','+' )
            self.generator.addGetHeap(expression.value,tempAccess)
            expression = Value(expression.value,True,expression.typeArray)
        #-----------------------------------------------------------------------------
        
        if(expression.type == typeExpression.CADENA):
            newTemp = self.generator.newTemp()
            self.generator.addExpression(newTemp,'H','','') #GUARDO LA POSICION DONDE INICIA EN EL HEAP

            sizeTemp = self.generator.newTemp()
            self.generator.addGetHeap(sizeTemp,expression.value)
    
            #LE PASO EL MISMO TAMANIO AL STRING RESULTANTE
            self.generator.addSetHeap('H',sizeTemp)
            self.generator.addNextHeap()

            self.generator.addExpression(sizeTemp,sizeTemp,'1','-')
            topTemp = self.generator.newTemp()
            self.generator.addExpression(topTemp,sizeTemp,expression.value,'+')

            initLabel = self.generator.newLabel() #ETIQUETA DE INICIO
            self.generator.addLabel(initLabel)

            self.generator.addExpression(expression.value,expression.value,'1','+') #CONTADOR
            labelTrue = self.generator.newLabel()
            labelFalse = self.generator.newLabel()
            self.generator.addIf(expression.value,topTemp,'<=',labelTrue)
            self.generator.addGoto(labelFalse)

            self.generator.addLabel(labelTrue)
            tempHeap = self.generator.newTemp()
            self.generator.addGetHeap(tempHeap,expression.value) #OBTENGO EL VALOR DEL HEAP

            labelContinue = self.generator.newLabel()
            changeLabel = self.generator.newLabel() #POSICION PARA CONVERITR DE MAYUSCULA A MINUSCULA

            #VERIFICA QUE SEA UNA LETRA EN MINUSCULA DE LA A-Z
            jumpLabel = self.generator.newLabel()
            self.generator.addIf(tempHeap,'97','>=',labelContinue)
            self.generator.addGoto(jumpLabel)
            self.generator.addLabel(labelContinue)
            self.generator.addIf(tempHeap,'122','<=',changeLabel)
            self.generator.addGoto(jumpLabel)
            #CAMBIO DE MAYUSCULA A MINUSCULA
            self.generator.addLabel(changeLabel)
            tempChange = self.generator.newTemp() #SE CREA EL TEMPORAL PARA CALCULO DE CAMBIO
            #CAMBIA LA EXPRESION Y LA ASIGNA AL HEAP
            self.generator.addExpression(tempChange,tempHeap,'32','-')
            self.generator.addSetHeap('H',tempChange)
            self.generator.addNextHeap()
            self.generator.addGoto(initLabel)

            #SI NO ES UNA LETRA MINUSCULA ASIGNA EL VALOR POR DEFECTO
            self.generator.addLabel(jumpLabel)
            self.generator.addSetHeap('H',tempHeap)
            self.generator.addNextHeap()
            self.generator.addGoto(initLabel)

            self.generator.addLabel(labelFalse)
            self.generator.addJumpLine()

            return Value(newTemp,True,typeExpression.CADENA)

        print("Se esperaba una cadena en el uppercase")
        return Value("0",False,typeExpression.INTEGER)