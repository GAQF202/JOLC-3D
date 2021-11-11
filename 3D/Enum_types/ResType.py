from Enum_types.typeExpression import typeExpression

ResType = [
                #STRING                     INTEGER                     FLOAT
    #STRING
    [   
                typeExpression.CADENA,      typeExpression.CADENA,      typeExpression.CADENA
    ],
    #INTEGER
    [
                typeExpression.ERROR,      typeExpression.INTEGER,     typeExpression.FLOAT
    ],
    #FLOAT
    [
                typeExpression.ERROR,      typeExpression.FLOAT,       typeExpression.FLOAT
    ]
]

RelationalResType =[
                #STRING                     INTEGER                     FLOAT                     BOOL                                NULO                      STRUCT              
    
    #STRING
    [   
                typeExpression.CADENA,      typeExpression.ERROR,      typeExpression.ERROR,      typeExpression.ERROR,      "",      typeExpression.NULO,      typeExpression.ERROR
    ],
    #INTEGER
    [
                typeExpression.ERROR,      typeExpression.INTEGER,     typeExpression.FLOAT,      typeExpression.ERROR,      "",      typeExpression.NULO,      typeExpression.ERROR
    ],
    #FLOAT
    [
                typeExpression.ERROR,      typeExpression.FLOAT,       typeExpression.FLOAT,      typeExpression.ERROR,      "",      typeExpression.NULO,      typeExpression.ERROR
    ],
    #BOOL
    [
                typeExpression.ERROR,      typeExpression.ERROR,       typeExpression.ERROR,      typeExpression.BOOL,      "",       typeExpression.NULO,      typeExpression.ERROR
    ],
    #VACIO
    [
                                  "",                        "",                          "",                      "",      "",                        "",                       ""
    ],
    #NULO
    [
                typeExpression.NULO,       typeExpression.NULO,        typeExpression.NULO,       typeExpression.NULO,      "",      typeExpression.NULO,      typeExpression.STRUCT
    ],
    #STRUCT
    [
                typeExpression.ERROR,      typeExpression.ERROR,       typeExpression.ERROR,      typeExpression.ERROR,      "",     typeExpression.STRUCT,     typeExpression.STRUCT
    ]
]