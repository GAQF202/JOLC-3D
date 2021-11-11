class Symbol:
    #ID TIPO POSICION ATRIBUTOS A TOMAR EN CUENTA 
    def __init__(self, type, id: str, row, column, datatype, position):
        self.type = type
        self.id = id
        #self.value = value
        self.row = row
        self.column = column
        self.datatype = datatype #VARIABLE PARA SABER SI ES UN STRUCT, VECTOR, etc...
        self.position = position
        self.arrayValues = []
        self.typeArray = None 

    def getId(self):
        return self.id

    def getValue(self):
        return self.value
    
    def getType(self):
        return self.type