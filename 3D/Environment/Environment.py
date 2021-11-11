from Enum_types.typeExpression import typeExpression
from Environment.Symbol import Symbol
# Reports.TS import setGlobalTS

class Environment:

    def __init__(self, father):
        #ATRIBUTO PARA SABER EL NOMBRE DEL ENTORNO
        self.name = ""
        #Usamos un diccionario para nuestra tabla de simbolos, guardara el id como clave y como cuerpo un simbolo
        self.variable = {}
        self.functions = {}
        self.structs = {}
        #ENTORNO PADRE
        self.father = father
        self.isLoopExpression = False
        #ATRIBUTO PARA SABER SI ES UNA FUNCION
        self.isFunction = False

        #SABER EL TAMAÑO DEL ENTORNO
        self.size = 0
        if(father != None):
            self.size = father.size

    
    def saveVariable(self, id: str, type: typeExpression, arrayValues, typeArray, line, column):
        #SI LA VARIABLE YA EXISTE
        if (self.variable.get(id) != None ):#and  not self.isLoopExpression):
            print("La variable " + id + " ya existe")
            return
        tempVar = Symbol(type,id,line,column,"",self.size)
        #SI ES UN ARRAY LE MANDO LOS VALORES RESUELTOS 
        tempVar.arrayValues = arrayValues
        tempVar.typeArray = typeArray
        #---------------------------------------------
        self.size = self.size + 1
        #print(self.size,self,id)
        self.variable[id] = tempVar
        return tempVar
        #setGlobalTS(id,getOutType(type),self.name,line,column)
    
    def saveStruct(self,id:str,struct):
        #VERIFICA QUE EL NOMBRE DEL STRUCT NO EXISTA ENTRE LAS VARIABLES DECLARADAS
        if (self.variable.get(id) != None):
            print("La variable " + id + " ya existe")
            return
        self.structs[id] = struct
        

    #METODO PARA BUSCAR VARIABLES EN TODOS LOS ENTORNOS PADRES
    def getVariable(self, id: str):
        tempEnv = self
        while(tempEnv != None):
            if(tempEnv.variable.get(id) != None):
                return tempEnv.variable.get(id)
            tempEnv = tempEnv.father

    #METODO PARA BUSCAR LOS STRUCT
    def getStruct(self, id:str):
        tempEnv = self
        #BUSCA EN TODOS LOS PADRES HASTA LLEGAR AL ENTORNO GLOBAL
        while(tempEnv != None):
            if tempEnv.father == None:
                if tempEnv.structs.get(id) != None:
                    return tempEnv.structs.get(id)
                else:
                    print("El Struct no existe")
                    return
            tempEnv = tempEnv.father
    
    #METODO PARA BUSCAR VARIABLES SOLO EN EL ENTORNO GLOBAL
    def getGlobal(self, id : str):
        tempEnv = self
        #SE RECORREN LOS PADRES
        while(tempEnv != None):
            #SI EL PADRE DEL ENTORNO ACTUAL ES NULO ENTONCES ES EL ENTORNO GLOBAL   
            if tempEnv.father == None:
                #BUSCA LA VARIABLE Y SI LA ENCUENTRA LA RETORNA
                if tempEnv.variable.get(id) != None :
                    return tempEnv.variable.get(id)

            tempEnv = tempEnv.father
    
    #METODO PARA SABER SI ES FUNCION ALGUNO DE LOS PADRES 
    def fatherIsFunction(self):
        #BUSCA EN TODOS LOS PADRES, SI ALGUNO ES FUNCION RETORNA TRUE
        isFunc = False
        tempEnv = self
        while(tempEnv!=None):
            if tempEnv.isFunction:
                isFunc = True
            tempEnv = tempEnv.father
        return isFunc

    #METODO PARA SABER SI ESTA DENTRO DE UN CICLO
    def fatherIsLoop(self):
        isOnLoop = False
        tempEnv = self
        while(tempEnv!=None):
            if tempEnv.isLoopExpression:
                isOnLoop = True
            tempEnv = tempEnv.father
        return isOnLoop

    #METODO PARA GUARDAR FUNCIONES EN EL ENTORNO
    def saveFunction(self, id: str, function):
        if (self.functions.get(id) != None):
            print("Error: la función ya existe")
            return
        self.functions[id] = function
    

    #METODO PARA BUSCAR FUNCIONES EN EL ENTORNO
    def getFunction(self, id : str):
        tempEnv = self
        while(tempEnv != None):
            if(tempEnv.functions.get(id) != None):
                return tempEnv.functions.get(id)
            tempEnv = tempEnv.father
        print("Error: la funcion " + id + " no existe")


    #METODO PARA ACTUALIZAR VALORES POR REFERENCIA A VARIABLES GLOBALES
    def upgradeVariables(self, id : str, value: Symbol):
        tempEnv = self 
        while(tempEnv != None):
            if(tempEnv.variable.get(id) != None):
                tempVar : Symbol = tempEnv.variable.get(id)
                #SI EL VALOR QUE SE PASA COMO PARAMETRO NO ES DE TIPO STRUCT SE TRABAJA CON LOS TIPOS PRIMITIVOS
                if(value.getType() != typeExpression.STRUCT):
                    #SI EL TIPO ES EL MISMO O EL TIPO DEL QUE SE ESTA CAMBIANDO ES NOTHING SE PUEDE CAMBIAR POR AHORA...
                    #if(tempVar.getType() == value.getType() or tempVar.getType() == typeExpression.NULO):
                        #print(id)
                    tempVar.value = value
                    #print(tempEnv.variable[id].value.value)
                    tempEnv.variable[id] = tempVar#.getValue()
                    return
                    #else:
                     #   print("Error la variable no puede ser cambiada de tipo")
                #SI EL VALOR QUE SE PASA COMO PARAMETRO SI ES STRUCT SE VERIFICA QUE SEA DEL MISMO TIPO
                elif(value.getType() == typeExpression.STRUCT):
                    if( tempVar.getType() == value.getValue().id or tempVar.getType() == typeExpression.NULO ):
                        tempVar.type = value.getType()
                        tempVar.value = value
                        tempEnv.variable[id] = tempVar.getValue()
                        return
            tempEnv = tempEnv.father
        print("Error la variable no existe")
        return None

    #METODO PARA ACTUALIZAR VALORES POR REFERENCIA PARA VARIABLES LOCALES 
    def upgradeVariableLocal(self,id:str, value:Symbol):
        tempEnv = self 
        while(tempEnv != None):
            if(tempEnv.father != None):
                if(tempEnv.variable.get(id) != None):
                    tempVar : Symbol = tempEnv.variable.get(id)
                    #hola = Symbol(tempVar.type,"",tempVar.value,"","","")
                    #SI EL TIPO ES EL MISMO O EL TIPO DEL QUE SE ESTA CAMBIANDO ES NOTHING SE PUEDE CAMBIAR POR AHORA...
                    if(tempVar.getType() == value.getType() or tempVar.getType() == typeExpression.NULO):
                        #tempVar.value = value
                        #POSIIIIBLE CAMBIOOO
                        tempEnv.variable[id] = value
                        return
                    else:
                        print("Error la variable no puede ser cambiada de tipo")
                tempEnv = tempEnv.father
        print("Error la variable no existe ")
        return None  
    
    def upgradeGlobal(self,id:str, value:Symbol):
        tempEnv = self
        #SE RECORREN LOS PADRES
        while(tempEnv != None):
            #SI EL PADRE DEL ENTORNO ACTUAL ES NULO ENTONCES ES EL ENTORNO GLOBAL   
            if tempEnv.father == None:
                #BUSCA LA VARIABLE Y SI LA ENCUENTRA LA RETORNA
                if tempEnv.variable.get(id) != None :
                    tempVar : Symbol = tempEnv.variable.get(id)
                    #SI EL TIPO ES EL MISMO O EL TIPO DEL QUE SE ESTA CAMBIANDO ES NOTHING SE PUEDE CAMBIAR POR AHORA...
                    if(tempVar.getType() == value.getType() or tempVar.getType() == typeExpression.NULO):
                        tempVar.value = value
                        tempEnv.variable[id] = tempVar.getValue()
                        return
                    else:
                        print("Error la variable no puede ser cambiada de tipo")

            tempEnv = tempEnv.father

    def upgradeArray(self, id : str, value : Symbol):
        tempEnv = self 
        while(tempEnv != None):
            if(tempEnv.variable.get(id) != None):
                tempEnv.variable[id].value.append(value)
                return
            tempEnv = tempEnv.father
        print("Error la variable no existe")
        return None
    
    def upgradeArrayPos(self, id:str, positions, value : Symbol):
        tempEnv = self 
        while(tempEnv != None):
            #SE VERIFICA QUE EXISTA LA VARIABLE
            if(tempEnv.variable.get(id) != None):
                #VALOR TEMPORAL DEL ARRAY A MODIFICAR
                #tempArray = tempEnv.variable[id].value[int(positions.pop(0))]
                if len(positions) == 1:
                    tempArray = tempEnv.variable[id].value[int(positions.pop(0))]
                    tempArray.value = value.getValue()
                    return
                else:
                    #MIENTRAS NO SE VACIE EL ARRAY DE POSICIONES SIGUE NAVEGANDO ENTRE DIMENSIONES
                    tempArray = tempEnv.variable[id].value[int(positions.pop(0))]
                    while(len(positions)!=0):
                        tempArray = tempArray.value[int(positions.pop(0))]
                    tempArray.value = value.getValue()
                    #SI ENCUENTRA LA VARIABLE INDICADA RETORNA
                    return
            #SIGUE ACCEDIENDO A LOS PADRES MIENTRAS NO ENCUENTRE LA VARIABLE INDICADA
            tempEnv = tempEnv.father
        print("Error la variable no existe")
        return None
    
    def removeOfArray(self, id : str):
        tempEnv = self 
        while(tempEnv != None):
            if(tempEnv.variable.get(id) != None):
                val = self.variable[id].value.pop()
                return Symbol(val.getType(),"",val.getValue(),"","","")
            tempEnv = tempEnv.father
        print("Error la variable no existe")
        return None

    #METODO PARA GUARDAR TODOS LOS SIMBOLOS EN LA TSGLOBAL
    def loadSymbols(self):
        self.variable
        #print(self.functions)
        #print(self.structs)

#FUNCION PARA BUSCAR EL TIPO Y RETORNARLO EN FORMA DE STRING
def getOutType(myType:typeExpression):
    if myType == typeExpression.CADENA:
        return "String"
    elif myType == typeExpression.INTEGER:
        return "Int64"
    elif myType == typeExpression.FLOAT:
        return "Float64"
    elif myType == typeExpression.CHARACTER:
        return "Char"
    elif myType == typeExpression.BOOL:
        return "Bool"
    elif myType == typeExpression.NULO:
        return "Nulo"
    elif myType == typeExpression.ARRAY:
        return "Array"
    elif myType == typeExpression.RANGE:
        return "Range"
    elif myType == typeExpression.STRUCT:
        return "Struct"
    else:
        return myType