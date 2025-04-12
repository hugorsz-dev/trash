def arrayACadena (array):
    nuevaCadena ="";
    for digito in array:
        nuevaCadena = nuevaCadena+digito;
    return nuevaCadena;

def invertirArray (array, m="a"):
    nuevoArray = [];
    for i in range (len(array)):
        nuevoArray.append (array[len(array)-i-1])
    if m=="c":
        return arrayACadena (nuevoArray);
    return nuevoArray;

def enteroABinario (entero):
    binario = "";

    while entero!=0:
        if (entero%2)==0:
            binario = binario + "0";
        else:
            binario = binario + "1";
        entero = entero//2;
        
    return invertirArray( binario, "c");

print ("Conversión de INT a binario")

while True:

    entero = -1;

    while entero<0:
        entero = int (input("Introduzca el número entero que desea convertir a binario: "));
        if entero < 0: print ("¡Recuerde introducir un número positivo");

    print (enteroABinario (entero)); 
