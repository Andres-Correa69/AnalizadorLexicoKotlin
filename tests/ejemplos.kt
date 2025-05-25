// Ejemplo 1: Función simple
fun suma(a: Int, b: Int): Int {
    val resultado = a + b
    return resultado
}

// Ejemplo 2: Uso de operadores y comentarios
fun operaciones() {
    var x = 10
    var y = 20.5
    
    /* Este es un comentario
       de múltiples líneas */
    if (x > 0 && y <= 30.0) {
        x++
        y = y * 2
    }
}

// Ejemplo 3: Cadenas y caracteres especiales
fun ejemploCadenas() {
    val str1 = "Hola \"Mundo\""
    val str2 = "Línea 1\\nLínea 2"
    when (str1) {
        "test" -> println(str1)
        else -> println(str2)
    }
} 