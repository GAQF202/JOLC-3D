from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class Array(Expression):

    def __init__(self, values) -> None:
        super().__init__()
        self.values = values
        #self.isPrincipal = True #PARA SABER SI ES EL ARRAY QUE CONTIENE AL RESTO

    def compile(self, environment: Environment) -> Value:
        
        #TEMPORAL PARA EL APUNTADOR EN EL HEAP
        newTemp = self.generator.newTemp()
        #VALOR DE RETORNO
        newValue = Value(newTemp,True,typeExpression.ARRAY)
        #GUARDO LAS EXPRESIONES PARA MANEJO DENTRO DEL CODIGO
        arrayValues = []

        self.generator.addExpression(newTemp,'H','','') #GUARDO LA POSICION DEL HEAP COMO APUNTADOR

        tempMarcador = self.generator.newTemp() #TEMPORAL PARA MARCAR QUE ES UN ARRAY
        self.generator.addExpression(tempMarcador,'0','0.0003','-')
        self.generator.addSetHeap('H',tempMarcador) #GUARDO EL MARCADOR EN LA PRIMERA POSICION DEL ARRAY
        self.generator.addNextHeap() #AUMENTO EL HEAP

        tempMarcador2 = self.generator.newTemp()
        self.generator.addExpression(tempMarcador2,'0','0.0001','-')

        tempMove = self.generator.newTemp() #TEMPORAL PARA MOVERSE EN EL HEAP
        self.generator.addExpression(tempMove,newTemp,'2','+') #LE SUMO UNO PARA NO TOMAR EN CUENTA EL TAMANIO
        
        totalSize = len(self.values) #GUARDO EL TAMANIO PRINCIPAL DEL ARRAY

        #ARREGLAAAAR
        for i in self.values:
            totalSize += 1
            #if(isinstance(i,Array)):
             #   totalSize += 1 #AUMENTO CADA VEZ QUE HAY UN ARREGLO PARA GUARDAR EL MARCADOR

        #GUARDO EL TAMANIO
        self.generator.addSetHeap('H',str(totalSize))
        self.generator.addNextHeap()

        #RESERVO LOS ESPACIOS EN EL HEAP
        for exp in range(totalSize):
            self.generator.addNextHeap()

        for exp in self.values:
            exp.generator = self.generator

            valExp = exp.compile(environment) #EJECUTA LA EXPRESION

            if valExp.type != typeExpression.ARRAY: #GUARDA LA EXPRESION EXCLUYENDO LA DEL ARRAY 
                newValue.typeArray = valExp.type #TODAS LAS EXPRESIONES DEBEN SER DEL MISMO TIPO
                self.generator.addSetHeap(tempMove,tempMarcador2) #MARCO DENTRO DEL ARREGLO PRINCIPAL QUE ES OTRO TIPO
                self.generator.addExpression(tempMove,tempMove,'1','+') #AUMENTO EN UNO LA POSICION
            else:
                newValue.typeArray = valExp.typeArray #SI NO ES DE TIPO ARRAY HEREDA EL TIPO DEL HIJO
                self.generator.addSetHeap(tempMove,tempMarcador) #MARCO DENTRO DEL ARREGLO PRINCIPAL QUE ES UN ARREGLO
                self.generator.addExpression(tempMove,tempMove,'1','+') #AUMENTO EN UNO LA POSICION


            arrayValues.append(valExp)

            self.generator.addSetHeap(tempMove,valExp.getValue()) #GUARDO LA EXPRESION
            self.generator.addExpression(tempMove,tempMove,'1','+') #AUMENTO EN UNO AL POSICION
        
        #LE PASO LAS EXPRESIONES RESUELTAS
        newValue.arrayValues = arrayValues
        return newValue




        