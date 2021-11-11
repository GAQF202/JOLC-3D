from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class Declaration(Instruction):

    def __init__(self, id:str, exp:Expression, type: typeExpression) -> None:
        super().__init__()
        self.id = id
        self.exp = exp
        self.type = type

    def compile(self, environment:Environment) -> Value:

        self.exp.generator = self.generator
        #COMPILA EL VALOR A ASIGNAR EN LA VARIABLE
        newValue: Value = self.exp.compile(environment)
        
        #BUSCA LA VARIABLE
        existVariable = environment.getVariable(self.id)
        #BUSCA SI ESTA DENTRO DE UNA FUNCION
        isFunc = environment.fatherIsFunction()

        #SI LA VARIABLE EXISTE SE ACTUALIZA 
        if existVariable:
            tempPosition = self.generator.newTemp()
            self.generator.addExpression(tempPosition,'P',str(existVariable.position),'+')
            self.generator.addSetStack(tempPosition,newValue.getValue())
            environment.upgradeVariables(self.id,newValue)
        
        else: #SI LA VARIABLE NO EXISTE SE CREA 
            
            if self.type == newValue.type or self.type == None:
                #SE DEFINE EL TIPO
                if(self.type != None):
                    resType = self.type
                else:
                    resType = newValue.type

                tempVar: Symbol = environment.saveVariable(self.id,resType,newValue.arrayValues,newValue.typeArray,'','')
                tempPosition = self.generator.newTemp()
                self.generator.addExpression(tempPosition,'P',str(tempVar.position),'+')
                
                #POSIBLE CAMBIOOOOOOO
                self.generator.addSetStack(tempPosition,newValue.getValue())
                #if(self.type != typeExpression.BOOL):
                #    self.generator.addSetStack(tempPosition,newValue.getValue())
                #else:
                #    self.generator.addSetStack(tempPosition,newValue.getValue())
            else:
                print("Error los tipos no coinciden")
            