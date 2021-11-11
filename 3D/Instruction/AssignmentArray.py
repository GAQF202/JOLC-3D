from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class AssignmentArray(Instruction):

    def __init__(self, id:str, positions, expression:Expression, line, column) -> None:
        super().__init__()
        self.id = id
        self.positions = positions
        self.expression = expression
        self.line = line
        self.column = column

    def compile(self, environment:Environment) -> Value:

        self.expression.generator = self.generator #LE PASO EL GENERADOR
        expression = self.expression.compile(environment) #COMPILO LA EXPRESION
        arrayFound = environment.getVariable(self.id) #BUSCA LA VARIABLE EN EL ENTORNO

        labelNotArray = self.generator.newLabel() #ETIQUETA PARA QUE SALGA Y MARQUE EL ERROR QUE NO ES ARRAY
        labelOutRange = self.generator.newLabel() #ETIQUETA PARA QUE MARQUE EL ERROR FUERA DE RANGO
        labelEnd = self.generator.newLabel() #LABEL PARA SALIR DE LA INSTRUCCION

        tempPos = self.generator.newTemp() #PRIMERA POSICION EN EL HEAP
        tempSize = self.generator.newTemp() #TAMAÑO DEL ARREGLO GUARDADO EN EL HEAP
        tempType = self.generator.newTemp() #PARA GUARDAR EL TIPO DENTRO DEL CODIGO INTERMEDIO
        tempMove = self.generator.newTemp() #PARA MOVERME EN EL HEAP SIN AFECTAR LA POSICION ABSOLUTA

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

                    #SI VIENE UN ARRAY
                    if expression.type == typeExpression.ARRAY:
                        #OBTENGO EL TIPO DE LA EXPRESION SI ES UN ARREGLO
                        tempTypeExp = self.generator.newTemp()
                        self.generator.addGetHeap(tempTypeExp,expression.value)
                        self.generator.addSetHeap(tempPos,tempTypeExp)
                        self.generator.addSetHeap(tempMove,expression.value)
                    else: #CUALQUIER OTRO TIPO DE EXPRESION
                        tempMarcaNoArray = self.generator.newTemp()
                        self.generator.addExpression(tempMarcaNoArray,'0','0.0001','-')
                        self.generator.addSetHeap(tempPos,tempMarcaNoArray)
                        self.generator.addSetHeap(tempMove,expression.value) 

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

                #SI VIENE UN ARRAY
                if expression.type == typeExpression.ARRAY:
                    #OBTENGO EL TIPO DE LA EXPRESION SI ES UN ARREGLO
                    tempTypeExp = self.generator.newTemp()
                    self.generator.addGetHeap(tempTypeExp,expression.value)
                    self.generator.addSetHeap(tempPos,tempTypeExp)
                    self.generator.addSetHeap(tempMove,expression.value)
                else: #CUALQUIER OTRO TIPO DE EXPRESION
                    tempMarcaNoArray = self.generator.newTemp()
                    self.generator.addExpression(tempMarcaNoArray,'0','0.0001','-')
                    self.generator.addSetHeap(tempPos,tempMarcaNoArray)
                    self.generator.addSetHeap(tempMove,expression.value)
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



