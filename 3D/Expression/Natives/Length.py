from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum_types.typeExpression import typeExpression

class Length(Expression):

    def __init__(self, expression:Expression, isId:bool, line, column) -> None:
        super().__init__()
        self.expression = expression
        self.isId = isId #PARA SABER SI BUSCAR EN EL HEAP O EN EL STACK
        self.line = line
        self.column = column

    def compile(self, environment: Environment) -> Value:
        #TEMPORAL DE RETORNO
        newTemp = self.generator.newTemp()
        expression = None
        if self.isId:
            tempPos = self.generator.newTemp() #TEMPORAL PARA GUARDAR LA POSICION DEL HEAP
            expression : Symbol = environment.getVariable(self.expression) #BUSCA LA VARIABLE
            self.generator.addGetStack(tempPos,str(expression.position)) #OBTIENE LA POSICION DEL STACK
            self.generator.addGetHeap(newTemp,tempPos) #OBTIENE EL TAMAÑO
        else:
            self.expression.generator = self.generator
            expression = self.expression.compile(environment) #RESUELVO LA EXPRESION
            self.generator.addGetHeap(newTemp,expression.value) #GUARDA EL TAMANIO EN EL TEMPORAL
        
        #VERIFICA LOS TIPOS
        if(expression.type == typeExpression.ARRAY):
            tempArray = self.generator.newTemp()
            tempAccess = self.generator.newTemp()

            if self.isId:
                self.generator.addExpression(tempAccess,str(expression.position),'1','+') #ACCEDO A LA POSICION DEL TAMANIO
            else:
                self.generator.addExpression(tempAccess,expression.value,'1','+') #ACCEDO A LA POSICION DEL TAMANIO

            self.generator.addGetHeap(tempArray,tempAccess) #OBTENGO EL TAMANIO
            self.generator.addExpression(newTemp,tempArray,'2','/') #CALCULO EL TAMANIO REAL
            return Value(newTemp,True,typeExpression.INTEGER) #RETORNO EL TAMANIO
            
        elif(expression.type == typeExpression.CADENA):
            self.generator.addExpression(newTemp,newTemp,'1','-') #RESTO UNO PORQUE ANTERIRORMENTE SUME
            return Value(newTemp,True,typeExpression.INTEGER)

        print("El tipo no puede ser usado con length")
        return Value("0",False,typeExpression.INTEGER)