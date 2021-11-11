from Generator.Headers import nativeFunctions
from Generator.Headers import useMath
from Generator.GenerateFunction import GenerateFunction

class Generator:

    def __init__(self) -> None:
        self.generator = None
        self.temporal = 0
        self.label = 0
        self.code = []
        self.functions = GenerateFunction()
        self.tempList = []
        self.libraries = []
    
    #OBTENER LOS TEMPORALES USADOS
    def getUsedTemps(self) -> str:
        return ",".join(self.tempList)

    #OBTENER EL CODIGO GENERADO
    def getCode(self) -> str:
        tempCode = "package main \n"
        if useMath.useMath:
            self.libraries.append('\"math\"')
        tempCode += '''import (
            \"fmt\"
            ''' + "\n".join(self.libraries) +  '''
        )\n'''
        tempCode = tempCode + "var HEAP[1000000] float64;\n"
        tempCode = tempCode + "var STACK[780000] float64;\n"
        tempCode = tempCode + "var P float64;\n"
        tempCode = tempCode + "var H float64;\n"

        #AGREGO LAS FUNCIONES NATIVAS EN CODIGO INTERMEDIO PARA ARREGLOS DE TODOS LOS TIPOS
        self.Integer_array()
        self.Float_array()
        self.Boolean_array()
        self.String_array()
        self.Print_string()
        self.Print_integer()
        self.Print_float()
        self.Print_bool()

        if(len(self.functions.tempList) > 0):
            tempCode += "var " + self.functions.getUsedTemps() + " float64;" + "\n\n"
        tempCode += nativeFunctions
        
        tempCode += self.functions.getCode() + "\n\n"
        tempCode += "func main(){\n"
        tempCode = tempCode + "\n".join(self.code)
        tempCode += "\n}"
        #+ self.getUsedTemps() +","+
        return tempCode
    
    def addLibraries(self,library):
        self.libraries.append(library)

    #GENERAR UN NUEVO TEMPORAL
    def newTemp(self) -> str:
        temp = "t" + str(self.functions.temporal)
        self.functions.temporal = self.functions.temporal + 1

        #LO GUARDAMOS PARA DECLARARLO
        self.functions.tempList.append(temp)
        return temp
    
    #GENERADOR DE LABEL
    def newLabel(self) -> str:
        temp = self.label
        self.label = self.label + 1
        return "L" + str(temp)
    
    #AÑADE LABEL AL CODIGO
    def addLabel(self, label:str):
        self.code.append(label + ":")
    
    #CREA UNA NUEVA OPERACION CON DOS OPERADORES 
    def addExpression(self, target:str, left:str, right:str, operator:str):
        self.code.append(target + " = " + left + " " + operator + " " + right + ";")
    
    #ANADE UN PRINTF
    def addPrintf(self, typePrint:str, value:str):
        self.code.append("fmt.Printf(\"%" + typePrint + "\"," + value + ");")
    
    #SALTO DE LINEA
    def addNewLine(self):
        self.code.append("fmt.Printf(\"%c\",10);")

    #ANIADE UN IF
    def addIf(self, left: str, right: str, operator:str, label:str):
        self.code.append("if(" + left + " " + operator + " " + right + ") { goto " + label + " ;} ")
    
    #ANIADE UN SALTO DE ETIQUETA
    def addGoto(self, label:str):
        self.code.append("goto " + label + ";")
    
    #AGREGA AL CODIGO UNA LLAMADA A UNA FUNCION NATIVA DEL CODIGO
    def addCallFunc(self, function):
        self.code.append(function + "();")
    
    #AGREGA UNA LLAMADA AL METODO Mod DE LA LIBRERIA Math
    def addModule(self, target:str, expLeft:str, expRight:str):
        self.code.append(target + " = " + "math.Mod("+ expLeft + "," + expRight + ");")

    #SE MUEVE HACIA LA POSICION SIGUIENTE DEL HEAP
    def addNextHeap(self):
        self.code.append("H = H + 1;")
    
    #SE MUEVE HACIA LA POSICION SIGUIENTE DEL STACK
    def addNextStack(self, index:str):
        self.code.append("P = P + " + index + ";")
    
    #SE MUEVE HACIA LA POSICION ANTERIOR DEL STACK
    def addBackStack(self, index:str):
        self.code.append("P = P - " + index + ";")
    
    #OBTIENE EL VALOR EN CIERTA POSICION DEL HEAP
    def addGetHeap(self, target:str, index:str):
        self.code.append(target + " = HEAP[int(" + index + ")];")
    
    #INSERTA VALOR EN EL HEAP
    def addSetHeap(self, index:str, value:str):
        self.code.append("HEAP[int(" + index +")] = " + value + ";")

    #OBTIENE EL VALOR DEL STACK EN CIERTA POSICION
    def addGetStack(self, target:str, index:str):
        self.code.append(target + " = STACK [ int(" + index + ")];")
    
    def addSetStack(self, index:str, value:str):
        self.code.append("STACK[int(" + index + ")] = " + value + ";")

    def addComment(self, comment:str):
        self.code.append("//" + comment)
    
    #AGREGA UN SALTO DE LINEA AL C3D    
    def addJumpLine(self):
        self.code.append("\n")
    

    #FUNCION EN 3D PARA PRINTIAR ARREGLOS DE ENTEROS
    def Integer_array(self):

        self.functions.addFunction("jolc_print_array_integer")

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
        self.functions.addCallFunc('jolc_print_array_integer')
        self.functions.addExpression('P','P','3','-') #REGRESO AL ENTORNO

        #---------IMPRESION DE COMA----------
        printComa2 = self.functions.newLabel()
        printComa3 = self.functions.newLabel()
        noPrintComa1 = self.functions.newLabel()
        self.functions.addIf(tempPos,tempTop,'!=',printComa2)
        self.functions.addGoto(noPrintComa1)
        self.functions.addLabel(printComa2)
        self.functions.addIf(tempPos,tempInit,'!=',printComa3)
        self.functions.addGoto(noPrintComa1)
        self.functions.addLabel(printComa3)
        self.functions.addPrintf('c',"int(" + str(ord(',')) + ")")
        self.functions.addLabel(noPrintComa1)
        #--------------------------------------
        self.functions.addGoto(labelBucle)

        self.functions.addLabel(labelFalse3)
        #################################################
        self.functions.addExpression(tempMove,'P','1','+')
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addExpression(tempPos,tempPos,'1','+')
        self.functions.addSetStack(tempMove,tempPos)
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addGetHeap(tempValor,tempPos)
        #####################################################
        self.functions.addPrintf("d","int(" + tempValor + ")")

        #---------IMPRESION DE COMA----------
        printComa = self.functions.newLabel()
        printComa1 = self.functions.newLabel()
        noPrintComa = self.functions.newLabel()
        self.functions.addIf(tempPos,tempTop,'!=',printComa)
        self.functions.addGoto(noPrintComa)
        self.functions.addLabel(printComa)
        self.functions.addIf(tempPos,tempInit,'!=',printComa1)
        self.functions.addGoto(noPrintComa)
        self.functions.addLabel(printComa1)
        self.functions.addPrintf('c',"int(" + str(ord(',')) + ")")
        self.functions.addLabel(noPrintComa)
        #--------------------------------------

        self.functions.addGoto(labelBucle)

        self.functions.addLabel(labelFalse1)
        ################################
        self.functions.addExpression(tempMove,'P','1','+')
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addExpression(tempPos,tempPos,'1','+')
        self.functions.addSetStack(tempMove,tempPos)
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addGetHeap(tempValor,tempPos)
        ####################################
        self.functions.addPrintf("d","int(" + tempValor + ")")


        self.functions.addLabel(labelFalse2)
        self.functions.addPrintf('c',"int(" + str(ord(']')) + ")")
        self.functions.addCloseBlock()

    #FUNCION EN 3D PARA PRINTIAR ARREGLOS DE DECIMALES
    def Float_array(self):

        self.functions.addFunction("jolc_print_array_float")

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
        self.functions.addCallFunc('jolc_print_array_float')
        self.functions.addExpression('P','P','3','-') #REGRESO AL ENTORNO

        #---------IMPRESION DE COMA----------
        printComa2 = self.functions.newLabel()
        printComa3 = self.functions.newLabel()
        noPrintComa1 = self.functions.newLabel()
        self.functions.addIf(tempPos,tempTop,'!=',printComa2)
        self.functions.addGoto(noPrintComa1)
        self.functions.addLabel(printComa2)
        self.functions.addIf(tempPos,tempInit,'!=',printComa3)
        self.functions.addGoto(noPrintComa1)
        self.functions.addLabel(printComa3)
        self.functions.addPrintf('c',"int(" + str(ord(',')) + ")")
        self.functions.addLabel(noPrintComa1)
        #--------------------------------------
        self.functions.addGoto(labelBucle)

        self.functions.addLabel(labelFalse3)
        ################################
        self.functions.addExpression(tempMove,'P','1','+')
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addExpression(tempPos,tempPos,'1','+')
        self.functions.addSetStack(tempMove,tempPos)
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addGetHeap(tempValor,tempPos)
        ####################################
        self.functions.addPrintf("f","float64(" + tempValor + ")")

        #---------IMPRESION DE COMA----------
        printComa = self.functions.newLabel()
        printComa1 = self.functions.newLabel()
        noPrintComa = self.functions.newLabel()
        self.functions.addIf(tempPos,tempTop,'!=',printComa)
        self.functions.addGoto(noPrintComa)
        self.functions.addLabel(printComa)
        self.functions.addIf(tempPos,tempInit,'!=',printComa1)
        self.functions.addGoto(noPrintComa)
        self.functions.addLabel(printComa1)
        self.functions.addPrintf('c',"int(" + str(ord(',')) + ")")
        self.functions.addLabel(noPrintComa)
        #--------------------------------------

        self.functions.addGoto(labelBucle)

        self.functions.addLabel(labelFalse1)
        ################################
        self.functions.addExpression(tempMove,'P','1','+')
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addExpression(tempPos,tempPos,'1','+')
        self.functions.addSetStack(tempMove,tempPos)
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addGetHeap(tempValor,tempPos)
        ####################################
        self.functions.addPrintf("f","float64(" + tempValor + ")")


        self.functions.addLabel(labelFalse2)
        self.functions.addPrintf('c',"int(" + str(ord(']')) + ")")
        self.functions.addCloseBlock()

    #FUNCION EN 3D PARA PRINTIAR ARREGLOS DE DECIMALES
    def Boolean_array(self):

        self.functions.addFunction("jolc_print_array_bool")

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
        self.functions.addCallFunc('jolc_print_array_bool')
        self.functions.addExpression('P','P','3','-') #REGRESO AL ENTORNO

        #---------IMPRESION DE COMA----------
        printComa2 = self.functions.newLabel()
        printComa3 = self.functions.newLabel()
        noPrintComa1 = self.functions.newLabel()
        self.functions.addIf(tempPos,tempTop,'!=',printComa2)
        self.functions.addGoto(noPrintComa1)
        self.functions.addLabel(printComa2)
        self.functions.addIf(tempPos,tempInit,'!=',printComa3)
        self.functions.addGoto(noPrintComa1)
        self.functions.addLabel(printComa3)
        self.functions.addPrintf('c',"int(" + str(ord(',')) + ")")
        self.functions.addLabel(noPrintComa1)
        #--------------------------------------
        self.functions.addGoto(labelBucle)

        self.functions.addLabel(labelFalse3)
        ################################
        self.functions.addExpression(tempMove,'P','1','+')
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addExpression(tempPos,tempPos,'1','+')
        self.functions.addSetStack(tempMove,tempPos)
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addGetHeap(tempValor,tempPos)
        ####################################
        
        printTrueLabel1 = self.functions.newLabel()
        printFalseLabel1 = self.functions.newLabel()
        jumpLabel1 = self.functions.newLabel()
        self.functions.addIf(tempValor, '1', "==", printTrueLabel1)
        self.functions.addGoto(printFalseLabel1)
        self.functions.addLabel(printTrueLabel1)
        self.functions.addCallFunc("print_true")
        self.functions.addGoto(jumpLabel1)
        self.functions.addLabel(printFalseLabel1)
        self.functions.addCallFunc("print_false")
        self.functions.addLabel(jumpLabel1)

        #---------IMPRESION DE COMA----------
        printComa = self.functions.newLabel()
        printComa1 = self.functions.newLabel()
        noPrintComa = self.functions.newLabel()
        self.functions.addIf(tempPos,tempTop,'!=',printComa)
        self.functions.addGoto(noPrintComa)
        self.functions.addLabel(printComa)
        self.functions.addIf(tempPos,tempInit,'!=',printComa1)
        self.functions.addGoto(noPrintComa)
        self.functions.addLabel(printComa1)
        self.functions.addPrintf('c',"int(" + str(ord(',')) + ")")
        self.functions.addLabel(noPrintComa)
        #--------------------------------------

        self.functions.addGoto(labelBucle)

        self.functions.addLabel(labelFalse1)

        ################################
        self.functions.addExpression(tempMove,'P','1','+')
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addExpression(tempPos,tempPos,'1','+')
        self.functions.addSetStack(tempMove,tempPos)
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addGetHeap(tempValor,tempPos)
        ####################################
        
        printTrueLabel = self.functions.newLabel()
        printFalseLabel = self.functions.newLabel()
        jumpLabel = self.functions.newLabel()
        self.functions.addIf(tempValor, '1', "==", printTrueLabel)
        self.functions.addGoto(printFalseLabel)
        self.functions.addLabel(printTrueLabel)
        self.functions.addCallFunc("print_true")
        self.functions.addGoto(jumpLabel)
        self.functions.addLabel(printFalseLabel)
        self.functions.addCallFunc("print_false")
        self.functions.addLabel(jumpLabel)


        self.functions.addLabel(labelFalse2)
        self.functions.addPrintf('c',"int(" + str(ord(']')) + ")")
        self.functions.addCloseBlock()

    #FUNCION EN 3D PARA PRINTIAR ARREGLOS DE STRINGS
    def String_array(self):

        self.functions.addFunction("jolc_print_array_string")

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
        self.functions.addCallFunc('jolc_print_array_string')
        self.functions.addExpression('P','P','3','-') #REGRESO AL ENTORNO

        #---------IMPRESION DE COMA----------
        printComa2 = self.functions.newLabel()
        printComa3 = self.functions.newLabel()
        noPrintComa1 = self.functions.newLabel()
        self.functions.addIf(tempPos,tempTop,'!=',printComa2)
        self.functions.addGoto(noPrintComa1)
        self.functions.addLabel(printComa2)
        self.functions.addIf(tempPos,tempInit,'!=',printComa3)
        self.functions.addGoto(noPrintComa1)
        self.functions.addLabel(printComa3)
        self.functions.addPrintf('c',"int(" + str(ord(',')) + ")")
        self.functions.addLabel(noPrintComa1)
        #--------------------------------------
        self.functions.addGoto(labelBucle)

        self.functions.addLabel(labelFalse3)
        ################################
        self.functions.addExpression(tempMove,'P','1','+')
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addExpression(tempPos,tempPos,'1','+')
        self.functions.addSetStack(tempMove,tempPos)
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addGetHeap(tempValor,tempPos)
        ####################################

        #----------IMPRESION DE CADENA---------
        newTemp0 = self.functions.newTemp()
        self.functions.addGetHeap(newTemp0, tempValor)
        top = self.functions.newTemp()
        self.functions.addExpression(top,tempValor,'1','+')
        cont = self.functions.newTemp()
        self.functions.addExpression(cont,newTemp0,tempValor,'+')

        newLabel0 = self.functions.newLabel()
        self.functions.addLabel(newLabel0)

        labelTrue0 = self.functions.newLabel()
        labelFalse0 = self.functions.newLabel()
        self.functions.addIf(top,cont,'<',labelTrue0)
        self.functions.addGoto(labelFalse0)
        self.functions.addLabel(labelTrue0)
        tempHeap = self.functions.newTemp()
        self.functions.addGetHeap(tempHeap,top)
        self.functions.addPrintf('c',"int(" + tempHeap + ")")
        self.functions.addExpression(top,top,'1','+')
        self.functions.addGoto(newLabel0)
        self.functions.addLabel(labelFalse0)
        #--------------------------------------

        #---------IMPRESION DE COMA----------
        printComa = self.functions.newLabel()
        printComa1 = self.functions.newLabel()
        noPrintComa = self.functions.newLabel()
        self.functions.addIf(tempPos,tempTop,'!=',printComa)
        self.functions.addGoto(noPrintComa)
        self.functions.addLabel(printComa)
        self.functions.addIf(tempPos,tempInit,'!=',printComa1)
        self.functions.addGoto(noPrintComa)
        self.functions.addLabel(printComa1)
        self.functions.addPrintf('c',"int(" + str(ord(',')) + ")")
        self.functions.addLabel(noPrintComa)
        #--------------------------------------

        self.functions.addGoto(labelBucle)

        self.functions.addLabel(labelFalse1)
        ################################
        self.functions.addExpression(tempMove,'P','1','+')
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addExpression(tempPos,tempPos,'1','+')
        self.functions.addSetStack(tempMove,tempPos)
        self.functions.addGetStack(tempPos,tempMove)
        self.functions.addGetHeap(tempValor,tempPos)
        ####################################

        #----------IMPRESION DE CADENA---------
        newTemp1 = self.functions.newTemp()
        self.functions.addGetHeap(newTemp1, tempValor)
        top0 = self.functions.newTemp()
        self.functions.addExpression(top0,tempValor,'1','+')
        cont0 = self.functions.newTemp()
        self.functions.addExpression(cont0,newTemp1,tempValor,'+')

        newLabel1 = self.functions.newLabel()
        self.functions.addLabel(newLabel1)

        labelTrue4 = self.functions.newLabel()
        labelFalse1 = self.functions.newLabel()
        self.functions.addIf(top0,cont0,'<',labelTrue4)
        self.functions.addGoto(labelFalse1)
        self.functions.addLabel(labelTrue4)
        tempHeap0 = self.functions.newTemp()
        self.functions.addGetHeap(tempHeap0,top0)
        self.functions.addPrintf('c',"int(" + tempHeap0 + ")")
        self.functions.addExpression(top0,top0,'1','+')
        self.functions.addGoto(newLabel1)
        self.functions.addLabel(labelFalse1)
        #--------------------------------------


        self.functions.addLabel(labelFalse2)
        self.functions.addPrintf('c',"int(" + str(ord(']')) + ")")
        self.functions.addCloseBlock()

    def Print_string(self):
        self.functions.addFunction("jolc_print_string")
        newTemp = self.functions.newTemp()
        tempValue = self.functions.newTemp()

        tempAccess = self.functions.newTemp()
        self.functions.addExpression(tempAccess,'P','0','+')
        self.functions.addGetStack(tempValue,tempAccess)

        self.functions.addGetHeap(newTemp, tempValue)
        top = self.functions.newTemp()
        self.functions.addExpression(top,tempValue,'1','+')
        cont = self.functions.newTemp()
        self.functions.addExpression(cont,newTemp,tempValue,'+')

        newLabel = self.functions.newLabel()
        self.functions.addLabel(newLabel)

        labelTrue = self.functions.newLabel()
        labelFalse = self.functions.newLabel()
        self.functions.addIf(top,cont,'<',labelTrue)
        self.functions.addGoto(labelFalse)
        self.functions.addLabel(labelTrue)
        tempHeap = self.functions.newTemp()
        self.functions.addExpression(top,top,'1','+')
        self.functions.addGetHeap(tempHeap,top)
        self.functions.addPrintf('c',"int(" + tempHeap + ")")
        self.functions.addGoto(newLabel)
        self.functions.addLabel(labelFalse)
        self.functions.addCloseBlock()

    def Print_integer(self):
        self.functions.addFunction("jolc_print_integer")
        newTemp = self.functions.newTemp()
        tempValue = self.functions.newTemp()

        tempAccess = self.functions.newTemp()
        self.functions.addExpression(tempAccess,'P','0','+')
        self.functions.addGetStack(tempValue,tempAccess)

        self.functions.addPrintf("d","int(" + tempValue+ ")")
        self.functions.addCloseBlock()
    
    def Print_float(self):
        self.functions.addFunction("jolc_print_float")
        newTemp = self.functions.newTemp()
        tempValue = self.functions.newTemp()

        tempAccess = self.functions.newTemp()
        self.functions.addExpression(tempAccess,'P','0','+')
        self.functions.addGetStack(tempValue,tempAccess)

        self.functions.addPrintf("f","float64(" + tempValue + ")")
        self.functions.addCloseBlock()
    
    
    def Print_bool(self):
        self.functions.addFunction("jolc_print_bool")
        newTemp = self.functions.newTemp()
        tempValue = self.functions.newTemp()

        tempAccess = self.functions.newTemp()
        self.functions.addExpression(tempAccess,'P','0','+')
        self.functions.addGetStack(tempValue,tempAccess)

        trueLabel = self.functions.newLabel()
        falseLabel = self.functions.newLabel()
        jumpLabel = self.functions.newLabel()
        self.functions.addIf(tempValue, '1', "==", trueLabel)
        self.functions.addGoto(falseLabel)
        self.functions.addLabel(trueLabel)
        self.functions.addCallFunc("print_true")
        self.functions.addGoto(jumpLabel)
        self.functions.addLabel(falseLabel)
        self.functions.addCallFunc("print_false")
        self.functions.addLabel(jumpLabel)
        self.functions.addCloseBlock()

    
