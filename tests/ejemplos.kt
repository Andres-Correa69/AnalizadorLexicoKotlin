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

// Ejemplo 4: Identificadores y estructuras
fun ejemploIdentificadores() {
    val variable_1 = 10
    var _test = 20
    
    when (_test) {
        10, 20, 30 -> {
            variable_1 + _test
        }
        else -> 0
    }
}

// Ejemplo 5: Operaciones matemáticas
fun calculadora(x: Double, y: Double) {
    val suma = x + y
    val resta = x - y
    val multiplicacion = x * y
    val division = x / y
    val modulo = x % y
    
    if (x >= y || y <= x) {
        println("Comparación realizada")
    }
}

// Ejemplo 6: Estructura compleja
fun ejemploComplejo() {
    val lista = listOf(1, 2.5, 3.14)
    var contador = 0
    
    /* Probando diferentes
       estructuras y tokens */
    when (contador) {
        0 -> println("Inicio")
        1 -> {
            contador++
            println(lista)
        }
        else -> {
            if (contador <= 10 && lista.size >= 3) {
                println("Fin")
            }
        }
    }
}

// ============= EJEMPLOS CON ERRORES =============

// Error 1: Identificador demasiado largo (más de 10 caracteres)
fun errorIdentificadorLargo() {
    val este_identificador_es_muy_largo = 10
    var otro_identificador_largo_tambien = 20
}

// Error 2: Cadenas mal formadas
fun errorCadenas() {
    // Cadena sin cerrar
    val str1 = "Esta cadena no tiene cierre
    
    // Carácter de escape al final
    val str2 = "Escape inválido\"
    
    // Salto de línea en cadena
    val str3 = "Esta cadena tiene
    un salto de línea"
}

// Error 3: Comentarios mal formados
fun errorComentarios() {
    /* Este comentario no se cierra
    
    // Este es un comentario normal
    val x = 10
    /* Este es otro comentario
       que tampoco se cierra
}

// Error 4: Caracteres no válidos
fun errorCaracteres() {
    val simbolo1 = @#$
    val simbolo2 = ¡¿?¬
    val numero@ = 123
}

// Error 5: Números mal formados
fun errorNumeros() {
    val decimal1 = 123.
    val decimal2 = .123
    val decimal3 = 1..2
    val decimal4 = 1.2.3
}

// Error 6: Operadores inválidos
fun errorOperadores() {
    val a = 10
    val b = 20
    
    // Operadores incompletos o inválidos
    if (a =< b) {  // Operador mal escrito
        a +* b     // Operadores juntos inválidos
        a >>> b    // Operador que no existe en Kotlin
    }
} 