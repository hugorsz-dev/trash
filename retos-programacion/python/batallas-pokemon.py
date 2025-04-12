
'''
 * Crea un programa que calcule el daño de un ataque durante
 * una batalla Pokémon.
 * - La fórmula será la siguiente: daño = 50 * (ataque / defensa) * efectividad
 * - Efectividad: x2 (súper efectivo), x1 (neutral), x0.5 (no es muy efectivo)
 * - Sólo hay 4 tipos de Pokémon: Agua, Fuego, Planta y Eléctrico 
 *   (buscar su efectividad)
 * - El programa recibe los siguientes parámetros:
 *   Pokémon atacante.
 *  - Tipo del Pokémon defensor.
'''
'''
Agua:

x2 contra Fuego
x2 contra Planta
x0.5 contra Agua
x1 contra Eléctrico
Fuego:

x2 contra Planta
x0.5 contra Fuego
x1 contra Agua
x1 contra Eléctrico
Planta:

x2 contra Agua
x0.5 contra Planta
x1 contra Fuego
x1 contra Eléctrico
Eléctrico:

x2 contra Agua
x1 contra Fuego
x1 contra Planta
x0.5 contra Eléctrico
'''


efectividadAtaque = {
    "agua": {"agua": 0.5, "fuego": 2, "planta": 2, "electrico": 1},
    "fuego": {"agua": 2, "fuego": 0.5, "planta": 2, "electrico": 1},
    "planta": {"agua": 2, "fuego": 1, "planta": 0.5, "electrico": 1},
    "electrico": {"agua": 2, "fuego": 1, "planta": 1, "electrico": 0.5},
}

class Pokemon ():
    def __init__ (self, nombre, ataque, defensa, vida, tipo):
        self.nombre = nombre;
        self.ataque = ataque; 
        self.defensa = defensa;
        self.tipo = tipo; 
        self.vida = vida;
        
    def atacar (self, contrincante):
        selfEfectividad = efectividadAtaque[self.tipo][contrincante.tipo];
        contrincanteEfectividad = efectividadAtaque[contrincante.tipo][self.tipo];
        
        danio= (50 * (self.ataque / contrincante.defensa) * selfEfectividad);
        
        print (f"{self.nombre} ataca a {contrincante.nombre} y le hace {danio} ptos de daño");
        
        contrincante.vida = contrincante.vida - danio;
        
        if contrincante.vida<=0:
            return False

        return True
    
    def mostrarEstadisticas (self):
        print (f"Estadísticas de {self.nombre}: ATAQUE: {self.ataque}, DEFENSA: {self.defensa}, VIDA: {self.vida}, TIPO: {self.tipo} ")

def combatirHastaLaMuerte (pokemon1, pokemon2):
    print (f"EMPIEZA el combate más esperado: {pokemon1.nombre} VS {pokemon2.nombre}");
    print ("-------------------")
    pokemon1.mostrarEstadisticas()
    print ("-------------------")
    pokemon2.mostrarEstadisticas()
    print ("-------------------")
    
    ganador = ""
    while True:
        if pokemon1.atacar(pokemon2) == False:
            print (f"{pokemon2.nombre} ha muerto.")
            ganador = pokemon1;
            break; 
        
        if pokemon2.atacar(pokemon1) == False:
            print (f"{pokemon1.nombre} ha muerto.")
            ganador = pokemon2;
            break; 
        
        print (f"|| vida de {pokemon1.nombre}: {pokemon1.vida}, vida de {pokemon2.nombre}: {pokemon2.vida} ||")
    print ("-------------------")
        
    print (f"El ganador ha sido {ganador.nombre}, todavía tiene {ganador.vida} ptos de vida restantes ¡enhorabuena!");
pikachu = Pokemon ("pikachu",50,20,900,"electrico");
charmander = Pokemon ("charmander", 120,10,800, "fuego"); 
       
        
combatirHastaLaMuerte(pikachu, charmander)            
       

         
    
        
    
    
    

    


