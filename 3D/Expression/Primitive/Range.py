from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class Range(Expression):

    def __init__(self, leftValue:Expression, rightValue:Expression) -> None:
        super().__init__()
        self.leftValue = leftValue
        self.rightValue = rightValue

    def compile(self, environment: Environment) -> Value:
        self.leftValue.generator = self.generator
        self.rightValue.generator = self.generator

        init = self.leftValue.compile(environment)
        final = self.rightValue.compile(environment)

        
        if(init.type == typeExpression.INTEGER and final.type == typeExpression.INTEGER):
            return init, final

        print("No se reconoce el tipo")
        return Value("0",False,typeExpression.INTEGER)