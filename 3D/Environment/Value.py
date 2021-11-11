from Enum_types.typeExpression import typeExpression

class Value:

    def __init__(self, value:str, isTemp:bool, type:typeExpression) -> None:
        self.value = value
        self.isTemp = isTemp
        self.type = type
        self.trueLabel = ""
        self.falseLabel = ""
        self.arrayValues = []
        self.typeArray = None #GUARDA EL TIPO DEL ARRAY

    def getValue(self):
        return self.value
    
    def getType(self):
        return self.type
    
    #METODO PARA OBTENER LOS VALORES DEL STRING
    def getString(self,generator):#,tempValue):
        newTemp = generator.newTemp()
        generator.addGetHeap(newTemp, self.value)
        top = generator.newTemp()
        generator.addExpression(top,self.value,'1','+')
        cont = generator.newTemp()
        generator.addExpression(cont,newTemp,self.value,'+')

        newLabel = generator.newLabel()
        generator.addLabel(newLabel)

        labelTrue = generator.newLabel()
        labelFalse = generator.newLabel()
        generator.addIf(top,cont,'<',labelTrue)
        generator.addGoto(labelFalse)
        generator.addLabel(labelTrue)
        tempHeap = generator.newTemp()
        generator.addGetHeap(tempHeap,top)
        generator.addSetHeap('H',tempHeap)
        generator.addNextHeap()
        generator.addExpression(top,top,'1','+')
        generator.addGoto(newLabel)
        generator.addLabel(labelFalse)