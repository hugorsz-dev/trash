/*
 * Crea una función que sea capaz de leer el número representado por el ábaco.
 * - El ábaco se representa por un array con 7 elementos.
 * - Cada elemento tendrá 9 "O" (aunque habitualmente tiene 10 para realizar
 *   operaciones) para las cuentas y una secuencia de "---" para el alambre.
 * - El primer elemento del array representa los millones, y el último las unidades.
 * - El número en cada elemento se representa por las cuentas que están a
 *   la izquierda del alambre.
 *
 * Ejemplo de array y resultado:
 * ["O---OOOOOOOO",
 *  "OOO---OOOOOO",
 *  "---OOOOOOOOO",
 *  "OO---OOOOOOO",
 *  "OOOOOOO---OO", // etc 
 *  "OOOOOOOOO---", // 9 decenas (90)
 *  "---OOOOOOOOO"] // 0 uds
 *  
 *  Resultado: 1.302.790
 */
 
 
package Retos;
 
public class Reto31Abaco {
 
	// CONSTRUCTOR
 
	public Reto31Abaco (String [] abaco) {
		this.abaco = abaco;
	}
 
	// ATRIBUTOS
 
	public String [] abaco = new String [6];
 
	// MÉTODOS
 
	/**
	 * Imprime nuestro ábaco, innecesario, pero pertinente. 
	 */
 
	public void imprimirAbaco () {
 
		for (int i=0; i< abaco.length; i++) {
			System.out.println (abaco[i]);
		}
 
	}
 
	/**
	 * Analiza el trazo, de modo que: 
	 * 
	 * Cuenta los elementos del array hasta encontrar un carácter '-'. 
	 * @param trazo
	 * @return
	 */
 
	private int analizarTrazo (String trazo) {
 
		int contador =0; 
		boolean bandera = false;
 
		while (bandera == false) {		
 
			if (trazo.charAt(contador) == '-') {
				bandera = true;
			}
			else {
				contador++;	
			}
 
		}
 
		return contador;
 
	}
 
	/**
	 * Utiliza la función de analizar trazo, y sobre el resutado, lo eleva a una potencia de diez inversa al punto en que se encuentra el array
	 * @return
	 */
 
	public int calcularAbaco () {
 
		int resultado =0; 
 
		for (int i=0; i< abaco.length; i++) {
			resultado = (int) (resultado + (analizarTrazo (abaco[i])*Math.pow(10, abaco.length-1-i)));
		}
 
		return resultado;
 
	}
 
	// MÉTODO PRINCIPAL
 
	public static void main(String[] args){
 
		String [] abaco = {
			"O---OOOOOOOO",
			"OOO---OOOOOO",
			"---OOOOOOOOO",
			"OO---OOOOOOO",
			"OOOOOOO---OO",
			"OOOOOOOOO---",
			"---OOOOOOOOO"	
		};
 
		Reto31Abaco reto = new Reto31Abaco (abaco);
 
		System.out.println (reto.calcularAbaco());
 
 
	}
 
 
}