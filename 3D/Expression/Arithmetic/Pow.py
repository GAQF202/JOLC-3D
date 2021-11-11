from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class Pow(Expression):

    def __init__(self, left: Expression, right: Expression):
        super().__init__()
        self.leftExpression = left
        self.rightExpression = right

    def compile(self, environment: Environment) -> Value:
        self.leftExpression.generator = self.generator
        self.rightExpression.generator = self.generator

        leftValue : Value = self.leftExpression.compile(environment)
        rightValue : Value = self.rightExpression.compile(environment)
        #TEMPORAL PARA EL VALOR RESULTANTE
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
                self.generator.addExpression(newTemp,leftValue.getValue(),'0',"+")
                contTemp = self.generator.newTemp()
                self.generator.addExpression(contTemp,'1','0',"+")
                ifLabel = self.generator.newLabel()
                self.generator.addLabel(ifLabel)
                trueLabel = self.generator.newLabel()
                falseLabel = self.generator.newLabel()
                self.generator.addIf(contTemp,rightValue.value,'<',trueLabel)
                self.generator.addGoto(falseLabel)
                self.generator.addLabel(trueLabel)
                self.generator.addExpression(newTemp,newTemp,leftValue.value,'*')
                self.generator.addExpression(contTemp,contTemp,'1','+')
                self.generator.addGoto(ifLabel)
                self.generator.addLabel(falseLabel)
                return Value(newTemp,True,rightValue.type)
            else:
                print("Error en suma")
                return Value("0",False,rightValue.type)

        elif(leftValue.type == typeExpression.FLOAT):
            if(rightValue.type == typeExpression.INTEGER or rightValue.type == typeExpression.FLOAT):
                self.generator.addExpression(newTemp,leftValue.getValue(),'0',"+")
                contTemp = self.generator.newTemp()
                self.generator.addExpression(contTemp,'1','0',"+")
                ifLabel = self.generator.newLabel()
                self.generator.addLabel(ifLabel)
                trueLabel = self.generator.newLabel()
                falseLabel = self.generator.newLabel()
                self.generator.addIf(contTemp,rightValue.value,'<',trueLabel)
                self.generator.addGoto(falseLabel)
                self.generator.addLabel(trueLabel)
                self.generator.addExpression(newTemp,newTemp,leftValue.value,'*')
                self.generator.addExpression(contTemp,contTemp,'1','+')
                self.generator.addGoto(ifLabel)
                self.generator.addLabel(falseLabel)
                return Value(newTemp,True,rightValue.FLOAT)
            else:
                print("Error en suma")
                return Value("0",False,typeExpression.INTEGER)

        elif(leftValue.type == typeExpression.CADENA):
            if(rightValue.type == typeExpression.INTEGER):
                self.generator.addComment("INICIA ELEVACION DE CADENA")

                functionFound = environment.getFunction("string_elevation")
                
                envTemp1 = self.generator.newTemp() #TEMPORAL PARA SIMULAR CAMBIO DE ENTORNO
                posTemp1 = self.generator.newTemp() #TEMPORAL PARA SIMULAR EL CAMBIO DE POSICION EN EL ENTORNO
                self.generator.addExpression(envTemp1,'P',str(environment.size),'+')
                self.generator.addExpression(posTemp1,envTemp1,str(0),'+')
                self.generator.addSetStack(posTemp1,leftValue.value)

                envTemp2 = self.generator.newTemp() #TEMPORAL PARA SIMULAR CAMBIO DE ENTORNO
                posTemp2 = self.generator.newTemp() #TEMPORAL PARA SIMULAR EL CAMBIO DE POSICION EN EL ENTORNO
                self.generator.addExpression(envTemp2,'P',str(environment.size),'+')
                self.generator.addExpression(posTemp2,envTemp2,str(1),'+')
                self.generator.addSetStack(posTemp2,rightValue.value)

                #LLAMADA A LA FUNCION NATIVA DE ELEVAR
                self.generator.addNextStack(str(environment.size))
                self.generator.addCallFunc("string_elevation")
                self.generator.addBackStack(str(environment.size))

                
                retSym:Symbol = functionFound.environment.getVariable("return")
                retTemp = self.generator.newTemp()
                #CREO EL TEMPORAL PARA OBTENER LA POSICION EXACTA DE LA VARIABLE EN EL ENTORNO
                tempPos = self.generator.newTemp()
                self.generator.addComment('Se obtiene la posicion exacta de la variable en el entorno')
                self.generator.addExpression(tempPos,str(environment.size),str(retSym.position),'+')
                self.generator.addGetStack(retTemp,tempPos)
                if(retSym.type != typeExpression.BOOL):
                    return Value(retTemp,True,typeExpression.CADENA)
                else:
                    return Value(retTemp,True,typeExpression.CADENA)

                self.generator.addComment("TERMINA ELEVACION DE CADENA")

                #return Value(newTemp,True,typeExpression.CADENA)

        else:
            print("Error los tipos no se pueden sumar")


