def NativesIntermediatesFunctions(self):

        self.functions.addFunction("jolc_print_array")

        tempMove = self.functions.newTemp()
        tempPos = self.functions.newTemp()
        tempValor = self.functions.newTemp()
        tempMarca = self.functions.newTemp()

        self.functions.addExpression(tempMove,'P','0','+')
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addGetHeap(tempValor,tempPos)
        self.functions.addExpression(tempMarca,'0','0.0003','-')

        labelTrue1 = self.functions.newLabel() 
        labelFalse1 = self.functions.newLabel()
        self.functions.addIf(tempValor,tempMarca,'==',labelTrue1) #VERIFICO QUE SEA UN ARRAY
        self.functions.addGoto(labelFalse1)

        self.functions.addLabel(labelTrue1)
        tempInit = self.functions.newTemp()
        self.functions.addExpression(tempInit,tempPos,'1','+')
        self.functions.addExpression(tempMove,'P','1','+')
        self.functions.addSetStack(tempMove,tempInit)
        tempSize = self.functions.newTemp()
        self.functions.addGetHeap(tempSize,tempInit)
        tempTop = self.functions.newTemp()
        self.functions.addExpression(tempTop,tempSize,tempInit,'+')

        labelBucle = self.functions.newLabel()
        self.functions.addLabel(labelBucle)
        self.functions.addExpression(tempMove,'P','1','+')
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addExpression(tempPos,tempPos,'1','+') #AUMENTO EL CONTADOR
        self.functions.addSetStack(tempMove,tempPos)
        self.functions.addGetStack(tempPos,tempMove)

        labelTrue2 = self.functions.newLabel()
        labelFalse2 = self.functions.newLabel()
        self.functions.addIf(tempPos,tempTop,'<=',labelTrue2)
        self.functions.addGoto(labelFalse2)

        self.functions.addLabel(labelTrue2)
        self.functions.addGetHeap(tempValor,tempPos)

        labelTrue3 = self.functions.newLabel()
        labelFalse3 = self.functions.newLabel()
        self.functions.addIf(tempValor,tempMarca,'==',labelTrue3)
        self.functions.addGoto(labelFalse3)

        self.functions.addLabel(labelTrue3)
        self.functions.addExpression(tempMove,'P','1','+')
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addExpression(tempPos,tempPos,'1','+')
        self.functions.addSetStack(tempMove,tempPos)
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addGetHeap(tempValor,tempPos)

        self.functions.addExpression(tempMove,'P','2','+')
        tempPar = self.functions.newTemp()
        self.functions.addExpression(tempPar,tempMove,'0','+')
        self.functions.addSetStack(tempPar,tempValor)

        self.functions.addExpression('P','P','2','+') #CAMBIO DE ENTORNO
        self.functions.addCallFunc('jolc_print_array')
        self.functions.addExpression('P','P','2','-') #REGRESO AL ENTORNO
        self.functions.addGoto(labelBucle)

        self.functions.addLabel(labelFalse3)
        self.functions.addPrintf("f","float64(" + tempValor + ")")
        self.functions.addGoto(labelBucle)

        self.functions.addLabel(labelFalse1)
        self.functions.addPrintf("f","float64(" + tempValor + ")")


        self.functions.addLabel(labelFalse2)
        self.functions.addCloseBlock()





    def NativesIntermediatesFunctions(self):

        self.functions.addFunction("jolc_print_array")

        tempMove = self.functions.newTemp()
        tempPos = self.functions.newTemp()
        tempValor = self.functions.newTemp()
        tempMarca = self.functions.newTemp()

        newTemp = self.functions.newTemp() #--------------------------------

        self.functions.addExpression(tempMove,'P','0','+')
        self.functions.addGetStack(newTemp,tempMove)

        temporalNuevo = self.functions.newTemp()
        self.functions.addExpression(temporalNuevo,'P','2','+')
        self.functions.addSetStack(temporalNuevo,newTemp)
        
        self.functions.addGetHeap(tempValor,newTemp)
        self.functions.addExpression(tempMarca,'0','0.0003','-')

        labelTrue1 = self.functions.newLabel() 
        labelFalse1 = self.functions.newLabel()
        self.functions.addIf(tempValor,tempMarca,'==',labelTrue1) #VERIFICO QUE SEA UN ARRAY
        self.functions.addGoto(labelFalse1)

        self.functions.addLabel(labelTrue1)
        self.functions.addPrintf('c',"int(" + str(ord('[')) + ")")
        tempInit = self.functions.newTemp()

        self.functions.addExpression(temporalNuevo,'P','2','+')
        self.functions.addGetStack(newTemp,temporalNuevo)

        self.functions.addExpression(tempInit,newTemp,'1','+')
        self.functions.addExpression(tempMove,'P','1','+')
        self.functions.addSetStack(tempMove,tempInit)
        tempSize = self.functions.newTemp()
        self.functions.addGetHeap(tempSize,tempInit)
        tempTop = self.functions.newTemp()
        self.functions.addExpression(tempTop,tempSize,tempInit,'+')

        labelBucle = self.functions.newLabel()
        self.functions.addLabel(labelBucle)
        self.functions.addExpression(tempMove,'P','1','+')
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addExpression(tempPos,tempPos,'1','+') #AUMENTO EL CONTADOR
        self.functions.addSetStack(tempMove,tempPos)
        self.functions.addGetStack(tempPos,tempMove)

        self.functions.addExpression(temporalNuevo,'P','2','+')
        self.functions.addGetStack(newTemp,temporalNuevo)
        self.functions.addExpression(tempInit,newTemp,'1','+')
        self.functions.addGetHeap(tempSize,tempInit)
        self.functions.addExpression(tempTop,tempSize,tempInit,'+')

        labelTrue2 = self.functions.newLabel()
        labelFalse2 = self.functions.newLabel()
        self.functions.addIf(tempPos,tempTop,'<=',labelTrue2)
        self.functions.addGoto(labelFalse2)

        self.functions.addLabel(labelTrue2)
        self.functions.addGetHeap(tempValor,tempPos)

        labelTrue3 = self.functions.newLabel()
        labelFalse3 = self.functions.newLabel()
        self.functions.addIf(tempValor,tempMarca,'==',labelTrue3)
        self.functions.addGoto(labelFalse3)

        self.functions.addLabel(labelTrue3)
        self.functions.addExpression(tempMove,'P','1','+')
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addExpression(tempPos,tempPos,'1','+')
        self.functions.addSetStack(tempMove,tempPos)
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addGetHeap(tempValor,tempPos)

        self.functions.addExpression(tempMove,'P','3','+')
        tempPar = self.functions.newTemp()
        self.functions.addExpression(tempPar,tempMove,'0','+')
        self.functions.addSetStack(tempPar,tempValor)

        self.functions.addExpression('P','P','3','+') #CAMBIO DE ENTORNO
        self.functions.addCallFunc('jolc_print_array')
        self.functions.addExpression('P','P','3','-') #REGRESO AL ENTORNO
        self.functions.addGoto(labelBucle)

        self.functions.addLabel(labelFalse3)
        self.functions.addPrintf("f","float64(" + tempValor + ")")
        self.functions.addGoto(labelBucle)

        self.functions.addLabel(labelFalse1)
        self.functions.addPrintf("f","float64(" + tempValor + ")")


        self.functions.addLabel(labelFalse2)
        self.functions.addPrintf('c',"int(" + str(ord(']')) + ")")
        self.functions.addCloseBlock()