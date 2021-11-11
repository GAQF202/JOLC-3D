from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class ForLoop(Instruction):

    def __init__(self, variable:str, expression:Expression, block, line, column) -> None:
        super().__init__()
        self.variable = variable
        self.expression = expression
        self.block = block
        self.line = line
        self.column = column

    def compile(self, environment:Environment) -> Value:
        self.expression.generator = self.generator

        expression = self.expression.compile(environment)

        #SI ES DE TIPO RANGE
        if(isinstance(expression,tuple)):
            #CREO EL TEMPORAL QUE IRA AUMENTANDO SEGUN EL RANGO 
            itTemp = self.generator.newTemp()
            self.generator.addExpression(itTemp,expression[0].value,'','')

            tempVar: Symbol = environment.saveVariable(self.variable,typeExpression.INTEGER,[],'','','')
            tempPos = self.generator.newTemp() #TEMPORAL PARA OBTENER LA POSICION EXACTA
            self.generator.addExpression(tempPos,'P',str(tempVar.position),'+')
            #SE HACE LA DECLARACION
            self.generator.addSetStack(tempPos,itTemp)

            #ETIQUETAS DE CONTROL
            initLabel = self.generator.newLabel()
            trueLabel = self.generator.newLabel()
            falseLabel = self.generator.newLabel()

            self.generator.addLabel(initLabel)
            self.generator.addIf(itTemp,expression[1].value,'<=',trueLabel)
            self.generator.addGoto(falseLabel)
            self.generator.addLabel(trueLabel)

            #EJECUTA EL CODIGO QUE VIENE DENTRO DEL FOR
            self.block.generator = self.generator
            self.block.compile(environment)


            self.generator.addExpression(itTemp,itTemp,'1','+')
            self.generator.addSetStack(tempPos,itTemp)
            self.generator.addGoto(initLabel)
            self.generator.addLabel(falseLabel)

        elif expression.type == typeExpression.CADENA:
            newTemp = self.generator.newTemp()
            self.generator.addGetHeap(newTemp, expression.value)
            top = self.generator.newTemp()

            self.generator.addExpression(top,expression.value,'1','+')
            cont = self.generator.newTemp()
            self.generator.addExpression(cont,newTemp,expression.value,'+')

            newLabel = self.generator.newLabel()
            self.generator.addLabel(newLabel)

            labelTrue = self.generator.newLabel()
            labelFalse = self.generator.newLabel()
            self.generator.addIf(top,cont,'<',labelTrue)
            self.generator.addGoto(labelFalse)
            self.generator.addLabel(labelTrue)
            tempHeap = self.generator.newTemp()
            self.generator.addGetHeap(tempHeap,top)

            #GUARDA EN EL HEAP LETRA POR LETRA Y DA COMO RESULTADO EL TEMPORAL CON SU POSICION
            tempChar = self.generator.newTemp()  
            self.generator.addExpression(tempChar,'H','0',"+")
            self.generator.addSetHeap("H",str(2))
            self.generator.addNextHeap()
            self.generator.addSetHeap("H",str(tempHeap))
            self.generator.addNextHeap()

            #GUARDA EN EL STACK LETRA POR LETRA
            tempVar: Symbol = environment.saveVariable(self.variable,typeExpression.CADENA,'','','','')
            tempPos = self.generator.newTemp() #TEMPORAL PARA OBTENER LA POSICION EXACTA
            self.generator.addExpression(tempPos,'P',str(tempVar.position),'+')
            #SE HACE LA DECLARACION
            self.generator.addSetStack(tempPos,tempChar)

            #EJECUTA EL CODIGO QUE VIENE DENTRO DEL CUERPO DEL FOR
            self.block.generator = self.generator
            self.block.compile(environment)

            #AUMENTO DEL TEMPORAL ITERABLE
            self.generator.addExpression(top,top,'1','+')
            self.generator.addGoto(newLabel)
            self.generator.addLabel(labelFalse)
            


