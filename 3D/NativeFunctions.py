
#CREACION DE LA FUNCIONES NATIVAS DESDE ALTO NIVEL PARA UTILIZARLAS EN BAJO NIVEL
NativeFunctions = '''

function string_elevation(cadena::String,potencia::Int64)
    res = cadena;
    for i in 1:potencia - 1
        res = res * cadena;
    end;
    return res;
end;

'''