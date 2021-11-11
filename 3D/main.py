from Analyzer.gramatica import parser
from NativeFunctions import NativeFunctions


if __name__ == "__main__":
    f = open("./entrada.txt", "r")
    input = f.read()
    C3D = parser.parse(NativeFunctions + input)   
    f2 = open("./salida.txt","w")
    f2.write(C3D)