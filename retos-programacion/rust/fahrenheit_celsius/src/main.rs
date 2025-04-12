
/*
    Función que despliega un menú basado en un array de strings
        - Date cuenta, el "&" delante de algo significa que es indeterminado.
            El array del parámetro será de una cantidad indeterminada &[tipo]
            El tipo string significa que es un conjunto indeterminado de caracteres en la memoria &str
*/

mod cin;

fn display_menu (menu_options: &[&str]) -> i8 {
    let mut counter = 0;
    for option in menu_options {
        println! ("{counter} {option}");
        counter+=1;
    };

    // Entrada de un número para seleccionar en el menú.

    let selection: i8 = cin::i8();

    // Comprobación de que el número no excede a la cantidad de selecciones

    if selection > menu_options.len() as i8 {
        println! ("Your selection exceeds the number of options!");
        return -1; 
    }

    // Devolver el formato

    selection
    
}

fn fah_to_celsius (fah: f64)  -> f64 {
    (fah-32.0)*(5.0/9.0)
}

fn celsius_to_fah (celsius: f64) -> f64 {
    celsius*(9.0/5.0)+32.0  
}

fn main() {

    let selection : i8 = display_menu (&["Convert Fahrenheit to Celsius", "Convert Celsius to Fahrenheit"]);

    match selection {
        0 => {
            println!("Insert value in fahrenheit (Fº): ");
            println! ("The conversion in celsius (Cº) is: {}", fah_to_celsius(cin::f64()))
        },
        1 => {
            println!("Insert value in celsius (Cº): ");
            println! ("The conversion in fahrenheit (Fº) is: {}", celsius_to_fah(cin::f64()))
        },
        _ => {
            println!("Fatal error");
        }
    };

}
