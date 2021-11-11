from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class Not(Expression):

    def __init__(self, expression:Expression) -> None:
        super().__init__()
        self.expression = expression
    
    def compile(self, environment:Environment) -> Value:
        self.expression.generator = self.generator

        expression: Value = self.expression.compile(environment)

        #TEMPORAL PARA GUARDAR EL RESULTADO
        newTemp = self.generator.newTemp()
        
        #SI ES UN ARRAY ME MUEVO AL VALOR REAL Y LE PASO EL TIPO DEL ARRAY AL VALOR
        if(expression.type == typeExpression.ARRAY):
            tempAccess = self.generator.newTemp()
            self.generator.addExpression(tempAccess,expression.value,'1','+' )
            self.generator.addGetHeap(expression.value,tempAccess)
            expression = Value(expression.value,True,expression.typeArray)
        #-----------------------------------------------------------------------------

        if(expression.type == typeExpression.BOOL):
                
            newValue = Value(newTemp,True,typeExpression.BOOL)

            if(self.trueLabel == ""):
                self.trueLabel = self.generator.newLabel()
            
            if(self.falseLabel == ""):
                self.falseLabel = self.generator.newLabel()
            
            labelTrue = self.generator.newLabel()
            labelFalse = self.generator.newLabel()
            jumpLabel  = self.generator.newLabel()

            self.generator.addIf(expression.value,'1','==',labelTrue)
            self.generator.addGoto(labelFalse)
            self.generator.addLabel(labelTrue)
            self.generator.addExpression(newTemp,'0','','')
            self.generator.addGoto(jumpLabel)
            self.generator.addLabel(labelFalse)
            self.generator.addExpression(newTemp,'1','','')
            self.generator.addLabel(jumpLabel)

            return newValue