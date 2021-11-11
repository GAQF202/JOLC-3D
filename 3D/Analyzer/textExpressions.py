from Analyzer.giveMeType import parser

def textExpression(cadena:str,environment):
    res = ''
    resString = ''
    exps = []
    concatenar = False
    state = 0
    
    for caracter in cadena:
        if caracter != ' ' or caracter != '\n':
            if caracter == '(':
                state += 1
            if concatenar:
                res += caracter
            else:
                resString += caracter
            if caracter == ')':
                state -= 1
            if state == 0:
                concatenar = False
                if res != '':
                    exps.append(parser.parse(res[1:-1]).execute(environment))
                res = ''
            if caracter == '$':
                concatenar = True
        else:
            continue
    contador = 0
    valueRes = ''
    for caracter in resString:
        if(caracter == '$'):
            valueRes += str(exps[contador].getValue())
            contador+=1
        else:
            valueRes += caracter

    return valueRes

def textValue(cadena : str, environment):
    exp = ''
    resString = ''
    exps = []
    cantidadEscapes = 0
    concatenar = False
    hayEscape = False
    state = 0

    for i in range(len(cadena)):
        if concatenar:
            exp += cadena[i]
        else:
            resString += cadena[i]

        if cadena[i] == '(':
            state += 1
        if cadena[i] == ')':
            state -= 1
    
        if i == (len(cadena)-1) and hayEscape:
            exps.append(parser.parse(exp).execute(environment))
            #exps.append(exp)
            exp = ''
                
        if cadena[i] == '$':
            hayEscape = True
            cantidadEscapes += 1
            if cantidadEscapes == 2:
                exps.append(parser.parse(exp[0:-1]).execute(environment))
                exp = ''
                cantidadEscapes -= 1
                if cadena[i-1] != ' ':
                    resString += cadena[i]

            concatenar = True
    
        if cadena[i] == ' ' and state == 0:
            resString += ' '
            concatenar = False

    contador = 0
    valueRes = ''
    #print(resString)
    for caracter in resString:
        if(caracter == '$'):
            valueRes += str(exps[contador].getValue())
            #valueRes += str(exps[contador])
            contador+=1
        else:
            valueRes += caracter

    return valueRes