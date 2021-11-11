from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class ArrayCall(Instruction):

    def __init__(self, id: str, positions, line, column) -> None:
        super().__init__()
        self.id = id
        self.positions = positions
        self.line = line
        self.column = column

    def compile(self, environment:Environment) -> Value:
        
        arrayFound = environment.getVariable(self.id) #BUSCA LA VARIABLE EN EL ENTORNO

        labelNotArray = self.generator.newLabel() #ETIQUETA PARA QUE SALGA Y MARQUE EL ERROR QUE NO ES ARRAY
        labelOutRange = self.generator.newLabel() #ETIQUETA PARA QUE MARQUE EL ERROR FUERA DE RANGO
        labelEnd = self.generator.newLabel() #LABEL PARA SALIR DE LA INSTRUCCION

        tempPos = self.generator.newTemp() #PRIMERA POSICION EN EL HEAP
        tempSize = self.generator.newTemp() #TAMAÑO DEL ARREGLO GUARDADO EN EL HEAP
        tempType = self.generator.newTemp() #PARA GUARDAR EL TIPO DENTRO DEL CODIGO INTERMEDIO
        tempMove = self.generator.newTemp() #PARA MOVERME EN EL HEAP SIN AFECTAR LA POSICION ABSOLUTA
        newTemp = self.generator.newTemp() #TEMPORAL PARA ENVIAR EN EL VALOR DE RETORNO
        newValue = Value(newTemp,True,typeExpression.ARRAY) #VALOR DE RETORNO EN LA EXPRESION
        newValue.typeArray = arrayFound.typeArray

        tempMarca = self.generator.newTemp()
        self.generator.addExpression(tempMarca,'0','0.0003','-') #OPERO LA MARCA

        self.generator.addGetStack(tempPos,str(arrayFound.position)) #OBTENGO EL APUNTADOR AL HEAP 
        self.generator.addGetHeap(tempType,tempPos) #OBTENGO EL TIPO INTERNO
        self.generator.addExpression(tempMove,tempPos,'1','+') #ME MUEVO HACIA EL TAMANIO
        self.generator.addGetHeap(tempSize,tempMove) #OBTENGO EL TAMANIO DEL ARREGLO CON LA POSICION DEL HEAP
        self.generator.addExpression(tempSize,tempSize,'2','/') #CALCULO EL TAMANIO REAL

        for position in self.positions:
            position.generator = self.generator #LE PASO EL GENERADOR A LAS EXPRESIONES
            index = position.compile(environment) #COMPILA LOS INDICES DE LA LLAMADA

            if (self.positions.index(position) == 0):
                
                labelTrue = self.generator.newLabel()
                self.generator.addIf(index.value,tempSize,'<=',labelTrue)
                self.generator.addGoto(labelOutRange)
                self.generator.addLabel(labelTrue)

                #SI ES SOLO UNA POSICION
                if len(self.positions) == 1:
                    tempAux = self.generator.newTemp() #AUXILIAR PARA MULTIPLICAR EL INDICE X2
                    self.generator.addExpression(tempAux,index.value,'2','*') #OBTENGO LA POSICION REAL
                    self.generator.addExpression(tempPos,tempPos,tempAux,'+')
                    self.generator.addGetHeap(tempType,tempPos) 
                    self.generator.addExpression(tempMove,tempPos,'1','+') 
                    self.generator.addComment("------------------------------------")
                    #VERIFICADOR DE TIPO
                    makeArray = self.generator.newLabel() 
                    makeOther = self.generator.newLabel()
                    self.generator.addIf(tempType,tempMarca,'==',makeArray)
                    self.generator.addGoto(makeOther)
                    #MANDO EL TEMPORAL COMO ARREGLO
                    self.generator.addLabel(makeArray)
                    self.generator.addGetHeap(newTemp,tempMove) #ASIGNO AL VALOR DE RETORNO
                    self.generator.addGoto(labelEnd) #FINALIZO LA EJECUCION SIN ERRORES
                    #MANDO EL TEMPORAL CON EL VALOR DE CUALQUIER TIPO PRIMITIVO
                    self.generator.addLabel(makeOther)
                    self.generator.addExpression(newTemp,tempPos,'','') #ASIGNO AL VALOR DE RETORNO
                    self.generator.addGoto(labelEnd) #FINALIZO LA EJECUCION SIN ERRORES

                else:      
                    jumpLabel = self.generator.newLabel()
                    tempAux = self.generator.newTemp()
                    self.generator.addExpression(tempAux,index.value,'2','*') #OBTENGO LA POSICION REAL
                    self.generator.addExpression(tempPos,tempPos,tempAux,'+')
                    self.generator.addGetHeap(tempType,tempPos)
                    labelContinue = self.generator.newLabel()
                    self.generator.addIf(tempType,tempMarca,'==',labelContinue)
                    self.generator.addGoto(labelNotArray)

                    self.generator.addLabel(labelContinue)
                    self.generator.addExpression(tempMove,tempPos,'1','+')
                    self.generator.addGetHeap(tempPos,tempMove)
                    self.generator.addGetHeap(tempType,tempPos)
                    self.generator.addExpression(tempMove,tempPos,'1','+')
                    self.generator.addGetHeap(tempSize,tempMove)
                    self.generator.addExpression(tempSize,tempSize,'2','/')

                    self.generator.addGoto(jumpLabel) #SALTA DEL ERROR 

                    #------MARCA QUE NO ES UN ARRAY------
                    self.generator.addLabel(labelNotArray)
                    self.generator.addPrintf('c',str(ord('N')))
                    self.generator.addPrintf('c',str(ord('I')))
                    self.generator.addPrintf('c',str(ord('A')))
                    self.generator.addGoto(labelEnd)

                    self.generator.addLabel(jumpLabel)

            #SI ES EL ULTIMO INDICE
            elif (self.positions.index(position) == (len(self.positions)-1)):

                labelTrue = self.generator.newLabel()
                self.generator.addIf(index.value,tempSize,'<=',labelTrue)
                self.generator.addGoto(labelOutRange)
                self.generator.addLabel(labelTrue)
                tempAux = self.generator.newTemp() #AUXILIAR PARA MULTIPLICAR EL INDICE X2
                self.generator.addExpression(tempAux,index.value,'2','*') #OBTENGO LA POSICION REAL
                self.generator.addExpression(tempPos,tempPos,tempAux,'+')
                self.generator.addGetHeap(tempType,tempPos)
                self.generator.addExpression(tempMove,tempPos,'1','+')

                self.generator.addComment("------------------------------------")
                #VERIFICADOR DE TIPO
                makeArray = self.generator.newLabel() 
                makeOther = self.generator.newLabel()
                self.generator.addIf(tempType,tempMarca,'==',makeArray)
                self.generator.addGoto(makeOther)
                #MANDO EL TEMPORAL COMO ARREGLO
                self.generator.addLabel(makeArray)
                self.generator.addGetHeap(newTemp,tempMove) #ASIGNO AL VALOR DE RETORNO
                self.generator.addGoto(labelEnd) #FINALIZO LA EJECUCION SIN ERRORES
                #MANDO EL TEMPORAL CON EL VALOR DE CUALQUIER TIPO PRIMITIVO
                self.generator.addLabel(makeOther)
                self.generator.addExpression(newTemp,tempPos,'','') #ASIGNO AL VALOR DE RETORNO
                self.generator.addGoto(labelEnd) #FINALIZO LA EJECUCION SIN ERRORES
                
            #MIENTRAS NO SEA EL ULTIMO INDICE SIGUE EL "BUCLE"
            else:
                labelTrue = self.generator.newLabel()
                jumpLabel = self.generator.newLabel()
                self.generator.addIf(index.value,tempSize,'<=',labelTrue)
                self.generator.addGoto(labelOutRange)
                self.generator.addLabel(labelTrue)

                tempAux = self.generator.newTemp()
                self.generator.addExpression(tempAux,index.value,'2','*') #OBTENGO LA POSICION REAL
                self.generator.addExpression(tempPos,tempPos,tempAux,'+')
                self.generator.addGetHeap(tempType,tempPos)
                labelContinue = self.generator.newLabel()
                self.generator.addIf(tempType,tempMarca,'==',labelContinue)
                self.generator.addGoto(labelNotArray)

                self.generator.addLabel(labelContinue)
                self.generator.addExpression(tempMove,tempPos,'1','+')
                self.generator.addGetHeap(tempPos,tempMove)
                self.generator.addGetHeap(tempType,tempPos)
                self.generator.addExpression(tempMove,tempPos,'1','+')
                self.generator.addGetHeap(tempSize,tempMove)
                self.generator.addGetHeap(tempSize,tempSize,'2','/')
                self.generator.addGoto(jumpLabel) #SALTA DEL ERROR 

                #------MARCA QUE NO ES UN ARRAY------
                self.generator.addLabel(labelNotArray)
                self.generator.addPrintf('c',str(ord('N')))
                self.generator.addPrintf('c',str(ord('I')))
                self.generator.addPrintf('c',str(ord('A')))
                self.generator.addGoto(labelEnd)

                self.generator.addLabel(jumpLabel)
        
        self.generator.addLabel(labelOutRange)
        self.generator.addPrintf('c',str(ord('O')))
        self.generator.addPrintf('c',str(ord('R')))
        self.generator.addGoto(labelEnd)

        self.generator.addLabel(labelEnd) #FIN DE LAS INSTRUCCIONES
        
        return newValue



