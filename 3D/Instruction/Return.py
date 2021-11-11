from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class Return(Instruction):

    def __init__(self, expression:Expression) -> None:
        super().__init__()
        self.expression = expression

    def compile(self, environment:Environment) -> Value:

        self.expression.generator = self.generator
        #COMPILA EL VALOR A ASIGNAR EN LA VARIABLE
        newValue: Value = self.expression.compile(environment)

        #BUSCA SI ESTA DENTRO DE UNA FUNCION
        isFunc = environment.fatherIsFunction()

        #GUARDA EL VALOR DEL RETURN EN LA PRIMERA POSICION DEL ENTORNO SIMULADO DE LA FUNCION
        tempPos = self.generator.newTemp()
        #self.generator.addExpression(tempPos,'P',str(environment.size),'-')
        self.generator.addSetStack('P',newValue.getValue())


