from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class Print(Instruction):

    def __init__(self, exp: Expression, saltoDeLinea : bool, isList : bool, line, column) -> None:
        super().__init__()
        self.exp = exp
        self.saltoDeLinea = saltoDeLinea
        self.isList = isList
        self.line = line
        self.column = column

    def compile(self, environment: Environment) -> Value:
        self.exp.generator = self.generator
        tempValue: Value = self.exp.compile(environment)

        #IMPRIMO COM FLOAT PARA QUE EVITAR ERROR EN GO
        #if(tempValue.type == typeExpression.INTEGER):
         #   self.generator.addPrintf("d","int(" + str(tempValue.getValue()) + ")")

        if(tempValue.type == typeExpression.FLOAT or tempValue.type == typeExpression.INTEGER):
            self.generator.addPrintf("f","float64(" + str(tempValue.getValue()) + ")")
        
        elif(tempValue.type == typeExpression.CADENA):
            newTemp = self.generator.newTemp()
            self.generator.addGetHeap(newTemp, tempValue.value)
            top = self.generator.newTemp()
            self.generator.addExpression(top,tempValue.value,'1','+')
            cont = self.generator.newTemp()
            self.generator.addExpression(cont,newTemp,tempValue.value,'+')

            newLabel = self.generator.newLabel()
            self.generator.addLabel(newLabel)

            labelTrue = self.generator.newLabel()
            labelFalse = self.generator.newLabel()
            self.generator.addIf(top,cont,'<',labelTrue)
            self.generator.addGoto(labelFalse)
            self.generator.addLabel(labelTrue)
            tempHeap = self.generator.newTemp()
            self.generator.addGetHeap(tempHeap,top)
            self.generator.addPrintf('c',"int(" + tempHeap + ")")
            self.generator.addExpression(top,top,'1','+')
            self.generator.addGoto(newLabel)
            self.generator.addLabel(labelFalse)

        elif(tempValue.type == typeExpression.ARRAY):

            tempSize = self.generator.newTemp()
            tempPos = self.generator.newTemp()
            self.generator.addExpression(tempSize,'P',str(environment.size),'+') #SUMO EL TAMANIO DEL ENTORNO
            self.generator.addExpression(tempPos,tempSize,'0','+') #ENVIO A LA POSICION DEL PARAMETRO

            labelPrintArray = self.generator.newLabel()
            labelPrintOther = self.generator.newLabel()
            tempType = self.generator.newTemp()
            self.generator.addGetHeap(tempType,tempValue.value)
            tempMarca = self.generator.newTemp()
            self.generator.addExpression(tempMarca,'0','0.0001','-')
            jumpLabel = self.generator.newLabel()
            self.generator.addIf(tempType,tempMarca,'!=',labelPrintArray)
            self.generator.addGoto(labelPrintOther)

            #-----------------ARRAY-----------------------
            self.generator.addLabel(labelPrintArray)
            self.generator.addSetStack(tempPos,tempValue.value)

            self.generator.addExpression('P','P',str(environment.size),'+')
            if tempValue.typeArray == typeExpression.INTEGER:
                self.generator.addCallFunc('jolc_print_array_integer')
            elif tempValue.typeArray == typeExpression.FLOAT:
                self.generator.addCallFunc('jolc_print_array_float')
            elif tempValue.typeArray == typeExpression.BOOL:
                self.generator.addCallFunc('jolc_print_array_bool')
            elif tempValue.typeArray == typeExpression.CADENA:
                self.generator.addCallFunc('jolc_print_array_string')
            self.generator.addExpression('P','P',str(environment.size),'-')
            self.generator.addGoto(jumpLabel) #SALTO AL FINAL

            #------------------OTROS TIPOS------------------
            self.generator.addLabel(labelPrintOther)
            tempAccess = self.generator.newTemp()
            self.generator.addExpression(tempAccess,tempValue.value,'1','+') #ACCEDO A LA POSICION REAL DEL VALOR
            

            self.generator.addExpression('P','P',str(environment.size),'+')

            #SI NO ES UNA CADENA LE ENVIO EL VALOR EN VEZ DE LA POSICION COMO EN LOS STIRNGS
            if tempValue.typeArray != typeExpression.CADENA:
                realTemp = self.generator.newTemp()
                self.generator.addGetHeap(realTemp,tempAccess)
                self.generator.addSetStack(tempPos,realTemp)

            if tempValue.typeArray == typeExpression.INTEGER:
                self.generator.addCallFunc('jolc_print_integer')
            elif tempValue.typeArray == typeExpression.FLOAT:
                self.generator.addCallFunc('jolc_print_float')
            elif tempValue.typeArray == typeExpression.BOOL:
                self.generator.addCallFunc('jolc_print_bool')
            elif tempValue.typeArray == typeExpression.CADENA:
                #SI ES STRING SI ENVIO LA POSICION 
                self.generator.addSetStack(tempPos,tempAccess)
                self.generator.addCallFunc('jolc_print_string')
            self.generator.addExpression('P','P',str(environment.size),'-')

            self.generator.addLabel(jumpLabel)

        elif(tempValue.type == typeExpression.BOOL):

            trueLabel = self.generator.newLabel()
            falseLabel = self.generator.newLabel()
            jumpLabel = self.generator.newLabel()
            self.generator.addIf(tempValue.value, '1', "==", trueLabel)
            self.generator.addGoto(falseLabel)
            self.generator.addLabel(trueLabel)
            self.generator.addCallFunc("print_true")
            self.generator.addGoto(jumpLabel)
            self.generator.addLabel(falseLabel)
            self.generator.addCallFunc("print_false")
            self.generator.addLabel(jumpLabel)
        else:
            print("Error en print")

        if self.saltoDeLinea:   
            self.generator.addNewLine()
    
    #METODO PARA IMPRIMIR VALORES QUE NO SON EXPRESIONES
    def printValue(self,tempValue):

        if(tempValue.type == typeExpression.FLOAT or tempValue.type == typeExpression.INTEGER):
            self.generator.addPrintf("f","float64(" + str(tempValue.getValue()) + ")")
        
        elif(tempValue.type == typeExpression.CADENA):
            newTemp = self.generator.newTemp()
            self.generator.addGetHeap(newTemp, tempValue.value)
            top = self.generator.newTemp()
            self.generator.addExpression(top,tempValue.value,'1','+')
            cont = self.generator.newTemp()
            self.generator.addExpression(cont,newTemp,tempValue.value,'+')

            newLabel = self.generator.newLabel()
            self.generator.addLabel(newLabel)

            labelTrue = self.generator.newLabel()
            labelFalse = self.generator.newLabel()
            self.generator.addIf(top,cont,'<',labelTrue)
            self.generator.addGoto(labelFalse)
            self.generator.addLabel(labelTrue)
            tempHeap = self.generator.newTemp()
            self.generator.addGetHeap(tempHeap,top)
            self.generator.addPrintf('c',"int(" + tempHeap + ")")
            self.generator.addExpression(top,top,'1','+')
            self.generator.addGoto(newLabel)
            self.generator.addLabel(labelFalse)

        elif(tempValue.type == typeExpression.ARRAY):
            self.generator.addPrintf('c',"int(" + str(ord('[')) + ")")
            #RECORRE LA LISTA DE VALORES QUE ESTAN ALMACENADOS EN EL ARREGLO
            for value in tempValue.arrayValues:
                if tempValue.arrayValues.index(value) != 0:
                    self.generator.addPrintf('c',"int(" + str(ord(',')) + ")")
                self.printValue(value)
            self.generator.addPrintf('c',"int(" + str(ord(']')) + ")")

        elif(tempValue.type == typeExpression.BOOL):

            trueLabel = self.generator.newLabel()
            falseLabel = self.generator.newLabel()
            jumpLabel = self.generator.newLabel()
            self.generator.addIf(tempValue.value, '1', "==", trueLabel)
            self.generator.addGoto(falseLabel)
            self.generator.addLabel(trueLabel)
            self.generator.addCallFunc("print_true")
            self.generator.addGoto(jumpLabel)
            self.generator.addLabel(falseLabel)
            self.generator.addCallFunc("print_false")
            self.generator.addLabel(jumpLabel)
        else:
            print("Error en print")