fn generate_fibonacci(limit: u128) {
    let mut term: u128 = 1;
    let mut aux: u128 = 1;
    let mut result: u128 = 0;

    for number in 2..limit + 2 {
        if number % 2 == 0 {
            aux = result;
        } else {
            term = result;
        }

        result = term + aux;

        println!("{result}")
    }
}

fn fibonacci(number: f64) -> f64 {
    let phi: f64 = (1.0 + 5.0f64.sqrt()) / 2.0;
    (phiº.powf(number) - (-phi.powf(-1.0).powf(number))) / 5.0f64.sqrt()
}

fn main() {
    generate_fibonacci(12);
    println!("{}", fibonacci(800.0));
}
