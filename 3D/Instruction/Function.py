from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class Function(Instruction):

    def __init__(self, id:str, parameters, type: typeExpression, block) -> None:
        super().__init__()
        self.id = id
        self.parameters = parameters
        self.type = type
        self.block = block
        self.environment = None #AQUI SE GUARDARA EL ENTORNO DE LA FUNCION

    def compile(self, environment:Environment) -> Value:
    #def compileFunc(self, environment:Environment) -> Value:
        #GUARDO LA FUNCION EN EL ENTORNO
        environment.saveFunction(self.id,self)

        newEnv = Environment(environment)
        #POSIBLEEEEEEEEEEEEEEE CAMBIOOOOOOOOOOOO
        newEnv.size = 0

        #EL PRIMER VALOR QUE LE PASO ES UN RETURN SIMULADO SOLO PARA QUE RESERVE EL ESPACIO
        #EN EL STACK
        newEnv.saveVariable('return','',[],'','','')

        #POSIBLE CAMBIO
        self.environment = newEnv
        #CREA LA FUNCION EN EL GENERADOR DE FUNCIONES DEL GENERADOR
        self.generator.functions.addFunction(self.id)

        #SE GUARDAN LOS PARAMETROS EN EL ENTORNO
        for parameter in self.parameters:

            #EL GENERADOR DE LOS PARAMETROS ES EL GENERADOR DE FUNCIONES
            parameter.generator = self.generator.functions
            parameter.compile(newEnv)

        #EJECUTA EL BLOQUE DE CODIGO DE LA FUNCION
        for ins in self.block:
            if ins != None:
                ins.generator = self.generator.functions
                ins.compile(newEnv)
        
        #LE PASO EL ENTORNO A LA FUNCION
        self.environment = newEnv

        self.generator.functions.addCloseBlock()
        self.generator.functions.addJumpLine()