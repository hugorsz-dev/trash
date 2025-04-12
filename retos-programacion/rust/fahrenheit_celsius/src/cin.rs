pub fn i8 () -> i8 {

    loop {
        let mut input = String::new(); // esta estructura, a diferencia de let mut selection ="", permite vivir en la memoria dinámica
        
        std::io::stdin()
            .read_line (&mut input) // esto no es una variable, es una referencia
            .expect ("Failed to read line");

        // Conversión a número entero. 

        match input.trim().parse() {
            Ok(number) => {
                return number;
            }, 
            Err(_) => {
                println! ("You have not entered a i8 number!");
            }
        };
        
    }

}

pub fn f64 () -> f64 {
    loop {
        let mut input = String::new(); // esta estructura, a diferencia de let mut selection ="", permite vivir en la memoria dinámica
        
        std::io::stdin()
            .read_line (&mut input) // esto no es una variable, es una referencia
            .expect ("Failed to read line");

        // Conversión a número entero. 

        match input.trim().parse() {
            Ok(number) => {
                return number;
            }, 
            Err(_) => {
                println! ("You have not entered a f64 number!");
            }
        };
        
    }

}
