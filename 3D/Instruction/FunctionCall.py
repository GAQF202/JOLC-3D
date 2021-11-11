from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class FunctionCall(Instruction):

    def __init__(self, id:str, parametersCall, isExpression:bool) -> None:
        super().__init__()
        self.id = id
        self.parametersCall = parametersCall
        self.isExpression = isExpression
        self.type = type

    def compile(self, environment:Environment) -> Value:
        #BUSCA LA FUNCION EN EL ENTORNO
        functionFound = environment.getFunction(self.id)

        if(len(self.parametersCall)==len(functionFound.parameters)):
        #RESUELVO LAS EXPRESIONES DE LOS PARAMETROS LLAMADOS
            for i in range(len(self.parametersCall)):
                envTemp = self.generator.newTemp() #TEMPORAL PARA SIMULAR CAMBIO DE ENTORNO
                posTemp = self.generator.newTemp() #TEMPORAL PARA SIMULAR EL CAMBIO DE POSICION EN EL ENTORNO
                self.parametersCall[i].generator = self.generator
                value = self.parametersCall[i].compile(environment)
                self.generator.addExpression(envTemp,'P',str(environment.size),'+')
                self.generator.addExpression(posTemp,envTemp,str(i + 1),'+')
                self.generator.addSetStack(posTemp,value.value)

            #CAMBIO DE ENTORNO
            if not self.isExpression:
                self.generator.addNextStack(str(environment.size))
                self.generator.addCallFunc(self.id)
                self.generator.addBackStack(str(environment.size))

            #SI LA LLAMADA A LA FUNCION ES UNA EXPRESION RETORNA EL VALOR DEL RETURN
            elif self.isExpression :

                #CREO EL TEMPORAL PARA RETORNAR EL VALOR DE LA ULTIMA POSICION DEL STACK
                referenceTemp = self.generator.newTemp()

                #ALMACENA LA POSICION DEL RETURN DE LA FUNCION QUE LLAMA SUMANDO LA POSICION
                #ACTUAL EN EL STACK MAS LA POSICION DONDE SE ENCUENTRA EL RETURN
                positionTemp = self.generator.newTemp()
                self.generator.addExpression(positionTemp,'P','','')#str(functionFound.environment.size),'+')
                #OBTIENE EL VALOR DE DONDE SE ENCUENTRA EL RETURN DE LA FUNCION Y LO RETORNA
                self.generator.addGetStack(referenceTemp,positionTemp)

                
                #CAMBIO DE ENTORNO
                self.generator.addNextStack(str(environment.size))
                self.generator.addCallFunc(self.id)
                #REGRESO AL ENTORNO ANTERIOR DESPUES DE LA LLAMADA
                self.generator.addBackStack(str(environment.size))

                return Value(referenceTemp,True,typeExpression.INTEGER)
        else:
            print("Error en la llamada a la función no tiene la misma cantidad de parametros")
        '''
            t0 = STACK[P + function.env.size]
        '''