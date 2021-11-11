from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class VariableCall(Expression):

    def __init__(self, id:str) -> None:
        super().__init__()
        self.id = id

    def compile(self, environment: Environment) -> Value:
        
        retSym:Symbol = environment.getVariable(self.id)
        newTemp = self.generator.newTemp()

        #VALOR DE RETORNO
        newValue = Value(newTemp,True,retSym.type)

        #CREO EL TEMPORAL PARA OBTENER LA POSICION EXACTA DE LA VARIABLE EN EL ENTORNO
        tempPos = self.generator.newTemp()
        self.generator.addComment('Se obtiene la posicion exacta de la variable en el entorno')
        self.generator.addExpression(tempPos,'P',str(retSym.position),'+')
        self.generator.addGetStack(newTemp,tempPos)
        #self.generator.addGetStack(newTemp,str(retSym.position))

        newValue.arrayValues = retSym.arrayValues #PASO DE LOS VALORES POR SI ES UN ARREGLO
        newValue.typeArray = retSym.typeArray

        if(retSym.type != typeExpression.BOOL):
            return newValue
        else:
            return newValue
            '''val = Value("",False,typeExpression.BOOL)

            if(self.trueLabel == ""):
                self.trueLabel = self.generator.newLabel()
                
            if(self.falseLabel == ""):
                self.falseLabel = self.generator.newLabel()

            self.generator.addIf(newTemp,"1","==",self.trueLabel)
            self.generator.addGoto(self.falseLabel)

            val.trueLabel = self.trueLabel
            val.falseLabel = self.falseLabel

            return val'''