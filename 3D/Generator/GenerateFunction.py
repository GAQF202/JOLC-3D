class GenerateFunction:

    def __init__(self) -> None:
        self.nameFunc = ''
        self.temporal = 0
        self.label = 0
        self.code = []
        #self.functions = []
        self.tempList = []
    
    #OBTENER LOS TEMPORALES USADOS
    def getUsedTemps(self) -> str:
        return ",".join(self.tempList)

    #OBTENER EL CODIGO GENERADO
    def getCode(self) -> str:
        tempCode = ""
        #tempCode += "func " + self.nameFunc + "(){\n"
        tempCode = tempCode + "\n".join(self.code)
        #tempCode += "\n}"

        return tempCode
    

    #GENERAR UN NUEVO TEMPORAL
    def newTemp(self) -> str:
        temp = "t" + str(self.temporal)
        self.temporal = self.temporal + 1

        #LO GUARDAMOS PARA DECLARARLO
        self.tempList.append(temp)
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
    
    #CREA UNA FUNCION NUEVA SIN CERRARLA
    def addFunction(self, nameFunc:str):
        self.code.append("func " + nameFunc +"(){") 

    #CIERRA CUALQUIER BLOQUE DE CODIGO COMO IF, FUNCTION, FOR, ETC...
    def addCloseBlock(self):
        self.code.append("}")
    
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

     