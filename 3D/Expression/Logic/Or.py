from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class Or(Expression):

    def __init__(self, left:Expression, right:Expression) -> None:
        super().__init__()
        self.leftExpression = left
        self.rightExpression = right
    
    def compile(self, environment:Environment) -> Value:
        self.leftExpression.generator = self.generator
        self.rightExpression.generator = self.generator

        leftValue: Value = self.leftExpression.compile(environment)
        rightValue: Value = self.rightExpression.compile(environment)

        #TEMPORAL PARA GUARDAR EL RESULTADO
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

        if(rightValue.type == typeExpression.BOOL):
            if(leftValue.type == typeExpression.BOOL):
                
                newValue = Value(newTemp,False,typeExpression.BOOL)

                if(self.trueLabel == ""):
                    self.trueLabel = self.generator.newLabel()
                
                if(self.falseLabel == ""):
                    self.falseLabel = self.generator.newLabel()
                
                labelTrue = self.generator.newLabel()
                labelFalse = self.generator.newLabel()
                jumpLabel = self.generator.newLabel()
                self.generator.addIf(leftValue.value,'1','==',labelTrue)
                self.generator.addGoto(labelFalse)
                self.generator.addLabel(labelTrue)
                self.generator.addExpression(newTemp,'1','','')
                self.generator.addGoto(jumpLabel)
                self.generator.addLabel(labelFalse)
                self.generator.addIf(rightValue.value,'1','==',labelTrue)
                self.generator.addExpression(newTemp,'0','','')
                self.generator.addLabel(jumpLabel)

                return newValue

                '''t2
                if (t0==0){goto L0}
                goto L1
                L0:
                t2 = 0
                goto L4
                L1:
                if (t1==0){goto L0}
                t2 = 1
                goto L4
                L4:'''